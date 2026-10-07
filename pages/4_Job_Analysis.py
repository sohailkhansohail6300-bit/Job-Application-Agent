import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json

import streamlit as st

from agents import job_matcher
from core.paths import path_from_root
from core.utils import load_yaml
from database import repository as repo
from jobs.job_parser import parse_job_description

st.set_page_config(page_title='Job Analysis')
st.header('🔍 Job Analysis')

jobs = repo.list_jobs()
if not jobs:
    st.info('No jobs yet. Add one first.')
    st.stop()

job = st.selectbox('Select job', jobs, format_func=lambda j: f"{j['company']} — {j['title']} ({j['status']})")
profile = load_yaml(path_from_root('profile', 'master_profile.yaml'), {}) or {}
if not profile.get('contact', {}).get('full_name'):
    st.error('Master profile is empty. Fill in My Profile before analyzing jobs.')
    st.stop()

if st.button('Run analysis', type='primary'):
    repo.update_job(job['id'], status='ANALYZING')
    try:
        parsed = parse_job_description(job['jd_text'])
    except ValueError as exc:
        st.error(str(exc))
        st.stop()

    repo.update_job(job['id'], jd_parsed=json.dumps(parsed))
    result = job_matcher.score_job(parsed, profile, location=job.get('location'), salary_raw=job.get('salary_raw'))

    st.session_state['analysis_result'] = {
        'job_id': job['id'],
        'job': job,
        'parsed': parsed,
        'result': result,
    }

    repo.update_job(job['id'], status='TAILORED', match_score=result['match_score'], recommendation=result['recommendation'], strengths='; '.join(result['strengths']), weaknesses='; '.join(result['weaknesses']))
    st.success(f'Analysis complete. Match score: {result["match_score"]}/100')

if 'analysis_result' in st.session_state:
    analysis = st.session_state['analysis_result']
    data = analysis['parsed']
    result = analysis['result']

    st.subheader('Job overview')
    c1, c2, c3, c4 = st.columns(4)
    c1.metric('Company', analysis['job']['company'])
    c2.metric('Title', analysis['job']['title'])
    c3.metric('Location', data.get('location') or analysis['job'].get('location') or 'Unknown')
    c4.metric('Salary', analysis['job'].get('salary_raw') or 'Not provided')

    st.subheader('Match score')
    st.metric('Overall', f"{result['match_score']}/100")
    st.caption(f"Recommendation: {result['recommendation']}")

    st.subheader('Requirements')
    st.write('Required skills:', ', '.join(data.get('skills', []) or ['n/a']))
    st.write('Preferred skills:', ', '.join(data.get('preferred_skills', []) or ['n/a']))
    st.write('Responsibilities:', '; '.join(data.get('responsibilities', []) or ['n/a']))
    st.write('Keywords:', ', '.join(data.get('keywords', []) or ['n/a']))
    st.write('Seniority:', data.get('seniority', 'n/a'))
    st.write('Education requirements:', ', '.join(data.get('education', []) or ['n/a']))
    st.write('Certifications:', ', '.join(data.get('certifications', []) or ['n/a']))

    st.subheader('Match strengths')
    for item in result['strengths']:
        st.success(item)

    st.subheader('Skill gaps / risks')
    for item in result['weaknesses']:
        st.warning(item)

    st.subheader('Score calculation transparency')
    st.json(result['detail'])
