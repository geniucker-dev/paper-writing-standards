---
name: paper-writing-standards
description: Draft or audit a research manuscript against a concrete set of paper-writing standards: the 5W narrative spine (Why → How → What → So what), first-use definition and whole-paper consistency of acronyms, terminology and notation, short-sentence style, an experiments section built on strong external baselines, hard rules for figures, tables and equations, and section-by-section guidance from Abstract to References. Two modes: draft-to-standard, and audit that returns a numbered issue list with drop-in replacement sentences. Use when writing, restructuring, or reviewing a paper, thesis chapter, or single section; when checking acronym definitions, notation consistency, sentence length, baseline strength, figure captions, or reference style; or when the user mentions paper writing, manuscript audit, submission check, contribution list, 论文写作、写论文、改论文、论文规范、论文自检、投稿前检查、审稿自查、写摘要/引言/方法/实验/结论、术语统一、符号定义、图表规范、baseline 对比、贡献怎么写.
version: 1.0.0
license: MIT
---

# Paper Writing Standards

This skill turns one specific set of paper-writing standards into executable steps: decide the mode first, then either write along the spine or check against the list.

The standards come in two parts — **common writing problems** and **section-by-section guidance**. Full detail lives in `references/`; this file keeps only what every job needs. **Do not apply the standards from memory. Read the matching reference file from disk when you need the detail.**

Reply in the language the user writes in. The manuscript prose itself is normally English unless the user says otherwise.

## Step 1: Pick the mode

| What the user gives you | Mode |
| --- | --- |
| Ideas, results, figures, notes, or a Chinese draft, with a request to write or rewrite a section | **Draft mode** |
| Finished prose, a section, a full manuscript, a `.tex`/`.md` file, with a request to check it | **Audit mode** |
| A paragraph plus "make this better" | Audit first, then rewrite from the audit findings |

Before starting, state the detected mode and scope in one line (which sections, which language) so the user can correct you cheaply.

When information is missing, write a placeholder and list it under "Open questions for the author". **Never invent data, baseline numbers, or citations.**

## The four rules that always apply

Follow these in draft mode; check every one of them in audit mode.

### 1. The narrative spine is 5W

The whole paper follows **Why → How → What → So what**. Section mapping: Introduction and Related Work carry Why, Method carries How, Experiments carries What result, Conclusion carries So what.

The expanded version, the 5W breakdown of an abstract, and the three-tier contribution structure are in [references/5w-framework.md](references/5w-framework.md).

### 2. Paragraphs are topic-sentence-first

Each paragraph opens with a topic sentence and the rest of the paragraph develops it. Across sentences, keep the old-information-to-new-information flow so each sentence hands off to the next. Causal and contrastive relations between sentences must be explicit and correct.

Test: **cover everything in a paragraph except its first sentence — a reader should still know what the paragraph is about.**

### 3. Terminology and notation: define once, stay consistent

- Every acronym, technical term, symbol, and model name gets its full form plus a short gloss at first use.
- One concept, one English wording throughout (pick either `power grid` or `power network`, never both).
- Symbols in the prose must match symbols in the equations, and a symbol's meaning must not change between sections.
- Do not use the math symbol `+` in running prose — write "and". Do not coin ad-hoc acronyms in prose.

Naming conventions, the two ways to introduce variables (a notation table versus at first use), and how to verify a technical term is real English are in [references/common-pitfalls.md](references/common-pitfalls.md).

### 4. Sentences: accuracy first, short sentences preferred

- One sentence carries one point. Avoid more than one subordinate clause.
- Split long sentences. Avoid stacked parentheticals and strings of three or four commas.
- **Lead with the subject.** Avoid piled-up modifiers such as "under the setting in which, by X, the Y that was Z-ed…"; name the agent of the action.
- **Avoid absolutes.** Replace *the key* / *the only* with *one key factor* / *one plausible explanation*.
- **Choose connectives by function:** addition — Moreover / Additionally; escalation — Furthermore; cause — Therefore / Thus; contrast — However / Nevertheless. Rotate lightly within a function.

## Draft mode

Work through these in order. Do not skip step 2 and jump straight to finished prose.

1. **Locate.** Which part of the 5W does this section carry? Write out that question explicitly, e.g. Method = "How: why does this design solve the difficulty raised earlier?"
2. **Build the skeleton.** Write only the topic sentence of each paragraph and hand the list to the user for confirmation. A wrong skeleton wastes everything downstream.
3. **Load the section rules.** Read the matching part of [references/section-guide.md](references/section-guide.md) and confirm the required elements and the prohibitions — especially the four-move abstract, the five-step introduction, the Method subsection order, and the five dimensions of Experiments.
4. **Write.** Fill in the skeleton. Maintain a terminology and notation ledger as you go (concept → chosen wording → where it is first defined).
5. **Self-check.** Run the final checklist below over what you just wrote, then deliver.

## Audit mode

1. **Read once and triage.** Identify the single most damaging problem first. It is usually structural — no topic sentences, no strong baseline, vague contributions — not grammatical. Do not open with grammar nits.
2. **Run the mechanical checks** (optional but recommended, see below) to get candidate lists of undefined acronyms, long sentences, inconsistent terms, and float ordering.
3. **Walk the failure-mode table.** Read the "Common failure modes" table at the end of [references/common-pitfalls.md](references/common-pitfalls.md) and check symptom by symptom.
4. **Walk the sections.** Read [references/section-guide.md](references/section-guide.md) and check each section for missing required elements and for prohibited moves.
5. **Report** using the template below.

### Audit report template

```markdown
## Verdict
<One sentence: what must be fixed first in this manuscript, and why>

## Must fix (a reviewer will challenge this)
- **[section / line / quoted fragment]** symptom → fix
  > Replace with: <a sentence the author can paste directly>

## Should fix
- **[location]** symptom → fix

## Terminology and notation ledger
| Concept | Wordings found in the draft | Unify to | First defined at |
| --- | --- | --- | --- |

## Open questions for the author
- <missing data, baseline settings, reproducibility details>
```

Every finding needs a **drop-in replacement**. "Consider rephrasing" is not a finding.

## Mechanical checks

`scripts/audit_manuscript.py` uses only the Python standard library and checks `.tex` / `.md` / `.txt` for the mechanically decidable problems: undefined acronyms, over-long sentences, inconsistent terminology, float and equation numbering order, absolute wording, and math symbols in prose.

```bash
python3 scripts/audit_manuscript.py paper.tex
python3 scripts/audit_manuscript.py paper.tex --terms "power grid=power network" "case embedding=case conditioning"
python3 scripts/audit_manuscript.py paper.tex --topic-sentences
python3 scripts/audit_manuscript.py paper.tex --json
```

The script reports candidates; **the judgement stays with you**. It does not know which acronyms are common knowledge in the field (CNN, GPU), and it does not know whether a long sentence is actually justified. Treat the output as scan results, not as findings to relay verbatim.

## Final checklist

Confirm every line before delivering any section:

- [ ] Every paragraph opens with a topic sentence that survives covering the rest of the paragraph
- [ ] The 5W chain is complete: Why has a real pain point, How has a novelty, What has numbers, So what has boundaries
- [ ] Every acronym, term, and symbol is defined at first use; prose symbols match equation symbols
- [ ] One concept, one wording, throughout
- [ ] No sentence with three or more subordinate clauses; no strings of three or four commas
- [ ] No *the key* / *the only* / *first to propose* style absolutes
- [ ] The main experiment compares head-to-head against classical and recent methods, not only against your own variants
- [ ] Floats are numbered in order of first citation, cited before they appear, captions readable standalone, axes carry units
- [ ] Contributions are verifiable, reproducible, and comparable, and each one has matching evidence in the experiments
- [ ] The conclusion introduces no new method or data
- [ ] Reference style is uniform and every citation supports a specific statement in the text

## Reference files

Load on demand; do not read them all at once.

| File | When to read it |
| --- | --- |
| [references/common-pitfalls.md](references/common-pitfalls.md) | Working on terminology, notation, sentence style, the experiment spine, or float rules. Required in audit mode for the failure-mode table at the end. |
| [references/section-guide.md](references/section-guide.md) | Writing or checking any specific section. |
| [references/5w-framework.md](references/5w-framework.md) | Structuring the whole paper, writing the abstract or the contribution list, or taking notes while reading related work. |
