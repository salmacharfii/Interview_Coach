from openai import OpenAI
from schemas import InterviewPlan
from prompts import PLANNER_PROMPT

client = OpenAI()

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