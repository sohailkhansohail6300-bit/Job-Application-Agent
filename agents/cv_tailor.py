import copy


def tailor_cv(profile, job, existing_cv=None):
    profile = profile or {}
    experience = profile.get('experience', []) or []
    skills = profile.get('skills', []) or []
    summary = profile.get('summary') or 'Professional with relevant experience and skills for this role.'

    selected_experience = experience[:3]
    relevant_skills = skills[:10]

    cv_text = [
        '# ' + (profile.get('contact', {}).get('full_name') or 'Candidate'),
        '',
        f"Email: {profile.get('contact', {}).get('email', '')}",
        f"Location: {profile.get('contact', {}).get('location', '')}",
        f"LinkedIn: {profile.get('contact', {}).get('linkedin', '')}",
        f"GitHub: {profile.get('contact', {}).get('github', '')}",
        '',
        '## Professional Summary',
        summary,
        '',
        '## Skills',
    ]

    if relevant_skills:
        cv_text.extend([f'- {s.get("name") if isinstance(s, dict) else s}' for s in relevant_skills])
    else:
        cv_text.append('- Skills to be added in the master profile')

    cv_text.extend(['', '## Experience'])
    for exp in selected_experience:
        title = exp.get('title') or exp.get('role') or 'Professional Experience'
        company = exp.get('company') or 'Company'
        period = exp.get('period') or exp.get('dates') or ''
        bullet_text = exp.get('summary') or exp.get('description') or 'Relevant experience.'
        cv_text.append(f'- {title} @ {company} ({period})')
        cv_text.append(f'  - {bullet_text}')

    cv_text.extend(['', '## Education'])
    for edu in profile.get('education', [])[:3]:
        name = edu.get('school') or edu.get('institution') or 'Education'
        degree = edu.get('degree') or 'Degree'
        cv_text.append(f'- {degree} — {name}')

    if profile.get('certifications'):
        cv_text.extend(['', '## Certifications'])
        for cert in profile.get('certifications', [])[:5]:
            cv_text.append(f'- {cert.get("name") or cert}')

    return '\n'.join(cv_text)
