import db
import pandas as pd
import streamlit as st
import spacy

nlp = spacy.load('en_core_web_lg')
connection = db.DatabaseConnection('entities.sqlite')

st.title('Named entity recognizer')

# view previously input sentences
# default: all, but user can search for a specific entity name
with st.form('new_query'):
    query = st.text_input('Query:', value='')
    full_columns = ['hash', 'ent', 'ent_label', 'start_token', 'end_token', 'start_char', 'end_char', 'sent']
    st.session_state.cols = ['ent', 'ent_label', 'sent']
    # checkboxes showing which columns to show;
    # checking boxes and hitting "filter" button prompts a new df to be created with the columns in question
    # wrap checkboxes; if we want to generalize, will need for loop
    checkrow1 = st.columns(4)
    checkboxes = {}
    for i, col in enumerate(full_columns[:4]):
        with checkrow1[i]:
            checkboxes[col] = st.checkbox(col)
    checkrow2 = st.columns(4)
    for i, col in enumerate(full_columns[4:]):
        with checkrow2[i]:
            checkboxes[col] = st.checkbox(col)
    filtered = st.form_submit_button('Filter')
    if filtered:
        st.session_state.cols = [col for col in full_columns if checkboxes[col]]
        if query:
            out = connection.get(query)
        else:
            out = connection.get(None)
    else:
        out = connection.get(None)

    full_df = pd.DataFrame.from_records(data=out, columns=full_columns)
    filtered_df = full_df[st.session_state.cols]
    st.dataframe(filtered_df)
