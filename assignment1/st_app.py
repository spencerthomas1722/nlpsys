from nltk.corpus import gutenberg
from nltk.tokenize import sent_tokenize
import random
import streamlit as st
import spacy
import spacy_streamlit


nlp = spacy.load('en_core_web_lg')

st.title('Named entity and dependency recognizer')
# one tab for demo
fname = random.choice(gutenberg.fileids())
all_text = gutenberg.raw(fname)
all_sents = sent_tokenize(all_text)
starting_index = random.randint(0, len(all_sents) - 5)
five_sents = ' '.join(all_sents[starting_index:starting_index + 5])

demo_tab, input_tab = st.tabs(['Demo', 'Try it yourself'])
with demo_tab:
    demo = nlp(five_sents)
    # spacy_streamlit.visualize_parser(demo)
    spacy_streamlit.visualize_ner(demo, labels=nlp.get_pipe("ner").labels)

# other tab for user input
with input_tab:
    with st.form('text_input'):
        text_input = st.text_area('Enter text:')
        submitted = st.form_submit_button('Submit')
        if submitted:
            doc = nlp(text_input)
            spacy_streamlit.visualize_parser(doc)
            spacy_streamlit.visualize_ner(doc, labels=nlp.get_pipe("ner").labels)
