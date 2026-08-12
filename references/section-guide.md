# Section-by-Section Guidance

Part two of the standards. Read the matching subsection when writing a section; in audit mode, check each section for missing required elements and prohibited moves.

## The narrative spine must be visible

Follow **Why → How → What → So what** (the 5W spine).

Paragraphs are topic-sentence-first: the opening sentence states the point, the rest develops it. Across sentences, keep the old-information-to-new-information flow so each sentence hands off to the next.

Causal and contrastive relations between sentences must be explicit and used correctly.

## 1. Abstract

**Moves:** one sentence on problem and background → one sentence on method → two or three core results, including order-of-magnitude comparisons → one sentence on significance.

**Prohibited:** piling up technical detail, over-claiming, and introducing any conclusion that the body does not support.

## 2. Introduction

**Logic:** real-world need or pain point → existing methods and their shortcomings → this paper's angle → contribution list, one to three items, nothing vague → a preview of results, ideally a figure or a number.

**Technique:** contributions must be verifiable, reproducible, and comparable. Avoid *first / first-ever / first to propose*; write "to the best of our knowledge, X has not been systematically addressed in the setting of Y" instead.

> The introduction is essentially a long-form abstract. The three-tier contribution structure is in [5w-framework.md](5w-framework.md).

## 3. Related Work

Organize by problem dimension, not as a paper-by-paper roll call of authors. Present the differences as a comparison table or as thematic subsections: data, assumptions, model, computational cost, interpretability.

End with a sentence that hands off naturally to your method.

> Warning sign: consecutive sentences of the form "X et al. proposed…; Y et al. proposed…". That is a list, not a problem-dimension analysis.

## 4. Method / Model

Open with the overall block diagram and data flow (Figure 1): input → encoding → core mechanism → output and loss.

Define symbols in the paragraph next to their equation. Do not hide a "Notation" section at the end of the paper.

**Suggested subsection order:**

1. Problem formulation — variables, objective, constraints and assumptions
2. Model architecture — modular breakdown: encoder, message passing, conditioning, heads
3. Training objective and optimization — loss, regularization, complexity
4. Implementation details — important hyperparameters, stabilization tricks

## 5. Experiments

**Comparison targets.** Cover simple strong baselines, plus methods the community widely accepts as classical (logistic regression, MLP, classical algorithms) and the latest or best-performing (SOTA) methods.

**Metrics and protocol.** State the data split, number of repeats and training epochs, evaluation scripts, significance testing, and what the confidence intervals or error bars mean.

**Ablations and cost.** Pair each module's gain with its time, parameter-count, and memory cost. Answer "is it worth it?".

**Reproducibility.** Seeds, hardware, key hyperparameters, scripts and repository if they can be released. State where each implementation came from (official code or your reimplementation) and confirm the settings are uniform.

**Robustness and generalization.** Across datasets, across scenarios, across random seeds. Report failure cases and boundaries.

## 6. Results & Discussion

**Figures and tables are about information density and readability:**

- One figure, one message. Panels (a)(b)(c) placed side by side must be aligned on the same dimension.
- Explain axes, units, and abbreviations in the caption or inside the figure.
- Cite before showing: "as shown in Figure 3…" comes first, the figure follows.

**The discussion must answer "why":** the mechanism, the boundary conditions, the failure cases, and the sources of error.

## 7. Conclusion

Return to the problem statement and the contributions. Do not introduce new methods or new data in the conclusion. Limitations and future work are welcome, but make them specific rather than slogans.

## 8. References

- Uniform style: venue, pages, year, author order.
- Every citation supports a specific statement in the text. No decorative citations.
- When citing several references at once, use a range or a consistent list form, e.g. [5–8].
