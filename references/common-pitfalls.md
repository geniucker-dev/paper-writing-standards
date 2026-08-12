# Common Writing Problems

Part one of the standards: five recurring problems plus the failure-mode table at the end. In audit mode, walk every item.

## 1. Define nouns and symbols at first use, acronyms included

Acronyms (AC-OPF), technical terms (hosting capacity), symbols, and model names all need their full form plus a short gloss the first time they appear:

> Alternating Current Optimal Power Flow (AC-OPF), abbreviated AC-OPF below.

**Two ways to introduce variables.** One is a notation table at the front of the paper listing what each variable means — common in journal papers, rare in conference papers. Conference papers normally define each variable at first use.

**Where the definition goes.** At the point of first appearance. If the variable comes from an equation, explain every new symbol in the same paragraph as that equation.

> Audit question: read from the top and stop at the first uppercase acronym, the first Greek letter, and the first subscripted variable. At each stop, ask whether the reader already knows what it is.

## 2. Terminology must be conventional, accurate, and consistent

Pick the conventional, authoritative English wording and use exactly one of them throughout: either `power grid` or `power network`, never both; never mix `case embedding` with `case conditioning`.

Do not translate technical terms literally from Chinese. If you are unsure of a term, translate it with an LLM first, then search it on Google or in a dictionary tool to check whether real sentences use it. If it barely appears anywhere, do not use it. If no established term exists, just spell the meaning out in plain English.

**Naming conventions.** Give variables meaningful subscripts and superscripts. Keep English terms lowercase and hyphenated, in one form throughout.

**Also:**

- Do not use the math symbol `+` in running prose — write "and".
- Do not coin ad-hoc acronyms in prose.
- A symbol's meaning must not change between sections.
- Symbols in the prose must match symbols in the equations.

> How to make this stick: maintain a terminology ledger while drafting (concept → chosen wording → where first defined), and use it for a find-and-replace pass before delivery.

## 3. Sentence style: accuracy first, short sentences preferred

- One sentence carries one point. Avoid more than one subordinate clause.
- Split long sentences and prefer short ones. Avoid stacked parentheticals, which fracture the sentence, and avoid strings of three or four commas.
- **Lead with the subject.** Avoid piled-up modifiers such as "under the setting in which, by X, the Y that was Z-ed…"; name the agent of the action.
- **Avoid absolutes.** Replace *the key* / *the only* with *one key factor* / *one plausible explanation*.
- **Choose connectives by function:** addition — Moreover / Additionally; escalation — Furthermore; cause — Therefore / Thus; contrast — However / Nevertheless. Rotate lightly within a function.

## 4. The experiment spine comes first

Head-to-head comparison against classical methods and recent methods as baselines is the core of your argument. Ablations and sensitivity analyses supplement that comparison; they do not replace it.

Do not benchmark only against your own variants. A paper built that way has ablations and parameter sweeps but no main experiment.

> Audit question: delete every ablation and parameter sweep. Do the remaining tables still show the method works? If not, the main experiment is missing.

## 5. Hard requirements for figures, tables, and equations

- **Numbering and citation.** Figure 1, Table 1, Eq. (1). Number them in order of first citation in the text.
- **Captions and units.** A caption must be readable on its own, away from the body text. Axes carry units and dimensions.
- **Multi-panel figures.** Panels (a)(b)(c) need the dimension they are aligned on stated explicitly in the caption.

## Common failure modes

| Symptom | How it shows up | Fix |
| --- | --- | --- |
| Undefined acronym or symbol | AC-OPF, KKT, λ appear out of nowhere | Give the full form and definition at first use; explain symbols in the same paragraph |
| Inconsistent terminology | grid/network mixed; case embedding/conditioning mixed | Pick one, replace throughout, and keep a terminology table |
| Paragraph without a topic sentence | The reader cannot tell what the paragraph is about | Make the first sentence state the conclusion or core message of that paragraph |
| Over-long sentences | Three or more subordinate clauses, comma chains | Split them; enforce one point per sentence |
| No strong baseline | Only ablations and self-comparison | Add community-accepted baselines; report the comparison under a single consistent protocol |
| Caption too thin | The reader cannot read the figure without the body text | Put variables, units, sample size, and statistical method in the caption |
| Equations detached from prose | New symbols appear in an equation and are never explained | Follow every equation immediately with a paragraph defining its new symbols |

The original table image is at [../assets/common-error-table.png](../assets/common-error-table.png).
