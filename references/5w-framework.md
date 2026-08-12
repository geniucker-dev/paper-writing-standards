# The 5W Framework

The same framework is used both to read papers and to structure your own.

## The five questions

When reading a paper, track the 5W — What problem, Why, How, What results, So what:

1. **What Problem** — what problem is being solved
2. **Why** — background, difficulty, challenge
3. **How** — the method that solves it, the novelty
4. **What Results** — what the results are and how good they are
5. **So What** — how far this can be extended

## Where each W lands

**Title.** Usually gives you What Problem and How.

**Abstract.** Starts with What Problem and Why (background, difficulty), then How — the abstract must foreground the novelty, typically signalled with *We propose* — then What Results, where you give concrete numbers and the most striking advantage, and finally So What, which is the conclusion.

**Introduction.** Essentially a long-form abstract:

- First introduce the problem, why it matters, and where the difficulty is.
- Then cover how existing methods approach it and what they run into. Those two together are **What Problem and Why**.
- Then present your line of thinking — the paper's core idea, your analysis and observation of the problem — and let it lead into your method. That is **How**, and it must also explain why the method is a reasonable thing to do, which is again **Why**.

**Figures.** Traditionally the most important result figure goes last; the current trend in computer science is to put it up front to catch attention. When reading, look at the architecture figure first and the data tables second.

**Whole-paper structure** maps onto the 5W as well: Introduction and Related Work carry Why, Method carries How, Experiments carries What result, Conclusion carries So what.

## Writing the contributions

Novelty comes in three tiers:

| Tier | Type of novelty |
| --- | --- |
| First | Posing a new problem |
| Second | A new method |
| Third | A new result or a new setting |

Write the contribution list along that structure, usually three items: the new problem (the framework) first, then the new method, then the new results.

> Every contribution must have matching evidence in the experiments. Without it, the contribution is vague by definition.

The original notes image is at [../assets/5w-framework.png](../assets/5w-framework.png).
