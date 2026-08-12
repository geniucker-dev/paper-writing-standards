# paper-writing-standards

A cross-agent Agent Skill that turns one concrete set of paper-writing standards into an executable drafting workflow and an audit checklist.

The standards cover two parts: **common writing problems** (terminology and notation, sentence style, the experiment spine, figures and equations) and **section-by-section guidance** (Abstract through References), organized around the 5W narrative spine.

Plain Markdown plus a standard-library Python script, no agent-specific format. Cursor, Codex CLI, and Claude Code can all read it as-is.

[中文说明](README.zh-CN.md)

## What it does

**Draft mode** — give it ideas, results, or a rough draft. It locates the section on the 5W spine, proposes a topic-sentence skeleton for you to confirm, then fills it in against the section rules.

**Audit mode** — give it existing prose. It triages the most damaging problem first, runs the mechanical checks, walks the failure-mode table and the section requirements, and returns a numbered issue list where every finding carries a drop-in replacement sentence.

## Layout

```
paper-writing-standards/
├── SKILL.md                        # entry point: mode selection, the four always-on rules,
│                                   # both workflows, the final checklist
├── references/
│   ├── common-pitfalls.md          # common writing problems + the failure-mode table
│   ├── section-guide.md            # the eight sections
│   └── 5w-framework.md             # the 5W spine + three-tier contribution structure
├── scripts/
│   └── audit_manuscript.py         # mechanical checks, standard library only
└── assets/                         # source images for the standards
```

`SKILL.md` holds only what every job needs; detail is loaded from `references/` on demand.

## Install

Clone it, then place or symlink the directory into your agent's skills folder:

```bash
git clone https://github.com/GaAs9000/paper-writing-standards.git

# Cursor
ln -s "$PWD/paper-writing-standards" ~/.cursor/skills/paper-writing-standards

# Codex CLI
ln -s "$PWD/paper-writing-standards" ~/.codex/skills/paper-writing-standards

# Claude Code
ln -s "$PWD/paper-writing-standards" ~/.claude/skills/paper-writing-standards
```

`mkdir -p` the target directory first if it does not exist. Symlinking means all three share one copy and a single `git pull` updates everything.

If your agent already reads another agent's skills directory, install it once — a second copy shows up as a duplicate entry.

You can also skip installing entirely and paste `SKILL.md` into the conversation, or point the agent at the files.

## Use

Once installed, just ask normally and the agent will match it:

```
Check intro.tex against my paper writing standards
Turn these results into an Experiments section
Is my contribution list specific enough?
Do a submission pass over the whole paper
```

Chinese requests trigger it too — the skill description carries Chinese trigger phrases, and the agent replies in whichever language you write in. You can also name it explicitly: `use paper-writing-standards on paper.tex`.

## The mechanical checker

```bash
python3 scripts/audit_manuscript.py paper.tex
python3 scripts/audit_manuscript.py paper.tex --topic-sentences
python3 scripts/audit_manuscript.py paper.tex --terms "power grid=power network"
python3 scripts/audit_manuscript.py paper.tex --json
```

Handles `.tex` / `.md` / `.txt` and mixed English/Chinese text. Python 3.9+, standard library only. LaTeX comments, math environments, `\cite` and `\ref` are skipped automatically.

| Check | What it flags |
| --- | --- |
| Undefined acronyms | No full form or parenthetical definition at first use |
| Inconsistent terminology | One concept with several wordings; 13 built-in groups, extend with `--terms` |
| Over-long sentences | Over 40 words in English, over 90 characters in Chinese |
| Comma chains | 3+ commas in English, 4+ in Chinese |
| Too many clauses | 3+ subordinate clause markers in one sentence |
| Absolute wording | *the key*, *the only*, *for the first time*, 首次提出, and similar |
| Math symbols in prose | Standalone `+` `&` `=` |
| Float numbering order | Whether first-citation order runs 1, 2, 3… |
| Unsupported significance | *significant* with no p-value or confidence interval in the same sentence |
| Overused connectives | Budgeted against total word count |

Also: `--ignore` to skip specific acronyms, `--strict` to exit 1 on any finding, which makes it usable in CI or a pre-commit hook.

The script reports candidates and makes no judgements. It does not know which acronyms are common knowledge in your field, and it cannot tell whether a long sentence is justified. **Vague contributions, missing baselines, a discussion that never explains a mechanism, captions that fail to stand alone — those must be checked against `references/` by a human or a model.**

## Relationship to other writing skills

This is a self-contained set of standards and does not depend on any other skill. If you also have general-purpose polishing or figure skills installed, this one takes precedence: it is a specific group's written requirement, not generic advice.

## License

MIT
