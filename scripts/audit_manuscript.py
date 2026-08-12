#!/usr/bin/env python3
"""Mechanical audit of a manuscript: reports candidate problems, not verdicts.

Standard library only. Handles .tex / .md / .txt, mixed English and Chinese.
The script covers only what a rule can decide. Semantic judgement — whether the
contributions are vague, whether the discussion explains a mechanism — stays with
a human or a model.

Usage:
    python3 audit_manuscript.py paper.tex
    python3 audit_manuscript.py paper.tex --terms "power grid=power network"
    python3 audit_manuscript.py paper.tex --topic-sentences
    python3 audit_manuscript.py paper.tex --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

CJK = r"\u4e00-\u9fff"

# Roman numerals and all-caps words that are not acronyms
DEFAULT_ACRONYM_SKIP = {
    "I", "A", "AND", "OR", "THE", "OF", "IN", "ON", "TO", "FOR", "WITH", "AS", "AT", "BY",
    "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII",
    "OK", "NO", "AM", "PM", "TODO", "NOTE", "FIG", "TAB", "EQ", "REF", "SEC", "APP",
}

# Wordings commonly mixed for one concept; reported when a group has 2+ variants present
DEFAULT_TERM_GROUPS = [
    ("power grid", "power network"),
    ("case embedding", "case conditioning"),
    ("dataset", "data set"),
    ("state-of-the-art", "state of the art"),
    ("hyperparameter", "hyper-parameter"),
    ("multi-task", "multitask"),
    ("pre-training", "pretraining"),
    ("fine-tuning", "finetuning"),
    ("neural network", "neural net"),
    ("optimize", "optimise"),
    ("analyze", "analyse"),
    ("behavior", "behaviour"),
    ("modeling", "modelling"),
]

ABSOLUTE_PATTERNS = [
    (r"\bthe key\b(?! factor)", "the key -> one key factor"),
    (r"\bthe only\b", "the only -> one plausible / among the few"),
    (r"\bthe first (?:to|work|method|paper|study|attempt)\b",
     'rewrite as "to the best of our knowledge, X has not been systematically addressed in Y"'),
    (r"\bfor the first time\b", 'rewrite as "to the best of our knowledge..."'),
    (r"\bfirst-ever\b", "drop the absolute claim"),
    (r"\bwe are the first\b", 'rewrite as "to the best of our knowledge..."'),
    (r"\bunprecedented\b", "drop the absolute claim"),
    (r"\b(?:completely|perfectly|fully) (?:solves?|addresses?|eliminates?)\b",
     "over-claiming; scope the statement"),
    (r"首次提出", 'rewrite as "to the best of our knowledge..."'),
    (r"首个", "scope the statement"),
    (r"完美(?:解决|克服)", "over-claiming"),
]

CONNECTORS = [
    "Moreover", "Furthermore", "Additionally", "In addition", "However",
    "Nevertheless", "Therefore", "Thus", "Hence", "Consequently",
]

SUBORDINATE_MARKERS = [
    "which", "that", "where", "when", "while", "although", "though",
    "whereas", "because", "since", "whether", "who", "whom", "whose",
]

ABBREVIATIONS = [
    "et al.", "i.e.", "e.g.", "vs.", "cf.", "Fig.", "Figs.", "Tab.", "Eq.", "Eqs.",
    "Sec.", "Ref.", "Refs.", "Dr.", "Prof.", "approx.", "resp.", "w.r.t.", "Alg.",
]

MATH_ENVS = [
    "equation", "equation*", "align", "align*", "gather", "gather*",
    "eqnarray", "eqnarray*", "multline", "multline*", "split", "displaymath",
]


# --------------------------------------------------------------------------- cleaning


def _blank(match: re.Match) -> str:
    """Replace a match with equal-length blanks so line numbers and offsets survive."""
    return re.sub(r"[^\n]", " ", match.group(0))


def clean_source(raw: str, suffix: str) -> str:
    """Strip comments, math, code and citation commands, preserving character offsets."""
    text = raw

    if suffix == ".tex":
        text = re.sub(r"(?<!\\)%[^\n]*", _blank, text)
        for env in MATH_ENVS:
            text = re.sub(
                r"\\begin\{" + re.escape(env) + r"\}.*?\\end\{" + re.escape(env) + r"\}",
                _blank, text, flags=re.DOTALL,
            )
        text = re.sub(r"\\\[.*?\\\]", _blank, text, flags=re.DOTALL)
        text = re.sub(r"\\\(.*?\\\)", _blank, text, flags=re.DOTALL)
        text = re.sub(r"\\(?:cite[a-zA-Z]*|ref|eqref|label|autoref|cref|Cref)\s*\{[^}]*\}", _blank, text)
        text = re.sub(r"\\(?:usepackage|documentclass|bibliography[a-z]*|input|include)\s*(\[[^\]]*\])?\{[^}]*\}", _blank, text)
        text = re.sub(r"\\begin\{(?:tabular|verbatim|lstlisting)\}.*?\\end\{(?:tabular|verbatim|lstlisting)\}", _blank, text, flags=re.DOTALL)
        text = re.sub(r"\\(?:begin|end)\s*\{[^}]*\}", _blank, text)
        # unescape without changing length
        text = re.sub(r"\\([%&_#$])", r" \1", text)
        text = re.sub(r"\\[a-zA-Z]+\*?", _blank, text)
        text = re.sub(r"[{}]", " ", text)
    else:
        text = re.sub(r"```.*?```", _blank, text, flags=re.DOTALL)
        text = re.sub(r"`[^`\n]*`", _blank, text)
        text = re.sub(r"\$\$.*?\$\$", _blank, text, flags=re.DOTALL)

    text = re.sub(r"(?<!\\)\$[^$\n]*\$", _blank, text)
    return text


def line_of(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


def snippet(text: str, pos: int, width: int = 70) -> str:
    start = max(0, pos - width // 3)
    end = min(len(text), pos + width)
    return " ".join(text[start:end].split())


# --------------------------------------------------------------------------- segmentation


def split_sentences(paragraph: str):
    """Return [(sentence, offset within paragraph)] for English and Chinese alike."""
    protected = paragraph
    for i, abbr in enumerate(ABBREVIATIONS):
        protected = protected.replace(abbr, abbr.replace(".", f"\x00{i}\x00"))

    spans, start = [], 0
    for match in re.finditer(r"(?<=[.!?])[ \t\n]+|(?<=[。！？；])", protected):
        end = match.start()
        if end > start:
            spans.append((start, end))
        start = match.end()
    if start < len(protected):
        spans.append((start, len(protected)))

    out = []
    for s, e in spans:
        raw = protected[s:e]
        for i, abbr in enumerate(ABBREVIATIONS):
            raw = raw.replace(abbr.replace(".", f"\x00{i}\x00"), abbr)
        if raw.strip():
            out.append((raw, s))
    return out


def iter_paragraphs(text: str):
    """Return [(paragraph, start offset in the full text)]."""
    out, pos = [], 0
    for chunk in re.split(r"\n[ \t]*\n", text):
        if chunk.strip():
            out.append((chunk, pos))
        pos += len(chunk) + 2
    return out


# --------------------------------------------------------------------------- checks


def _is_shouting_line(text: str, pos: int) -> bool:
    """An all-caps heading is not a source of acronyms."""
    start = text.rfind("\n", 0, pos) + 1
    end = text.find("\n", pos)
    line = text[start:end if end != -1 else len(text)].strip()
    if len(line) > 80 or re.search(f"[{CJK}]", line):
        return False
    letters = re.findall(r"[A-Za-z]", line)
    words = re.findall(r"[A-Za-z]{2,}", line)
    return len(words) >= 2 and bool(letters) and all(c.isupper() for c in letters)


def check_acronyms(text: str, skip: set) -> list:
    findings, seen = [], OrderedDict()
    pattern = re.compile(r"\b[A-Z][A-Za-z0-9]*[A-Z0-9](?:-[A-Z0-9]+)*\b")
    for match in pattern.finditer(text):
        token = match.group(0)
        if token.upper() in skip or token in skip or not re.search(r"[A-Z]{2}", token):
            continue
        if len(token) > 12 or _is_shouting_line(text, match.start()):
            continue
        seen.setdefault(token, match.start())

    for token, pos in seen.items():
        before = text[max(0, pos - 140):pos]
        after = text[pos + len(token):pos + len(token) + 140]
        inside_parens = before.rfind("(") > before.rfind(")") and after.find(")") != -1
        expanded_after = re.match(r"\s*\([^)]{4,}\)", after) is not None
        if inside_parens or expanded_after:
            continue
        findings.append({
            "check": "undefined-acronym",
            "line": line_of(text, pos),
            "item": token,
            "message": f"{token} has no full form or definition at first use",
            "fix": "give the full form and a gloss at first use, e.g. Full Name (ABC)",
            "context": snippet(text, pos),
        })
    return findings


def check_sentences(text: str) -> list:
    findings = []
    for para, para_pos in iter_paragraphs(text):
        for sentence, offset in split_sentences(para):
            pos = para_pos + offset
            line = line_of(text, pos)
            stripped = sentence.strip()
            cjk_chars = len(re.findall(f"[{CJK}]", stripped))
            words = re.findall(r"[A-Za-z][A-Za-z'\-]*", stripped)
            commas = len(re.findall(r"[,，]", stripped))

            if cjk_chars > len(words):
                if len(stripped) > 90:
                    findings.append(_sentence_finding("long-sentence", line, stripped,
                                                      f"{len(stripped)} characters, over the 90 limit",
                                                      "split it; one point per sentence"))
                if commas >= 4:
                    findings.append(_sentence_finding("comma-chain", line, stripped,
                                                      f"{commas} commas in one sentence",
                                                      "split it; avoid stacked parentheticals"))
                continue

            if len(words) > 40:
                findings.append(_sentence_finding("long-sentence", line, stripped,
                                                  f"{len(words)} words, over the 40 limit",
                                                  "split it; one point per sentence"))
            if commas >= 3:
                findings.append(_sentence_finding("comma-chain", line, stripped,
                                                  f"{commas} commas in one sentence",
                                                  "split it; avoid stacked parentheticals"))
            clauses = sum(len(re.findall(rf"\b{m}\b", stripped, re.IGNORECASE)) for m in SUBORDINATE_MARKERS)
            if clauses >= 3:
                findings.append(_sentence_finding("too-many-clauses", line, stripped,
                                                  f"{clauses} subordinate clause markers",
                                                  "one point per sentence; at most one subordinate clause"))
    return findings


def _sentence_finding(check: str, line: int, sentence: str, message: str, fix: str) -> dict:
    text = " ".join(sentence.split())
    return {
        "check": check,
        "line": line,
        "item": text[:60] + ("..." if len(text) > 60 else ""),
        "message": message,
        "fix": fix,
        "context": text[:160],
    }


def check_terms(text: str, groups: list) -> list:
    findings = []
    lowered = text.lower()
    for group in groups:
        counts = {v: len(re.findall(rf"(?<![\w-]){re.escape(v.lower())}(?![\w-])", lowered)) for v in group}
        present = {v: c for v, c in counts.items() if c}
        if len(present) < 2:
            continue
        winner = max(present, key=present.get)
        detail = ", ".join(f"{v} x{c}" for v, c in present.items())
        first = min(lowered.find(v.lower()) for v in present)
        findings.append({
            "check": "term-inconsistency",
            "line": line_of(text, first),
            "item": " / ".join(present),
            "message": f"one concept, several wordings: {detail}",
            "fix": f"pick one and replace throughout (most frequent: {winner}); add it to the terminology table",
            "context": detail,
        })
    return findings


def check_float_order(text: str) -> list:
    findings = []
    kinds = {
        "Figure": r"(?:Fig(?:ure)?s?\.?~?\s*|图\s*)(\d+)",
        "Table": r"(?:Tab(?:le)?s?\.?~?\s*|表\s*)(\d+)",
        "Equation": r"(?:Eq(?:uation|n)?s?\.?~?\s*\(?|式\s*\(?)(\d+)\)?",
    }
    for label, pattern in kinds.items():
        order, first_pos = [], {}
        for match in re.finditer(pattern, text):
            num = int(match.group(1))
            if num not in first_pos:
                first_pos[num] = match.start()
                order.append(num)
        if not order:
            continue
        expected = list(range(1, len(order) + 1))
        if order != expected:
            findings.append({
                "check": "float-order",
                "line": line_of(text, first_pos[order[0]]),
                "item": f"{label} citation order",
                "message": f"first-citation order is {order}, expected {expected}",
                "fix": "renumber in order of first citation; confirm each float is cited before it appears",
                "context": f"{label} " + " -> ".join(str(n) for n in order),
            })
    return findings


def check_absolutes(text: str) -> list:
    findings = []
    for pattern, fix in ABSOLUTE_PATTERNS:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            findings.append({
                "check": "absolute-wording",
                "line": line_of(text, match.start()),
                "item": match.group(0),
                "message": "absolute or over-claiming wording",
                "fix": fix,
                "context": snippet(text, match.start()),
            })
    return findings


def check_math_in_prose(text: str) -> list:
    findings = []
    for match in re.finditer(r"(?<!\S)[+&=](?!\S)", text):
        symbol = match.group(0)
        findings.append({
            "check": "math-symbol-in-prose",
            "line": line_of(text, match.start()),
            "item": symbol,
            "message": f"math symbol {symbol} in running prose",
            "fix": 'keep math symbols out of prose; write "and" instead of "+"',
            "context": snippet(text, match.start()),
        })
    return findings


def check_significance(text: str) -> list:
    findings = []
    for para, para_pos in iter_paragraphs(text):
        for sentence, offset in split_sentences(para):
            if not re.search(r"\bsignificant(?:ly)?\b|显著", sentence, re.IGNORECASE):
                continue
            if re.search(r"\bp\s*[<=>]|p-value|置信区间|confidence interval|\bCI\b", sentence, re.IGNORECASE):
                continue
            findings.append(_sentence_finding(
                "unsupported-significance", line_of(text, para_pos + offset), sentence,
                'claims "significant" with no statistic in the same sentence',
                "add the test and its p-value or confidence interval, or drop the statistical wording"))
    return findings


def check_connectors(text: str) -> list:
    words = len(re.findall(r"[A-Za-z][A-Za-z'\-]*", text))
    if words < 200:
        return []
    counts = Counter()
    positions = {}
    for connector in CONNECTORS:
        for match in re.finditer(rf"\b{re.escape(connector)}\b", text):
            counts[connector] += 1
            positions.setdefault(connector, match.start())
    budget = max(3, words // 500)
    findings = []
    for connector, count in counts.items():
        if count > budget:
            findings.append({
                "check": "connector-overuse",
                "line": line_of(text, positions[connector]),
                "item": connector,
                "message": f"{connector} used {count} times in ~{words} words (budget {budget})",
                "fix": "rotate within the function: addition Moreover/Additionally, escalation Furthermore, "
                       "cause Therefore/Thus, contrast However/Nevertheless",
                "context": "",
            })
    return findings


def collect_topic_sentences(text: str) -> list:
    out = []
    for index, (para, para_pos) in enumerate(iter_paragraphs(text), start=1):
        sentences = split_sentences(para)
        if not sentences:
            continue
        first = " ".join(sentences[0][0].split())
        out.append({
            "paragraph": index,
            "line": line_of(text, para_pos),
            "first_sentence": first[:140] + ("..." if len(first) > 140 else ""),
        })
    return out


# --------------------------------------------------------------------------- reporting

CHECK_TITLES = {
    "undefined-acronym": "Undefined acronyms and symbols",
    "term-inconsistency": "Inconsistent terminology",
    "long-sentence": "Over-long sentences",
    "comma-chain": "Comma chains",
    "too-many-clauses": "Too many subordinate clauses",
    "absolute-wording": "Absolute wording",
    "math-symbol-in-prose": "Math symbols in prose",
    "float-order": "Float and equation numbering order",
    "unsupported-significance": "Unsupported claims of significance",
    "connector-overuse": "Overused connectives",
}

CHECK_ORDER = list(CHECK_TITLES)

NOT_CHECKED = ("Not checked here: whether the contributions are vague, whether a strong baseline is missing, "
               "whether the discussion explains a mechanism, whether captions read standalone. "
               "Check those against references/ by hand.")


def render_text(path: Path, findings: list, topics) -> str:
    lines = [f"# Mechanical audit: {path.name}", ""]
    if not findings:
        lines.append("No mechanical problems found. Structural and semantic issues "
                     "(topic sentences, contributions, baselines, discussion depth) still need review.")
    else:
        grouped = {}
        for f in findings:
            grouped.setdefault(f["check"], []).append(f)
        lines.append(f"{len(findings)} candidate problems across {len(grouped)} categories. "
                     "These are candidates, not verdicts.")
        lines.append("")
        for check in CHECK_ORDER:
            items = grouped.get(check)
            if not items:
                continue
            lines.append(f"## {CHECK_TITLES[check]} ({len(items)})")
            lines.append("")
            for f in sorted(items, key=lambda x: x["line"]):
                lines.append(f"- L{f['line']} `{f['item']}` — {f['message']}")
                lines.append(f"  Fix: {f['fix']}")
                if f["context"]:
                    lines.append(f"  Context: {f['context']}")
            lines.append("")

    if topics is not None:
        lines.append("## Topic sentences")
        lines.append("")
        lines.append("Read the first sentences in order. If they do not chain into the argument "
                     "of the section, the topic sentences are not doing their job.")
        lines.append("")
        for t in topics:
            lines.append(f"- P{t['paragraph']} (L{t['line']}) {t['first_sentence']}")
        lines.append("")

    lines.append("---")
    lines.append(NOT_CHECKED)
    if path.suffix == ".tex":
        lines.append(r"Note: \ref{} does not resolve to a number, so check float ordering "
                     "against the compiled PDF.")
    return "\n".join(lines)


# --------------------------------------------------------------------------- entry point


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Mechanical audit of a manuscript")
    parser.add_argument("path", type=Path, help="path to a .tex / .md / .txt manuscript")
    parser.add_argument("--terms", nargs="*", default=[],
                        help='extra terminology groups, = separated, e.g. "power grid=power network"')
    parser.add_argument("--ignore", nargs="*", default=[],
                        help="acronyms to skip, e.g. CNN GPU")
    parser.add_argument("--topic-sentences", action="store_true",
                        help="also list the first sentence of every paragraph")
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument("--strict", action="store_true", help="exit 1 when anything is found")
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    if not args.path.is_file():
        print(f"No such file: {args.path}", file=sys.stderr)
        return 2

    raw = args.path.read_text(encoding="utf-8", errors="replace")
    text = clean_source(raw, args.path.suffix.lower())

    groups = list(DEFAULT_TERM_GROUPS)
    for spec in args.terms:
        variants = tuple(v.strip() for v in spec.split("=") if v.strip())
        if len(variants) >= 2:
            groups.append(variants)

    skip = set(DEFAULT_ACRONYM_SKIP) | {w.upper() for w in args.ignore}

    findings = (
        check_acronyms(text, skip)
        + check_terms(text, groups)
        + check_sentences(text)
        + check_absolutes(text)
        + check_math_in_prose(text)
        + check_float_order(text)
        + check_significance(text)
        + check_connectors(text)
    )
    topics = collect_topic_sentences(text) if args.topic_sentences else None

    if args.json:
        print(json.dumps({"file": str(args.path), "findings": findings, "topic_sentences": topics},
                         ensure_ascii=False, indent=2))
    else:
        print(render_text(args.path, findings, topics))

    return 1 if (args.strict and findings) else 0


if __name__ == "__main__":
    sys.exit(main())
