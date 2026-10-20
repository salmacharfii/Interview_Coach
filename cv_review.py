import io
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

from prompts import CV_REVIEW_PROMPT
from schemas import CVReview

def review_cv(role: str, job_description: str, cv_text: str) -> CVReview:
    user_input = (
        f"<role>{role}</role>\n"
        f"<job_description>{job_description or 'Not provided'}</job_description>\n"
        f"<cv>{cv_text}</cv>"
    )
    response = client.responses.parse(
        model="gpt-6-luna",
        instructions=CV_REVIEW_PROMPT,
        input=user_input,
        text_format=CVReview,
    )
    return response.output_parsed

import pdfplumber

def extract_cv_text(file_bytes: bytes) -> str:
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        pages = [p.extract_text(layout=True) or "" for p in pdf.pages]
    text = "\n".join(pages).strip()
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