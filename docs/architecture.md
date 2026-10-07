# Architecture Overview

This document describes the structure and responsibilities of the Personal Job-Application Agent as defined in the specification.

## 1. System overview

The application is a local, human-in-the-loop workflow built around a master profile and a per-job analysis pipeline. It reads a job description, compares it to the user profile, and produces an application package that can be reviewed and approved before export.

The design emphasizes three goals:

1. Maintain a single, trusted source of truth
2. Generate evidence-backed CV and application content
3. Keep the user in control of all final decisions

## 2. Layered architecture

### Core layer

The `core/` package contains foundational utilities used across the app:

- `core.paths` — resolves project-root-relative file paths
- `core.utils` — YAML loading/saving, sanitization, compatibility helpers
- `core.llm` — optional LLM integration for polishing and answer generation

This layer centralizes environment access and avoids duplicate path logic in the UI and agents.

### Configuration layer

The project uses `config/settings.yaml` to store scoring settings, thresholds, and match weights. This file allows the weighting model to be tuned without changing code logic.

### Data layer

The `database/` package manages all local state through SQLite:

- schema definition in `database/schema.sql`
- repository abstraction in `database/repository.py`

The repository is responsible for:

- storing job records
- tracking match status and analysis results
- storing generated application packages
- tracking application lifecycle states
- persisting artifacts and notes

### Job ingestion and parsing layer

The `jobs/` package extracts structured information from raw job description text.

`jobs/job_parser.py` performs the following:

- parse the raw job description text
- identify title, company, location, salary, and seniority
- extract required skills and degree requirements
- identify years of experience and preferred technology stacks
- produce a normalized structure used by the matcher

### Matching and tailoring layer

The `agents/` package contains the reasoning pipeline:

- `job_matcher.py` — computes score and reasoning for a job
- `cv_tailor.py` — rewrites and prioritizes CV bullets based on profile facts
- `cover_letter.py` — drafts cover letter content from profile and job context
- `answer_engine.py` — generates responses to application forms or screening questions
- `validator.py` — blocks unsupported or untraceable claims

This is the intelligence layer of the system. It transforms raw job data and profile facts into a tailored application package.

### Document generation layer

The `documents/` package generates exportable outputs:

- `pdf_generator.py` — Markdown to HTML to PDF conversion
- `cv_generator.py` — CV generation in DOCX and PDF
- `cover_letter_generator.py` — cover letter generation in DOCX and PDF

The system outputs versioned filenames based on the company and job title, with a timestamp.

### UI layer

The Streamlit app uses page modules under `pages/`:

- `app.py` — landing page and central workflow overview
- `1_Dashboard.py` — summary metrics and recent applications
- `2_My_Profile.py` — master profile editor
- `3_Add_Job.py` — job intake from URL or pasted text
- `4_Job_Analysis.py` — parse + score + tailor a job
- `5_Tailored_Application.py` — review and edit generated CV, cover letter, and Q&A
- `6_Review.py` — approve or reject candidate package
- `7_Application_Tracker.py` — pipeline tracking and follow-up management

These pages create a guided workflow while keeping the process transparent and human-controlled.

## 3. Data flow

The high-level data flow is as follows:

1. User populates `profile/master_profile.yaml`
2. User adds a job via URL or manual description
3. Application stores the job record in SQLite
4. Parser extracts structured requirements
5. Matcher computes a fit score against the profile
6. Tailoring engine builds a CV and cover letter
7. Answer engine generates personal responses for application questions
8. Validator checks each claim against the master profile
9. User reviews the generated package
10. User approves export or rejects the package
11. The application is tracked through follow-up and outcome states

## 4. Trust and validation model

The system intentionally implements a provenance-based design:

- profile facts are treated as authoritative
- generated bullets are traceable back to data entries
- validation logic flags unsupported claims
- blocked claims prevent approval
- the user remains responsible for final submission

This structure reduces the risk of fabricated detail while still allowing useful automation.

## 5. Key design decisions

### Human-in-the-loop workflow

The system does not auto-submit applications or auto-send documents. The user must review and approve package content before export and manual application.

### Local-first design

All application state is stored locally in SQLite. This makes the system simple to run and maintain without external account services.

### Profile-first generation

The user profile is the only allowed source for professional statements. That design is the foundation of the validation layer.

### Optional LLM use

When an API key is present, the system can improve clarity or polish outputs. Without a key, a template/offline path still enables the core workflow with no forced cloud dependency.

## 6. Risk and limitations

The system should be treated as a productivity assistant, not an autonomous recruiter or legal compliance engine. It is designed to avoid unsupported claims, but the user is still responsible for:

- checking legal eligibility
- confirming salary and work authorization details
- validating final application content
- applying manually to job boards and employers

## 7. Summary

The project is a structured application pipeline that turns personal profile data and job descriptions into a reviewable, exportable job package. Its core strength is the combination of profile-grounded generation with validation and explicit human approval.
