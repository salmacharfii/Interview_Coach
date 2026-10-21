
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
    model_config = ConfigDict(extra="forbid")
    message: str = Field(description="What the interviewer says to the candidate")
    question_number: int = Field(description="Which main question (1-5) this turn belongs to")
    is_follow_up: bool
    finished: bool = Field(description="True only when the interview is over")


#Interview_feedback
class QuestionScore(BaseModel):
    model_config = ConfigDict(extra="forbid")
    competency: str
    asked: bool = Field(description="True only if the interviewer actually asked this question")
    score: int | None = Field(description="1 to 5 against the plan's anchors; null if not asked")
    evidence_quote: str = Field(description="The candidate's exact words; empty if there is no usable answer")
    justification: str

class Point(BaseModel):
    model_config = ConfigDict(extra="forbid")
    point: str
    quote: str = Field(description="The candidate's exact words")

class Weakness(Point):
    model_config = ConfigDict(extra="forbid")
    improvement: str
    better_answer_example: str

class InterviewFeedback(BaseModel):
    model_config = ConfigDict(extra="forbid")
    scores: list[QuestionScore]
    strengths: list[Point]
    weaknesses: list[Weakness]

#Review_CV
class Finding(BaseModel):
    model_config = ConfigDict(extra="forbid")
    issue: str
    quote: str = Field(description="Exact CV text; empty if something is missing")
    suggestion: str

class CVReview(BaseModel):
    model_config = ConfigDict(extra="forbid")
    verdict: str = Field(description="Two sentences on how well this CV fits the role")
    content: list[Finding]
    clarity: list[Finding]
    formatting: list[Finding]
    errors: list[Finding]
    skills_present: list[str] = Field(description="Short skill names, 1 to 4 words each")
    skills_missing: list[str] = Field(description="Short skill names, 1 to 4 words each")
    top_improvements: list[str] = Field(description="Max 5, most impactful first")

class CVSections(BaseModel):
    model_config = ConfigDict(extra="forbid")
    contact: str
    summary: str
    experience: str
    education: str
    skills: str
    languages: str
    other: str = Field(description="Anything that fits no other section")

#Job_fit
class Requirement(BaseModel):
    model_config = ConfigDict(extra="forbid")
    requirement: str = Field(description="One requirement from the job description, in a few words")
    status: Literal["met", "partly", "missing"]
    evidence: str = Field(description="Exact CV text that shows it; empty if missing")
    how_to_close: str = Field(description="One concrete action to close the gap; empty if met")

class JobFit(BaseModel):
    model_config = ConfigDict(extra="forbid")
    summary: str = Field(description="Two sentences on how well this CV fits this job")
    requirements: list[Requirement] = Field(description="At most 10, most important first")