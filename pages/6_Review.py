import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime

import streamlit as st

from database import repository as repo
from documents import cv_generator, cover_letter_generator

st.set_page_config(page_title='Review')
st.header('✅ Review Application Package')

apps = [a for a in repo.list_applications() if a['status'] in ('TAILORED', 'READY_FOR_REVIEW', 'APPROVED')]
if not apps:
    st.info('Nothing available for review yet.')
    st.stop()

app = st.selectbox('Select package', apps, format_func=lambda a: f"#{a['id']} — {a['company']} / {a['title']} [{a['status']}]")

st.warning('Nothing is submitted automatically. Approval exports documents and marks the package ready for manual application.', icon='🖐️')

st.subheader('Validation report')
validation = app.get('validation_json')
if validation:
    import json
    validation = json.loads(validation)
    st.info(validation.get('summary', 'Not validated yet.'))
    for block in validation.get('blocked', []):
        st.error(f"⚠️ Unsupported claim detected: {block['claim']}")
        st.caption(block.get('detail', ''))
else:
    st.info('Validation not run yet.')

st.subheader('Tailored CV')
st.markdown(app.get('cv_text') or '_empty_')

st.subheader('Cover letter')
st.markdown((app.get('cover_letter_text') or '_empty_').replace('\n', '  \n'))

st.subheader('Application Q&A')
if app.get('qa_json'):
    import json
    for qa in json.loads(app['qa_json']):
        st.markdown(f"**{qa['question']}**\n{qa.get('answer') or '_needs your answer_'}")
else:
    st.info('No Q&A generated yet.')

col1, col2, col3 = st.columns(3)
if col1.button('✔️ APPROVE', type='primary', use_container_width=True):
    repo.update_application(app['id'], status='APPROVED', date_approved=datetime.now().isoformat(timespec='seconds'))
    st.success('Approved. Documents can now be exported.')

if col2.button('✏️ EDIT', use_container_width=True):
    st.switch_page('pages/5_Tailored_Application.py')

if col3.button('✖️ REJECT', use_container_width=True):
    repo.update_application(app['id'], status='WITHDRAWN', outcome='rejected_by_user')
    st.warning('Package rejected.')

if app['status'] == 'APPROVED' and st.button('Export documents'):
    from core.paths import path_from_root
    out_dir = path_from_root('artifacts')
    cv_files = cv_generator.generate_cv_documents(app.get('cv_text') or '', app['company'], app['title'], out_dir)
    cl_files = cover_letter_generator.generate_cover_letter_documents(app.get('cover_letter_text') or '', app['company'], app['title'], out_dir)
    for artifact_kind, payload in [('cv', cv_files), ('cover_letter', cl_files)]:
        for ext, path in payload.items():
            if ext in ('docx', 'pdf'):
                repo.add_artifact(app['id'], f'{artifact_kind}_{ext}', path)
    st.success('Documents exported to artifacts/.')
