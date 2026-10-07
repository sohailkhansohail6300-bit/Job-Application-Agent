import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import yaml

from core.paths import path_from_root
from core.utils import load_yaml, save_yaml

PROFILE_PATH = path_from_root('profile', 'master_profile.yaml')

st.set_page_config(page_title='My Profile')
st.header('👤 My Profile')
st.caption('This is the single source of truth for the application agent.')

profile = load_yaml(PROFILE_PATH, {}) or {}
contact = profile.setdefault('contact', {})
work = profile.setdefault('work', {})
prefs = profile.setdefault('preferences', {})

with st.form('profile_form'):
    st.subheader('Contact')
    contact['full_name'] = st.text_input('Full name', value=contact.get('full_name', ''))
    contact['email'] = st.text_input('Email', value=contact.get('email', ''))
    contact['phone'] = st.text_input('Phone', value=contact.get('phone', ''))
    contact['location'] = st.text_input('Location', value=contact.get('location', ''))
    contact['linkedin'] = st.text_input('LinkedIn', value=contact.get('linkedin', ''))
    contact['github'] = st.text_input('GitHub', value=contact.get('github', ''))
    contact['portfolio'] = st.text_input('Portfolio', value=contact.get('portfolio', ''))

    st.subheader('Work & legal')
    work['authorization'] = st.text_input('Work authorization', value=work.get('authorization', ''))
    work['relocation'] = st.text_input('Relocation preference', value=work.get('relocation', ''))
    work['notice_period'] = st.text_input('Notice period', value=work.get('notice_period', ''))
    work['years_experience'] = st.number_input('Years of experience', 0, 60, int(work.get('years_experience') or 0))

    st.subheader('Job preferences')
    prefs['target_titles'] = st.text_input('Target job titles (comma-separated)', value=', '.join(prefs.get('target_titles', [])))
    prefs['locations'] = st.text_input('Preferred locations', value=', '.join(prefs.get('locations', [])))
    prefs['remote'] = st.selectbox('Remote preference', ['any', 'remote', 'hybrid', 'onsite'], index=['any', 'remote', 'hybrid', 'onsite'].index(prefs.get('remote') or 'any'))
    prefs['min_salary'] = st.number_input('Minimum salary', 0, 2000000, int(prefs.get('min_salary') or 0))
    prefs['salary_currency'] = st.text_input('Currency', value=prefs.get('salary_currency', 'USD'))
    prefs['max_applications_per_day'] = st.number_input('Max applications per day', 1, 50, int(prefs.get('max_applications_per_day') or 5))

    profile['summary'] = st.text_area('Professional summary', value=profile.get('summary', '') or '', height=140)

    if st.form_submit_button('💾 Save profile'):
        prefs['target_titles'] = [t.strip() for t in prefs['target_titles'].split(',') if t.strip()]
        prefs['locations'] = [t.strip() for t in prefs['locations'].split(',') if t.strip()]
        profile['experience'] = profile.get('experience', [])
        profile['education'] = profile.get('education', [])
        profile['skills'] = profile.get('skills', [])
        profile['certifications'] = profile.get('certifications', [])
        profile['languages'] = profile.get('languages', [])
        save_yaml(PROFILE_PATH, profile)
        st.success('Profile saved.')

st.subheader('Advanced YAML editor')
raw = st.text_area('Master profile YAML', value=yaml.safe_dump(profile, sort_keys=False, allow_unicode=True), height=500)
if st.button('💾 Save YAML'):
    try:
        parsed = yaml.safe_load(raw) or {}
        if not isinstance(parsed, dict):
            st.error('YAML must resolve to a dictionary object.')
        else:
            save_yaml(PROFILE_PATH, parsed)
            st.success('YAML saved.')
    except Exception as exc:
        st.error(f'Invalid YAML: {exc}')

if not contact.get('full_name'):
    st.warning('Add at least your full name before analyzing jobs.')
