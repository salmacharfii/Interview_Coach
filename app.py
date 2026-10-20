import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from openai import OpenAIError

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

import interview
from schemas import InterviewPlan
from fastapi import File, HTTPException, UploadFile
import cv_review

app = FastAPI()


class StartRequest(BaseModel):
    role: str
    job_description: str = ""


class TurnRequest(BaseModel):
    role: str
    plan: InterviewPlan
    history: list[dict]

logger = logging.getLogger("career_coach")


@app.exception_handler(OpenAIError)
async def openai_error(request: Request, exc: OpenAIError):
    logger.exception("OpenAI call failed on %s", request.url.path)
    return JSONResponse(
        status_code=502,
        content={"detail": "The AI didn't respond this time. Please try again."},
    )


@app.exception_handler(Exception)
async def unexpected_error(request: Request, exc: Exception):
    logger.exception("Unexpected error on %s", request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Something went wrong on our side. Please try again."},
    )

@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/interview/start")
def start(req: StartRequest):
    plan = interview.plan_interview(req.role, req.job_description)
    turn = interview.interviewer_turn(plan, req.role, [])
    return {"plan": plan, "turn": turn}


@app.post("/interview/turn")
def turn(req: TurnRequest):
    result = interview.interviewer_turn(req.plan, req.role, req.history)
    return {"turn": result}


@app.post("/interview/feedback")
def feedback(req: TurnRequest):
    fb = interview.interview_feedback(req.plan, req.history)
    overall = round(sum(s.score for s in fb.scores) / len(fb.scores), 1)
    return {"overall": overall, "feedback": fb}

class CVRequest(BaseModel):
    role: str
    job_description: str = ""
    cv_text: str


@app.post("/cv/review")
def review(req: CVRequest):
    if len(req.cv_text) > 20000:
        raise HTTPException(status_code=400, detail="That CV is too long. Please shorten it.")
    return {"review": cv_review.review_cv(req.role, req.job_description, req.cv_text)}


@app.post("/cv/extract")
async def extract(file: UploadFile = File(...)):
    try:
        raw = cv_review.extract_cv_text(await file.read())
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

    sections = cv_review.tidy_cv(raw)
    kept = sum(len(v) for v in sections.model_dump().values())
    return {
        "cv_text": raw,
        "sections": sections,
        "lost_content": kept < len(raw.replace(" ", "")) * 0.8,
    }