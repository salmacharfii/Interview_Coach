
from pydantic import Field, ConfigDict,BaseModel
from typing import Literal

#Plan_Interview
class PlannedQuestion(BaseModel):
    model_config = ConfigDict(extra="forbid")
    competency: str = Field(description="The competency this question tests")
    why_it_matters: str = Field(description="One sentence linking it to the job")
    question_type: Literal["behavioral", "hypothetical", "technical"]
    question: str
    follow_ups: list[str] = Field(description="Exactly 2 follow-up probes")
    poor_answer: str
    solid_answer: str
    outstanding_answer: str

class InterviewPlan(BaseModel):
    model_config = ConfigDict(extra="forbid")
    role_summary: str
    seniority: Literal["junior", "mid", "senior", "lead"]
    questions: list[PlannedQuestion]

#Interview_turn
class InterviewerTurn(BaseModel):
    message: str = Field(description="What the interviewer says to the candidate")
    question_number: int = Field(description="Which main question (1-5) this turn belongs to")
    is_follow_up: bool
    finished: bool = Field(description="True only when the interview is over")


#Interview_feedback
class QuestionScore(BaseModel):
    competency: str
    score: int = Field(description="1 to 5, against the plan's anchors")
    evidence_quote: str = Field(description="The candidate's exact words")
    justification: str

class Point(BaseModel):
    point: str
    quote: str = Field(description="The candidate's exact words")

class Weakness(Point):
    improvement: str
    better_answer_example: str

class InterviewFeedback(BaseModel):
    scores: list[QuestionScore]
    strengths: list[Point]
    weaknesses: list[Weakness]

#Review_CV
class Finding(BaseModel):
    issue: str
    quote: str = Field(description="Exact CV text; empty if something is missing")
    suggestion: str

class CVReview(BaseModel):
    verdict: str = Field(description="Two sentences on how well this CV fits the role")
    content: list[Finding]
    clarity: list[Finding]
    formatting: list[Finding]
    errors: list[Finding]
    skills_present: list[str]
    skills_missing: list[str]
    top_improvements: list[str] = Field(description="Max 5, most impactful first")