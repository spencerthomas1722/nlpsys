import db
import pandas as pd
import streamlit as st
import spacy

nlp = spacy.load('en_core_web_lg')
connection = db.DatabaseConnection('entities.sqlite')

st.title('Named entity recognizer')
st.session_state.cols = ['count', 'entity', 'label']

# view previously input sentences
# default: all, but user can search for a specific entity name
with st.form('new_query'):
    query = st.text_input('Query:', value='')
    full_columns = ['hash', 'entity', 'label', 'count']
    filtered = st.form_submit_button('Filter')
    if filtered and query.strip() != '':
        out = connection.get(query)
    else:
        out = connection.get(None)
    full_df = pd.DataFrame.from_records(data=out, columns=full_columns)
    filtered_df = full_df[st.session_state.cols]

# checkboxes allowing the user to sort
with st.form('sorting_checkboxes'):
    checkrow = st.columns(4)
    checkboxes = {}
    for i, col in enumerate(st.session_state.cols):
        with checkrow[i]:
            checkboxes[col] = st.checkbox(col)
    sort = st.form_submit_button('Sort')
    if sort:
        if checkboxes['label']:
            filtered_df = filtered_df.sort_values(by='label', ascending=True)
        if checkboxes['entity']:
            filtered_df = filtered_df.sort_values(by='entity', ascending=True)
        if checkboxes['count']:
            filtered_df = filtered_df.sort_values(by='count', ascending=False)

st.dataframe(filtered_df, use_container_width=True)
