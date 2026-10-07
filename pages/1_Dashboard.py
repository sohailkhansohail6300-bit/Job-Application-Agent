import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st

from database import repository as repo

st.set_page_config(page_title='Dashboard')
st.header('📊 Dashboard')

stats = repo.dashboard_stats()
cols = st.columns(4)
for col, (label, key) in zip(cols * 2, [
    ('Jobs analyzed', 'jobs_analyzed'),
    ('Strong matches', 'strong_matches'),
    ('Ready for review', 'ready_for_review'),
    ('Approved', 'approved'),
    ('Applied', 'applied'),
    ('Interviews', 'interviews'),
    ('Rejections', 'rejections'),
    ('Offers', 'offers'),
]):
    col.metric(label, stats[key])

st.subheader('Recent applications')
apps = repo.list_applications()[:15]
if apps:
    st.dataframe([
        {
            'Company': a['company'],
            'Job': a['title'],
            'Score': a['match_score'],
            'Status': a['status'],
            'Found': (a['date_found'] or '')[:10],
        }
        for a in apps
    ], use_container_width=True, hide_index=True)
else:
    st.info('No applications yet. Add a job to begin.')
