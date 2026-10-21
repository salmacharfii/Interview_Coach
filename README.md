## Review quality (LLM-as-a-Judge)

A second model call audits each CV review on four criteria (1–5): accuracy (quotes exist in the CV, nothing invented), relevance to the role, actionability and completeness. We ran it on 5 made-up CVs for a Junior UX/UI designer role, including one in Spanish.

| CV | accuracy | relevance | actionability | completeness |
|---|---|---|---|---|
| cv_aisha | 4 | 5 | 4 | 5 |
| cv_lucia | 5 | 5 | 5 | 5 |
| cv_lukas | 2 | 5 | 4 | 5 |
| cv_marta | 5 | 5 | 5 | 5 |
| cv_tom | 4 | 5 | 5 | 5 |
| **average** | 4.0 | 5.0 | 4.6 | 5.0 |

**Testing the judge.** We replaced one quote in a review with a sentence that isn't in the CV ("Led a team of 12 designers at Google"). Accuracy dropped from 5 to 2 and the judge named the invented quote.

**What it found.** The lowest score (Lukas, accuracy 2) came from a rewritten bullet that added "after launch", a detail the CV doesn't state. Other deductions: a quote shortened with "...", and a skill inferred rather than stated. We tightened the review prompt in response.

**Limits.** One run, 5 CVs, and the same model family writes and judges the reviews, so scores may be lenient. Relevance scored 5 everywhere and doesn't separate reviews.