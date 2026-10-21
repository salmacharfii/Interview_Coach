import io
import re
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

from prompts import CV_REVIEW_PROMPT, PDF_NOTE
from schemas import CVReview

def review_cv(role: str, job_description: str, cv_text: str, source: str = "paste") -> CVReview:
    instructions = CV_REVIEW_PROMPT + (PDF_NOTE if source == "pdf" else "")
    user_input = (
        f"<role>{role}</role>\n"
        f"<job_description>{job_description or 'Not provided'}</job_description>\n"
        f"<cv>{cv_text}</cv>"
    )
    response = client.responses.parse(
        model="gpt-6-luna",
        instructions=instructions,
        input=user_input,
        text_format=CVReview,
    )
    return response.output_parsed

import pdfplumber


def compact_whitespace(text: str) -> str:
    """Shrink the padding that layout extraction adds. Indentation is kept in
    proportion (a quarter of the width) and gaps inside a line become 3 spaces,
    so the tidy step can still tell the columns apart."""
    lines = []
    for line in text.splitlines():
        body = line.lstrip(" ")
        if not body.strip():
            lines.append("")
            continue
        indent = " " * ((len(line) - len(body)) // 4)
        lines.append(indent + re.sub(r" {3,}", "   ", body).rstrip())
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip("\n")


def non_whitespace_length(text: str) -> int:
    return len(re.sub(r"\s", "", text))

def extract_cv_text(file_bytes: bytes) -> str:
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            pages = [p.extract_text(layout=True) or "" for p in pdf.pages]
    except Exception:
        raise ValueError(
            "We couldn't open this file. Make sure it's a PDF that isn't damaged "
            "or password-protected, or paste your CV as text instead."
        ) from None
    text = compact_whitespace("\n".join(pages))
    if len(text) < 100:
        raise ValueError(
            "We couldn't read text from this PDF. If it's a scanned document, "
            "please paste your CV as text instead."
        )
    return text

from prompts import TIDY_CV_PROMPT
from schemas import CVSections

def tidy_cv(cv_text: str) -> CVSections:
    response = client.responses.parse(
        model="gpt-6-luna",
        instructions=TIDY_CV_PROMPT,
        input=f"<cv>{cv_text}</cv>",
        text_format=CVSections,
    )
    return response.output_parsed

from prompts import JOB_FIT_PROMPT
from schemas import JobFit

POINTS = {"met": 1, "partly": 0.5, "missing": 0}

def job_fit(job_description: str, cv_text: str) -> JobFit:
    response = client.responses.parse(
        model="gpt-6-luna",
        instructions=JOB_FIT_PROMPT,
        input=f"<job_description>{job_description}</job_description>\n<cv>{cv_text}</cv>",
        text_format=JobFit,
    )
    return response.output_parsed

def match_score(fit: JobFit) -> int:
    """The score is counted in code, so the same answers always give the same number."""
    if not fit.requirements:
        return 0
    points = sum(POINTS[r.status] for r in fit.requirements)
    return round(points / len(fit.requirements) * 100)

from prompts import JUDGE_PROMPT
from schemas import ReviewJudgement

def judge_review(role: str, cv_text: str, review: CVReview) -> ReviewJudgement:
    response = client.responses.parse(
        model="gpt-6-luna",
        instructions=JUDGE_PROMPT,
        input=(
            f"<role>{role}</role>\n"
            f"<cv>{cv_text}</cv>\n"
            f"<review>{review.model_dump_json()}</review>"
        ),
        text_format=ReviewJudgement,
    )
    return response.output_parsed