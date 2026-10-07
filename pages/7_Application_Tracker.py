import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from database import repository as repo

st.set_page_config(page_title='Application Tracker')
st.header('📋 Application Tracker')

apps = repo.list_applications()
if not apps:
    st.info('No applications yet.')
    st.stop()

st.dataframe([
    {
        'ID': a['id'],
        'Company': a['company'],
        'Job': a['title'],
        'Score': a['match_score'],
        'Status': a['status'],
        'Found': (a['date_found'] or '')[:10],
        'Approved': (a['date_approved'] or '')[:10],
        'Applied': (a['date_applied'] or '')[:10],
        'Follow-up': a['follow_up_date'] or '',
    }
    for a in apps
], use_container_width=True, hide_index=True)

st.subheader('Update application status')
app = st.selectbox('Select application', apps, format_func=lambda a: f"#{a['id']} — {a['company']} / {a['title']}")
status = st.selectbox('Status', repo.APPLICATION_STATUSES, index=repo.APPLICATION_STATUSES.index(app['status']))
follow_up = st.text_input('Follow-up date (YYYY-MM-DD)', value=app.get('follow_up_date') or '')
notes = st.text_area('Notes', value=app.get('notes') or '', height=120)
outcome = st.text_input('Outcome', value=app.get('outcome') or '')

if st.button('💾 Update'):
    if follow_up and len(follow_up.strip()) != 10:
        st.error('Follow-up date must be YYYY-MM-DD.')
    else:
        repo.update_application(app['id'], status=status, follow_up_date=follow_up.strip() or None, notes=notes, outcome=outcome)
        st.success('Application updated.')

if app['status'] == 'APPLIED' and st.button('Promote to INTERVIEW'):
    repo.update_application(app['id'], status='INTERVIEW')
    st.success('Status updated to INTERVIEW.')
