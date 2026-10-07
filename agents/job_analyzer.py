from __future__ import annotations

import json
from typing import Dict, List

from jobs.job_parser import parse_job_description


def analyze_job(raw_text: str) -> Dict:
    parsed = parse_job_description(raw_text)
    return {
        'parsed': parsed,
        'summary': {
            'job_title': parsed.get('title'),
            'location': parsed.get('location'),
            'skills': parsed.get('skills', []),
            'keywords': parsed.get('keywords', []),
            'seniority': parsed.get('seniority'),
            'education': parsed.get('education', []),
            'certifications': parsed.get('certifications', []),
        },
    }
