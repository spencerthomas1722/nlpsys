from flask import Flask, jsonify, request, render_template, Markup
from flask_restful import Api
from nltk.corpus import gutenberg
from nltk.tokenize import sent_tokenize
import random
import spacy
from spacy import displacy

app = Flask(__name__)
api = Api()

nlp = spacy.load('en_core_web_lg')
nlp.add_pipe('merge_entities')
dep_ents = {}

html_template = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; 
                    padding: 1rem; margin-bottom: 2.5rem">{}</div>"""


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input_json = request.get_json()
        return render_template('index.html', post=jsonify({'returning': user_input_json})), 201
    else:
        entities = []
        while len(entities) == 0:  # keep looking for examples until we see one with named entities
            # get random text from corpus for demo
            fname = random.choice(gutenberg.fileids())
            print(fname)
            all_text = gutenberg.raw(fname)
            all_sents = sent_tokenize(all_text)
            sent = random.choice(all_sents)
            # pipe that text
            doc = nlp(sent)
            entities = doc.ents
        # display
        markup = Markup(add_tag(displacy.render(doc, options={'compact': True}), entities))
        return render_template("index.html", post=jsonify('Hello, human (presumably)'), demograph=markup)


@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        text = request.form['rawtext']
        # get piped text
        doc = nlp(text)  # TODO separate sentences
        # get entities
        entities = doc.ents
        markup = Markup(add_tag(displacy.render(doc, options={'compact': True}), entities))
        return render_template('results.html', depgraphs=markup)


def add_tag(html, ents):
    lines = html.split('\n')
    ent_texts = [ent.text for ent in ents]
    new_lines = []
    this_chunk = []
    namedent = False
    for line in lines:
        if 'displacy-token' in line:  # beginning of a word block
            this_chunk.append(line)
        elif len(this_chunk) > 0:  # in a word chunk
            this_chunk.append(line)
            if '</text>' in line:
                if namedent:  # if there was a named entity in this text box,
                    new_lines.append(this_chunk[0].replace('displacy-token', 'displacy-token-namedent'))
                    new_lines.extend(this_chunk[1:])
                else:
                    new_lines.extend(this_chunk)
                this_chunk = []
                namedent = False
            else:
                for ent in ent_texts:
                    if '>' + ent + '</tspan>' in line:  # is this hacky? yes. does it work? also yes.
                        namedent = True
        else:
            new_lines.append(line)
    return '\n'.join(new_lines)


if __name__ == '__main__':
    app.run(port=5000, debug=True)
