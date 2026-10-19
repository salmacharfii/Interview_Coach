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