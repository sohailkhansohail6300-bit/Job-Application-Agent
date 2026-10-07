import re
from collections import Counter


def _clean_text(text):
    text = re.sub(r'\s+', ' ', text or '')
    return text.strip()


def _extract_skill_tokens(text):
    text = text.lower()
    common = [
        'python', 'sql', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'javascript', 'typescript',
        'react', 'node', 'java', 'c#', 'go', 'scala', 'spark', 'airflow', 'machine learning', 'ml',
        'data analysis', 'etl', 'postgres', 'mysql', 'mongodb', 'redis', 'linux', 'terraform',
        'ci/cd', 'git', 'agile', 'scrum', 'product management', 'power bi', 'tableau', 'excel'
    ]
    found = []
    for item in common:
        if item in text:
            found.append(item)
    return found


def parse_job_description(raw_text):
    text = _clean_text(raw_text)
    if not text or len(text) < 30:
        raise ValueError('Job description is empty or too short.')

    title = 'Job Role'
    if ' engineer ' in text.lower():
        title = 'Engineer'
    elif ' manager ' in text.lower():
        title = 'Manager'
    elif ' analyst ' in text.lower():
        title = 'Analyst'
    elif 'developer' in text.lower():
        title = 'Developer'

    skills = _extract_skill_tokens(text)
    keywords = list(dict.fromkeys(skills))
    responsibilities = []
    for match in re.findall(r'(?i)(?:responsibilities|you will|duties include|key responsibilities)[:\s]+([^\.]+)', text):
        responsibilities.append(match.strip())
    if not responsibilities:
        responsibilities = ['Role requirements and responsibilities are described in the job description.']

    seniority = 'mid'
    lowered = text.lower()
    if any(term in lowered for term in ['senior', 'lead', 'principal']):
        seniority = 'senior'
    elif any(term in lowered for term in ['junior', 'associate']):
        seniority = 'junior'

    education = []
    if 'bachelor' in lowered:
        education.append('Bachelor\'s degree')
    if 'master' in lowered:
        education.append('Master\'s degree')

    certifications = []
    if 'aws' in lowered:
        certifications.append('AWS')
    if 'azure' in lowered:
        certifications.append('Azure')

    location = ''
    loc_match = re.search(r'(?i)\b(?:location|city|remote|hybrid)[:\s]+([^\n]+)', text)
    if loc_match:
        location = loc_match.group(1).strip()

    salary = ''
    sal_match = re.search(r'\$\s?[0-9][0-9,]*(?:\s*-\s*\$?\s?[0-9][0-9,]*)?', text)
    if sal_match:
        salary = sal_match.group(0)

    return {
        'title': title,
        'company': 'Unknown',
        'location': location or 'Unknown',
        'salary_raw': salary,
        'skills': skills,
        'preferred_skills': skills,
        'keywords': keywords,
        'responsibilities': responsibilities,
        'seniority': seniority,
        'education': education,
        'certifications': certifications,
        'requirements': {
            'skills': skills,
            'seniority': seniority,
            'education': education,
            'certifications': certifications,
        },
        'raw_text': text,
    }
