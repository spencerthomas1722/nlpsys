"""To run:
uvicorn restful:app"""
from fastapi import FastAPI, Body
import json
from nltk.corpus import gutenberg
from nltk.tokenize import sent_tokenize
import random
import spacy

app = FastAPI()
nlp = spacy.load("en_core_web_lg", exclude=['tokenizer', 'tok2vec', 'tagger', 'parser',
                                            'senter', 'attribute_ruler', 'lemmatizer'])


# while there is no user input,
# return NER output for five contiguous sentences from one of the works in the gutenberg corpus
# the work and the starting sentence are chosen at random
@app.get("/")
def index():
    fname = random.choice(gutenberg.fileids())
    all_text = gutenberg.raw(fname)
    all_sents = sent_tokenize(all_text)
    starting_index = random.randint(0, len(all_sents) - 5)
    five_sents = ' '.join(all_sents[starting_index:starting_index + 5])
    return nlp(five_sents).to_json()


# given a text, return its NER output
# NER output will be in json format
@app.post("/process")
def process(input_text: str = Body()):
    return json.dumps(get_entities(nlp(input_text)))


def get_entities(doc):
    entities = []
    for e in doc.ents:
        entities.append((e.start_char, e.end_char, e.label_, e.text))
    return entities
