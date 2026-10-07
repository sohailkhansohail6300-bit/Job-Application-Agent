import streamlit as st


def banner(text, kind='info'):
    if kind == 'info':
        st.info(text)
    elif kind == 'warning':
        st.warning(text)
    elif kind == 'error':
        st.error(text)
    elif kind == 'success':
        st.success(text)
    else:
        st.write(text)
