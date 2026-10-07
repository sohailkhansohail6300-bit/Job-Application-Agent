import json
from typing import Dict, List

from core.utils import load_yaml
from core.paths import path_from_root


def _normalized(value):
    if isinstance(value, str):
        return value.lower().strip()
    return str(value).lower().strip()


def load_settings():
    return load_yaml(path_from_root('config', 'settings.yaml'), {}) or {}


def _calc_score(parsed, profile):
    settings = load_settings().get('scoring', {})
    weights = {
        'skill_match': settings.get('skill_match', 30),
        'experience': settings.get('experience', 20),
        'ats_keywords': settings.get('ats_keywords', 15),
        'responsibilities': settings.get('responsibilities', 15),
        'location': settings.get('location', 8),
        'salary': settings.get('salary', 7),
        'education_certifications': settings.get('education_certifications', 5),
    }

    prof_skills = [
        _normalized(s.get('name') or s.get('skill') or s)
        for s in (profile.get('skills') or [])
    ]
    required = [_normalized(s) for s in (parsed.get('skills') or [])]
    matched = [s for s in required if s in prof_skills]
    skill_score = (len(matched) / max(1, len(required))) * 100 if required else 100

    years = int(profile.get('work', {}).get('years_experience') or 0)
    exp_needed = 3 if parsed.get('seniority') == 'mid' else 5 if parsed.get('seniority') == 'senior' else 1
    exp_score = min(100, max(0, (years / max(1, exp_needed)) * 100))

    keyword_hits = [k for k in (parsed.get('keywords') or []) if _normalized(k) in ' '.join(prof_skills)]
    ats_score = (len(keyword_hits) / max(1, len(parsed.get('keywords') or []))) * 100

    location_ok = True
    if parsed.get('location') and profile.get('preferences', {}).get('locations'):
        prof_locations = [_normalized(x) for x in profile.get('preferences', {}).get('locations', [])]
        location_ok = _normalized(parsed.get('location')) in prof_locations or any(
            _normalized(p) in _normalized(parsed.get('location')) for p in prof_locations
        )
    location_score = 100 if location_ok else 50

    salary_score = 100
    if parsed.get('salary_raw') and profile.get('preferences', {}).get('min_salary'):
        min_salary = int(profile.get('preferences', {}).get('min_salary') or 0)
        salary_score = 100 if min_salary <= 0 else 80

    education_score = 100
    if parsed.get('education'):
        prof_edu = [
            _normalized(item.get('degree') or item.get('name') or item)
            for item in (profile.get('education') or [])
        ]
        req_edu = [_normalized(v) for v in parsed.get('education', [])]
        if req_edu and not any(r in prof_edu for r in req_edu):
            education_score = 50

    weighted = (
        skill_score * (weights['skill_match'] / 100)
        + exp_score * (weights['experience'] / 100)
        + ats_score * (weights['ats_keywords'] / 100)
        + 60 * (weights['responsibilities'] / 100)
        + location_score * (weights['location'] / 100)
        + salary_score * (weights['salary'] / 100)
        + education_score * (weights['education_certifications'] / 100)
    )

    score = round(min(100, max(0, weighted)), 1)
    return {
        'score': score,
        'skill_score': round(skill_score, 1),
        'experience_score': round(exp_score, 1),
        'ats_score': round(ats_score, 1),
        'location_score': round(location_score, 1),
        'salary_score': round(salary_score, 1),
        'education_score': round(education_score, 1),
    }


def score_job(parsed, profile, location=None, salary_raw=None):
    score_info = _calc_score(parsed, profile)
    score = score_info['score']
    thresholds = load_settings().get('thresholds', {})
    if score >= thresholds.get('strong_match', 80):
        recommendation = 'STRONG MATCH'
    elif score >= thresholds.get('good_match', 65):
        recommendation = 'GOOD MATCH'
    elif score >= thresholds.get('possible_match', 45):
        recommendation = 'POSSIBLE MATCH'
    elif score >= thresholds.get('weak_match', 25):
        recommendation = 'WEAK MATCH'
    else:
        recommendation = 'DO NOT APPLY'

    strengths = []
    if score_info['skill_score'] >= 60:
        strengths.append('Core skills align well with the role.')
    if score_info['experience_score'] >= 60:
        strengths.append('Experience level matches the target seniority.')
    if score_info['ats_score'] >= 50:
        strengths.append('The profile includes useful ATS keywords from the job.')

    weaknesses = []
    if score_info['skill_score'] < 60:
        weaknesses.append('Some required skills are missing from the profile.')
    if score_info['location_score'] < 100:
        weaknesses.append('Location preference may not align with the role.')
    if score_info['education_score'] < 100:
        weaknesses.append('Education or certification requirements may not be fully covered.')

    result = {
        'score': int(score),
        'match_score': int(score),
        'recommendation': recommendation,
        'strengths': strengths,
        'weaknesses': weaknesses,
        'detail': score_info,
    }
    return result
