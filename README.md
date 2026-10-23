# margin

**Get ready for your next job.** margin is an AI career coach. It runs a mock interview or reviews your CV for the role you want, and every note quotes your own words.

**Live:** https://interview-coach-margin.vercel.app/

Ironhack AI Engineering bootcamp, Project 2: AI-Powered Career Coach. Built by Joey and Salma.

## What it does

One journey in four steps, the same for both modes:

1. **Brief:** the role you want and, if you have it, the job description.
2. **Rehearse**
   - **Mock interview:** five questions planned for the role, asked one at a time, with follow-ups when an answer is vague. You can type or speak your answers.
   - **CV review:** upload a PDF or paste the text. You check the sections before the review runs.
3. **Debrief**
   - **Interview:** a 1–5 score per skill, the quote it's based on, what to fix and a stronger version of the answer.
   - **CV:** notes on content, clarity, format, errors and skills. With a job description you also get a job-fit score and a skills gap.
4. **Next steps:** the top actions to take before you apply, ready to copy or download.

## How it works

- **Backend:** FastAPI, deployed on Vercel.
- **Frontend:** a single HTML page (`static/index.html`) with vanilla JavaScript. The session lives in the browser, and nothing is stored on the server.
- **AI:** the OpenAI Responses API. One model plays several roles, each with its own prompt in `prompts.py`:
  - **Planner:** picks five skills for the role and writes what a poor, solid and outstanding answer looks like.
  - **Interviewer:** asks one question at a time and decides when to follow up.
  - **Evaluator:** scores each skill against the planner's anchors and quotes the answer.
  - **CV reviewer, section sorter and job-fit checker:** review the CV and match it to the job description.
  - **Judge:** audits CV reviews for quality (see below).
- **Structured outputs:** every model reply is parsed into a Pydantic schema (`schemas.py`), so the page always gets valid JSON.
- **Job-fit score:** calculated in code from met, partly met and missing requirements, so the same CV always gets the same number.
- **Voice input:** the browser's own speech recognition (Web Speech API). It works in Chrome, Edge and Safari; in Firefox the mic button is hidden.

### API

| Method | Path | What it does |
|---|---|---|
| GET | `/` | Serves the page |
| GET | `/health` | Health check |
| POST | `/interview/start` | Plans the interview and asks the first question |
| POST | `/interview/turn` | Takes an answer and returns the next question or a follow-up |
| POST | `/interview/feedback` | Scores the interview |
| POST | `/cv/extract` | Reads a PDF (max 4 MB) and sorts it into sections |
| POST | `/cv/review` | Reviews the CV |
| POST | `/cv/fit` | Scores the CV against the job description |

## Run it locally

You need Python 3 and an OpenAI API key.

```bash
python -m venv .venv
```
```bash
source .venv/bin/activate
```
```bash
pip install -r requirements.txt
```

Create a `.env` file with your key:

```
OPENAI_API_KEY=sk-...
```

Start the server and open http://127.0.0.1:8000:

```bash
uvicorn app:app --reload
```

## Privacy

What you type or say is sent to OpenAI to write your feedback; margin doesn't save it. Voice input is transcribed by your browser's speech service (Google in Chrome, Apple in Safari).

## Files

| File | Purpose |
|---|---|
| `app.py` | FastAPI routes, size limits and error handling |
| `interview.py` | Planner, interviewer and evaluator calls |
| `cv_review.py` | PDF sorting, CV review, job fit and judge calls |
| `prompts.py` | All system prompts |
| `schemas.py` | Pydantic models for every structured output |
| `static/index.html` | The whole interface |
| `judge_test.py` | Runs the judge on every CV in `test_cvs/` |
| `judge_tamper.py` | Plants a fake quote to check that the judge catches it |
| `test_cvs/` | Five made-up CVs used for evaluation |

## Review quality (LLM-as-a-Judge)

A second model call audits each CV review on four criteria (1–5): accuracy (quotes exist in the CV, nothing invented), relevance to the role, actionability and completeness. We ran it on 5 made-up CVs for a Junior UX/UI designer role, including one in Spanish.

| CV | accuracy | relevance | actionability | completeness |
|---|---|---|---|---|
| cv_aisha | 4 | 5 | 4 | 5 |
| cv_lucia | 5 | 5 | 5 | 5 |
| cv_lukas | 2 | 5 | 4 | 5 |
| cv_marta | 5 | 5 | 5 | 5 |
| cv_tom | 4 | 5 | 5 | 5 |
| **average** | 4.0 | 5.0 | 4.6 | 5.0 |

**Testing the judge.** We replaced one quote in a review with a sentence that isn't in the CV ("Led a team of 12 designers at Google"). Accuracy dropped from 5 to 2 and the judge named the invented quote.

**What it found.** The lowest score (Lukas, accuracy 2) came from a rewritten bullet that added "after launch", a detail the CV doesn't state. Other deductions: a quote shortened with "...", and a skill inferred rather than stated. We tightened the review prompt in response.

**Limits.** One run, 5 CVs, and the same model family writes and judges the reviews, so scores may be lenient. Relevance scored 5 everywhere and doesn't separate reviews.