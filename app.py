from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

import interview
from schemas import InterviewPlan

app = FastAPI()


class StartRequest(BaseModel):
    role: str
    job_description: str = ""


class TurnRequest(BaseModel):
    role: str
    plan: InterviewPlan
    history: list[dict]


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


from fastapi import File, HTTPException, UploadFile

import cv_review

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
        return {"cv_text": cv_review.extract_cv_text(await file.read())}
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

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