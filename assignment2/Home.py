import db
import os
import pandas as pd
import streamlit as st
import spacy
import spacy_streamlit
from streamlit_extras.switch_page_button import switch_page

nlp = spacy.load('en_core_web_lg')
connection = db.DatabaseConnection('entities.sqlite')

st.set_page_config(page_title="Home")

st.title('Named entity recognizer')

if 'last_input' not in st.session_state:  # https://blog.streamlit.io/session-state-for-streamlit/
    st.session_state.last_input = ''

with st.form('new_input'):
    text_input = st.text_area('Enter text:')
    submitted = st.form_submit_button('Submit')
    if submitted:
        doc = nlp(text_input)
        st.session_state.last_input = doc
        # get entity
        for ent in doc.ents:  # add to database
            # ent, ent_label, start_token, end_token, start_char, end_char, sent
            connection.add(ent.text, ent.label_, ent.start, ent.end, ent.start_char, ent.end_char, text_input)  # add to history
        switch_page('Results')

# TODO remove before submitting:
# multiple pages: https://towardsdatascience.com/3-ways-to-create-a-multi-page-streamlit-app-1825b5b07c0f
