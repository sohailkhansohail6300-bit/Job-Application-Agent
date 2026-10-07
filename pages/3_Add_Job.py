import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import re

import streamlit as st

from database import repository as repo

st.set_page_config(page_title='Add Job')
st.header('➕ Add Job')

def _extract_text(html):
    html = re.sub(r'(?is)<(script|style).*?>.*?</\\1>', ' ', html)
    return re.sub(r'\s+', ' ', re.sub(r'(?s)<[^>]+>', ' ', html)).strip()

urls_tab, manual_tab = st.tabs(['From job URL', 'Paste job description'])

def _save_job(source, url, company, title, location, salary, jd_text):
    if repo.find_job_by_url(url):
        st.error('Duplicate job URL already exists.')
        return
    if not company.strip() or not title.strip():
        st.error('Company and job title are required.')
        return
    if not jd_text or len(jd_text.strip()) < 30:
        st.error('Job description is too short or empty.')
        return
    job_id = repo.create_job(source, url, company.strip(), title.strip(), location.strip() or None, salary.strip() or None, jd_text.strip())
    st.success(f'Job saved (id {job_id}). Go to Job Analysis to score it.')

with urls_tab:
    url = st.text_input('Indeed URL', placeholder='https://www.indeed.com/viewjob?jk=...')
    if st.button('Try to fetch text'):
        if not url.strip():
            st.warning('Please paste a URL first.')
        else:
            try:
                import requests
                r = requests.get(url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
                if r.status_code == 200 and len(r.text) > 500:
                    jd_text = _extract_text(r.text)
                    st.session_state['jd_preview'] = jd_text
                    st.success('The page was fetched. You can review/edit it before saving.')
                else:
                    st.warning('Could not fetch the URL; paste the job description manually instead.')
            except Exception as exc:
                st.warning(f'Fetch failed: {exc}. Paste the description manually instead.')
    job_preview = st.text_area('Fetched/edited job description', value=st.session_state.get('jd_preview', ''), height=250)
    company = st.text_input('Company *')
    title = st.text_input('Job title *')
    location = st.text_input('Location')
    salary = st.text_input('Salary', placeholder='e.g. 85,000 - 110,000 a year')
    if st.button('Save job from URL', key='save_url'):
        _save_job('indeed', url.strip() or None, company, title, location, salary, job_preview)

with manual_tab:
    manual = st.text_area('Paste job description', height=280, placeholder='Paste the full job description here...')
    company = st.text_input('Company *', key='manual_company')
    title = st.text_input('Job title *', key='manual_title')
    location = st.text_input('Location', key='manual_location')
    salary = st.text_input('Salary', placeholder='e.g. 85,000 - 110,000 a year', key='manual_salary')
    if st.button('Save manual job', key='save_manual'):
        _save_job('manual', None, company, title, location, salary, manual)
