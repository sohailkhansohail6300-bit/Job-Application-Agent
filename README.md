# Personal Job-Application Agent

This project is a local, human-in-the-loop job application assistant designed to help you manage the full job application lifecycle without submitting anything automatically. It analyzes a job description, scores how well it matches your profile, tailors your CV and cover letter using only facts from your master profile, answers job-application questions, validates claims before approval, and exports final documents for manual submission.

## Product goal

The system keeps a single source of truth in a master profile and refuses to fabricate experience or claims. Every generated document and answer is traceable back to that profile. The user must explicitly approve final output before export or application.

## Core principles

- Human approval is required before submission or export
- The master profile is the only source of truth
- Matching, tailoring, and validation are grounded in structured profile data
- The system supports manual job applications on Indeed and similar job boards
- LLM-generated content is optional and only used when an API key is available
- The validator blocks unsupported claims to reduce fabrication risk

## Feature highlights

- Job ingestion from an Indeed URL or copy-pasted job description
- Parsed job metadata extraction: skills, seniority, degree requirements, location, salary, and job title
- Match scoring from 0 to 100 against the user profile
- Tailored CV generation in DOCX and PDF format
- Cover letter generation in DOCX and PDF format
- Q&A generation for application forms
- Validation against the master profile before approval
- Exported application package with artifact tracking
- Application status tracking from job entry to interview and outcome

## Architecture summary

The implementation described in the provided specification is organized into these layers:

- `core/` — shared utilities, config, and path helpers
- `database/` — SQLite schema and repository queries
- `jobs/` — parsing and extraction of job requirements
- `agents/` — job matching, CV tailoring, cover letter generation, answer generation, and validation
- `documents/` — PDF and document generation
- `pages/` — Streamlit UI pages
- `profile/` — master profile YAML files
- `config/` — scoring and app configuration
- `artifacts/` — exported CV and cover-letter files

## Technology stack

- Python 3.10+
- Streamlit for the workflow UI
- SQLite for local application data
- YAML for profile storage
- `pydantic` / Python data processing utilities where applicable
- WeasyPrint for PDF rendering
- python-docx for DOCX export
- Optional LLM integration via Kimi / Moonshot API

## Setup

```bash
git clone <your-repo> job-agent
cd job-agent
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Edit `.env` and set the LLM API key if needed:

```env
KIMI_API_KEY=your_key_here
```

If no API key is configured, the app can still run in offline mode. Matching, CV tailoring, and validation continue to function, while LLM polishing of cover letters, summaries, and free-form Q&A is skipped.

## Configuration

The primary runtime config lives in `config/settings.yaml`.

This file controls match weights, thresholds, and scoring behavior. The project also expects a local profile file under `profile/master_profile.yaml`.

## Database initialization

The database is created automatically on first run using `database/schema.sql`.

To reset the database:

```bash
rm database/app.db
```

## Run the app

```bash
streamlit run app.py
```

## Workflow

1. Create or update your master profile
2. Add a job by URL or paste the description
3. Parse and analyze the job description
4. Score the job against your profile
5. Generate a tailored CV
6. Generate a cover letter
7. Answer application questions
8. Validate claims against the profile
9. Review the package manually
10. Approve export and apply manually
11. Track status through interviews, rejections, and offers

## Documented implementation stages

The provided implementation specification is structured into the following stages:

- Stage 1: core config, environment, paths, DB schema, repository layer
- Stage 2: job parsing and matcher scoring
- Stage 3: CV tailoring and answer logic
- Stage 4: validation and anti-fabrication safeguards
- Stage 5: document generation to DOCX and PDF
- Stage 6: Streamlit pages and interactive UI
- Stage 7: project README and usage documentation

## Security and trust model

The application is designed to minimize hallucination and misrepresentation:

- It stores a master profile as a grounded source of truth
- It enforces provenance tagging for generated bullets and statements
- It validates each claim before approval
- It blocks unsupported claims from export
- It asks for explicit user approval before any export or submission

## Directory structure

```text
job-agent/
├── app.py
├── README.md
├── requirements.txt
├── .env.example
├── config/
│   └── settings.yaml
├── core/
│   ├── paths.py
│   ├── utils.py
│   ├── llm.py
│   └── ...
├── database/
│   ├── schema.sql
│   └── repository.py
├── jobs/
│   └── job_parser.py
├── agents/
│   ├── job_matcher.py
│   ├── cv_tailor.py
│   ├── cover_letter.py
│   ├── answer_engine.py
│   └── validator.py
├── documents/
│   ├── pdf_generator.py
│   ├── cv_generator.py
│   └── cover_letter_generator.py
├── pages/
│   ├── 1_Dashboard.py
│   ├── 2_My_Profile.py
│   ├── 3_Add_Job.py
│   ├── 4_Job_Analysis.py
│   ├── 5_Tailored_Application.py
│   ├── 6_Review.py
│   └── 7_Application_Tracker.py
├── profile/
│   └── master_profile.yaml
├── artifacts/
└── .venv/
```

## Recommended operating model

Use the tool as a decision-support system rather than an autonomous job-application bot:

- Fill out your profile completely
- Review every generated CV and cover letter
- Resolve validator warnings and blocked claims before approval
- Apply manually through the original job board
- Track application outcomes in the tracker

## Support notes

This project is intended as a personal, privacy-focused workflow assistant. Since it uses local data and explicit user review, it is best suited for individual use and small-scale job search tracking rather than fully automated mass application workflows.
