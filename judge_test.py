"""Run the CV reviewer and the judge on every CV in test_cvs/ and print a table.
Usage: python judge_test.py"""
from pathlib import Path
import cv_review

ROLE = "Junior UX/UI designer"
CRITERIA = ["accuracy", "relevance", "actionability", "completeness"]

rows = []
for path in sorted(Path("test_cvs").glob("*.txt")):
    cv_text = path.read_text(encoding="utf-8")   # always UTF-8, on every computer
    review = cv_review.review_cv(ROLE, "", cv_text)
    verdict = cv_review.judge_review(ROLE, cv_text, review)
    scores = [getattr(verdict, c).score for c in CRITERIA]
    rows.append((path.stem, scores))
    print(f"{path.stem}: {scores}")
    for c in CRITERIA:
        print(f"   {c}: {getattr(verdict, c).justification}")

# Markdown table to paste into the README
print("\n| CV | " + " | ".join(CRITERIA) + " |")
print("|---" * (len(CRITERIA) + 1) + "|")
for name, scores in rows:
    print(f"| {name} | " + " | ".join(str(s) for s in scores) + " |")
averages = [round(sum(s[i] for _, s in rows) / len(rows), 1) for i in range(len(CRITERIA))]
print("| **average** | " + " | ".join(str(a) for a in averages) + " |")