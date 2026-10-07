def generate_cover_letter(profile, job):
    contact = profile.get('contact', {})
    full_name = contact.get('full_name') or 'Candidate'
    location = contact.get('location') or 'Your location'
    company = job.get('company') or 'the company'
    title = job.get('title') or 'the role'
    summary = profile.get('summary') or 'I am a motivated professional with relevant experience and a strong desire to contribute.'

    return f'''Dear Hiring Manager,

I am writing to express my interest in the {title} position at {company}. I am excited by the opportunity to contribute my background and experience to a team that values thoughtful execution and measurable impact.

{summary}

I am especially interested in this opportunity because it aligns with my experience, skills, and career goals. I would welcome the opportunity to discuss how my background can support {company}'s goals and the expectations of this role.

Thank you for your time and consideration. I look forward to the opportunity to speak further.

Sincerely,
{full_name}
{location}
'''
