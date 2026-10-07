# User Workflow Guide

This guide explains the intended application flow for the Personal Job-Application Agent.

## 1. Prepare the master profile

Start by updating your personal profile in the `My Profile` page. This page is the system's single source of truth.

Capture the following information:

- Full name and contact details
- Location and work authorization status
- Relocation preferences and notice period
- Years of experience
- Experience entries
- Education entries
- Skills and certifications
- Languages
- Target role titles and preferred locations
- Salary range and remote preference

The structured editor stores core fields such as contact info and work authorization. The YAML tab is used for more detailed experience and education records. Every list item should have a stable identifier so the system can track provenance.

## 2. Add a job

Use the `Add Job` page to add a role in one of two ways:

- Paste an Indeed URL and attempt automatic fetch
- Paste the full job description manually

The system stores:

- company
- job title
- location
- salary raw text
- source type (`indeed` or `manual`)
- raw description text

If the Indeed page fetch fails or returns a poor result, the manual paste path is the fallback.

## 3. Run job analysis

From the `Job Analysis` page, select a saved job and click `Run analysis`.

The system performs the following operations:

- parse the job description
- extract structured requirements
- compare those requirements to the profile
- compute a match score from 0 to 100
- generate a recommendation and rationale
- prepare a tailored CV draft
- prepare cover letter content
- produce application Q&A responses

If the profile is incomplete, analysis is blocked until the required profile information is added.

## 4. Review the generated package

After analysis, the application enters the review pipeline. The `Tailored Application` page allows the user to inspect:

- tailored CV text
- cover letter draft
- Q&A responses
- validation issues and warning notes

This is where the user can adjust wording and confirm that every claim is traceable to the master profile.

## 5. Validate before approval

The validator checks generated statements against the profile. It can:

- approve a statement as supported
- warn that a statement may need confirmation
- block a statement as unsupported

A blocked claim prevents approval. This is a deliberate safeguard against fabricated professional claims.

## 6. Approve and export

The `Review` page gives the user a final approval checkpoint. Approval is only possible when:

- no critical blocked claims remain
- all required Q&A items have been answered
- the user explicitly confirms acceptance

When approved, the system exports:

- DOCX version of the tailored CV
- PDF version of the tailored CV
- DOCX version of the cover letter
- PDF version of the cover letter

Files are saved into the project `artifacts/` directory with timestamped names and a versioned base name.

## 7. Apply manually

The app is intentionally designed to avoid automatic application submission. After export, the user is expected to:

- open the original job listing manually
- submit the tailored materials through the actual application form
- confirm later whether the application was sent or rejected

This keeps the workflow lawful, transparent, and user-controlled.

## 8. Manage tracker status

The `Application Tracker` page is used to log the application lifecycle:

- found
- analyzing
- tailored
- ready for review
- approved
- applied
- interview
- rejected
- withdrawn
- offer

Users can also add:

- follow-up dates
- notes
- final outcome descriptions

This provides a simple operational record for ongoing job search management.

## 9. Recommended operating habits

To keep the tool effective and trustworthy:

- update your profile frequently as roles and experience evolve
- review each generated package before approval
- resolve warnings instead of ignoring them
- keep job records organized by company and title
- use tracker notes to maintain a clean follow-up cadence

## 10. Typical end-to-end flow

A common usage pattern looks like this:

1. Define or refresh your profile
2. Add a job description
3. Run analysis
4. Review CV and cover letter
5. Resolve validation issues
6. Approve export
7. Submit the application manually
8. Update the tracker with status and follow-up dates

This workflow turns the tool into a guided job-search assistant rather than an autonomous application bot.
