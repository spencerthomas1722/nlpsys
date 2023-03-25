import db
import pandas as pd
import streamlit as st
import spacy
import spacy_streamlit

nlp = spacy.load('en_core_web_lg')
connection = db.DatabaseConnection('entities.sqlite')

st.title('Named entity recognizer')

input_tab, history_tab = st.tabs(['Input', 'History'])

# tab for user input
with input_tab:
    with st.form('new_input'):
        text_input = st.text_area('Enter text:')
        submitted = st.form_submit_button('Submit')
        if submitted:
            doc = nlp(text_input)
            # get entity
            for ent in doc.ents:
                connection.add(ent.text, ent.start_char, ent.label_, text_input)  # add to history


# TODO separate pages, not tabs
    # TODO main
    # TODO results
        # TODO do implementation code
    # TODO history
        # TODO don't show hash

# view previously input sentences
# default: all, but user can search for a specific entity name
with history_tab:
    with st.form('new_query'):
        query = st.text_input('Query:', value=None)
        submitted = st.form_submit_button('Search')
        if submitted:
            out = connection.get(query)
        else:
            out = connection.get(None)
        results_df = pd.DataFrame.from_records(data=out)
        st.dataframe(results_df)
