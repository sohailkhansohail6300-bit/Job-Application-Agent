import re


def fetch_job_text(url=None, raw_text=None):
    if raw_text and raw_text.strip():
        return raw_text.strip()
    if not url:
        raise ValueError('Please provide a job URL or paste the job description.')
    if not re.match(r'https?://', url):
        raise ValueError('The job URL must start with http:// or https://.')
    return raw_text.strip() if raw_text else ''
