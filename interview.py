from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

from schemas import InterviewPlan
from prompts import PLANNER_PROMPT

def plan_interview(role: str, job_description: str) -> InterviewPlan:
    user_input = (
        f"<role>{role}</role>\n"
        f"<job_description>{job_description or 'Not provided'}</job_description>"
    )
    response = client.responses.parse(
        model="gpt-6-luna",
        instructions=PLANNER_PROMPT,
        input=user_input,
        text_format=InterviewPlan,
    )
    return response.output_parsed

from schemas import InterviewerTurn
from prompts import INTERVIEWER_PROMPT

def interviewer_turn(plan, role, history):
    messages = history or [
        {"role": "user", "content": "[start]"}
    ]
    response = client.responses.parse(
        model="gpt-6-luna",
        instructions=INTERVIEWER_PROMPT.format(role=role, plan=plan.model_dump_json()),
        input=messages,
        text_format=InterviewerTurn,
    )
    return response.output_parsed

from schemas import InterviewFeedback
from prompts import EVALUATOR_PROMPT

def interview_feedback(plan, history):
    transcript = "\n".join(
        f"{'Interviewer' if m['role'] == 'assistant' else 'Candidate'}: {m['content']}"
        for m in history
    )
    user_input = (
        f"<interview_plan>{plan.model_dump_json()}</interview_plan>\n"
        f"<transcript>{transcript}</transcript>"
    )
    response = client.responses.parse(
        model="gpt-6-luna",
        instructions=EVALUATOR_PROMPT,
        input=user_input,
        text_format=InterviewFeedback,
    )
    return response.output_parsed