import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json

import streamlit as st

from agents import answer_engine, cover_letter, cv_tailor, validator
from core.paths import path_from_root
from core.utils import load_yaml
from database import repository as repo

st.set_page_config(page_title='Tailored Application')
st.header('🧩 Tailored Application')

apps = repo.list_applications()
if not apps:
    st.info('No application package exists yet. Run analysis from a saved job first.')
    st.stop()

app = st.selectbox('Select package', apps, format_func=lambda a: f"#{a['id']} — {a['company']} / {a['title']} [{a['status']}]")

profile = load_yaml(path_from_root('profile', 'master_profile.yaml'), {}) or {}
if not profile.get('contact', {}).get('full_name'):
    st.error('Please complete your master profile first.')
    st.stop()

job = None
job_candidates = repo.list_jobs()
for item in job_candidates:
    if item['company'] == app['company'] and item['title'] == app['title']:
        job = item
        break

if job is None:
    st.error('Matching job record not found.')
    st.stop()

if st.button('Generate tailored package'):
    cv_text = cv_tailor.tailor_cv(profile, job)
    cl_text = cover_letter.generate_cover_letter(profile, job)
    questions = [
        'Do you require visa sponsorship or work authorization support?',
        'Are you willing to relocate for this role?',
        'Which salary expectations do you have for this position?',
    ]
    qa = answer_engine.generate_answers(profile, questions)
    validation = validator.validate_claims(profile, [line for line in cv_text.splitlines() if line.strip() and not line.startswith('#') and not line.startswith('##') and not line.startswith('- ')])

    repo.update_application(
        app['id'],
        cv_text=cv_text,
        cover_letter_text=cl_text,
        qa_json=json.dumps(qa),
        validation_json=json.dumps(validation),
        status='READY_FOR_REVIEW',
    )
    st.success('Tailored package generated and saved.')
    st.rerun()

if app.get('cv_text'):
    st.subheader('Tailored CV')
    st.text_area('Edit CV', value=app['cv_text'], height=350, key='cv_edit')
    if st.button('Save CV edits'):
        repo.update_application(app['id'], cv_text=st.session_state['cv_edit'])
        st.success('CV updated.')

if app.get('cover_letter_text'):
    st.subheader('Cover letter')
    st.text_area('Edit cover letter', value=app['cover_letter_text'], height=250, key='cl_edit')
    if st.button('Save cover letter edits'):
        repo.update_application(app['id'], cover_letter_text=st.session_state['cl_edit'])
        st.success('Cover letter updated.')

if app.get('qa_json'):
    st.subheader('Application Q&A')
    qa = json.loads(app['qa_json'])
    for item in qa:
        st.markdown(f"**Q:** {item['question']}")
        st.text_area('Answer', value=item.get('answer', ''), key=f"qa_{item['question']}")
        if item.get('requires_confirmation'):
            st.warning('⚠️ This item requires confirmation before approval.')

validation = json.loads(app['validation_json']) if app.get('validation_json') else {'ok': True, 'blocked': [], 'needs_confirmation': []}
if validation.get('blocked'):
    st.subheader('Validation results')
    for block in validation['blocked']:
        st.error(f"⚠️ Unsupported claim detected: {block['claim']}")
        st.caption(block['detail'])
