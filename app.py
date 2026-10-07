import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st

from database import repository as repo

st.set_page_config(page_title='Job Application Agent', page_icon='🎯', layout='wide')
st.title('🎯 Personal Job-Application Agent')
st.markdown(
    '''
    **Workflow:** PASTE JOB → ANALYZE → MATCH → TAILOR CV → COVER LETTER → Q&A → VALIDATE → REVIEW → APPROVE → EXPORT → APPLY MANUALLY → TRACK

    - Nothing is submitted automatically.
    - The validator blocks unsupported claims.
    - Complete **My Profile** before adding a job.
    '''
)

stats = repo.dashboard_stats()
cols = st.columns(4)
for i, (label, key) in enumerate([
    ('Jobs analyzed', 'jobs_analyzed'),
    ('Strong matches', 'strong_matches'),
    ('Ready for review', 'ready_for_review'),
    ('Approved', 'approved'),
    ('Applied', 'applied'),
    ('Interviews', 'interviews'),
    ('Rejections', 'rejections'),
    ('Offers', 'offers'),
]):
    with cols[i % 4]:
        st.metric(label, stats[key])

st.subheader('Recent applications')
apps = repo.list_applications()[:10]
if apps:
    st.dataframe(
        [
            {
                'Company': a['company'],
                'Job': a['title'],
                'Score': a['match_score'],
                'Status': a['status'],
                'Found': (a['date_found'] or '')[:10],
            }
            for a in apps
        ],
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info('No applications yet. Add a job to begin.')
