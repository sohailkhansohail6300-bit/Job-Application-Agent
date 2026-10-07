def generate_answers(profile, questions):
    contact = profile.get('contact', {})
    work = profile.get('work', {})
    answers = []
    for q in questions:
        ql = (q or '').lower()
        if 'authorization' in ql or 'sponsorship' in ql or 'visa' in ql:
            answer = work.get('authorization') or 'Please confirm your work authorization status.'
            requires_confirmation = not bool(work.get('authorization'))
        elif 'location' in ql or 'relocate' in ql:
            answer = work.get('relocation') or 'Please confirm your relocation preference.'
            requires_confirmation = not bool(work.get('relocation'))
        elif 'salary' in ql or 'compensation' in ql:
            answer = f"My target salary is {profile.get('preferences', {}).get('min_salary', 0)} {profile.get('preferences', {}).get('salary_currency', 'USD')} per year."
            requires_confirmation = False
        else:
            answer = 'Based on my profile, I am confident in my background and qualifications for this role.'
            requires_confirmation = False
        answers.append({
            'question': q,
            'answer': answer,
            'requires_confirmation': requires_confirmation,
            'supporting_profile_facts': ['Master profile'],
        })
    return answers
