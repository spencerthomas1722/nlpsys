# import db
import streamlit as st
import spacy
import spacy_streamlit

nlp = spacy.load('en_core_web_lg')
# connection = db.DatabaseConnection('entities.sqlite')

st.title('Named entity recognizer')

doc = st.session_state.last_input
spacy_streamlit.visualize_ner(doc, labels=nlp.get_pipe("ner").labels, show_table=False)
