"""Check the judge notices a wrong quote. Usage: python judge_tamper.py"""
import cv_review

ROLE = "Junior UX/UI designer"
cv_text = open("test_cvs/cv_marta.txt", encoding="utf-8").read()
review = cv_review.review_cv(ROLE, "", cv_text)

honest = cv_review.judge_review(ROLE, cv_text, review)

# Swap the first quote for a sentence that is not in the CV
fake = review.model_copy(deep=True)
target = (fake.clarity or fake.content)[0]
original_quote = target.quote
target.quote = "Led a team of 12 designers at Google"
tampered = cv_review.judge_review(ROLE, cv_text, fake)

print("Planted quote replaced:", repr(original_quote))
print("accuracy, honest review:  ", honest.accuracy.score)
print("accuracy, tampered review:", tampered.accuracy.score, "-", tampered.accuracy.justification)