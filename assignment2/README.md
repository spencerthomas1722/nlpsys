This was made and tested using Python 3.11.0.
The modules required are listed in `requirements.txt`:
* pandas==1.5.3
* spacy==3.4.4
* spacy-streamlit==1.0.4
* streamlit==1.20.0
* streamlit_extras==0.2.6

as well as spaCy's `en_core_web_lg`, which can be obtained by inputting the following to the command line:

`python -m spacy download en_core_web_sm`

To run this program, I suggest doing the following:

`git clone https://github.com/spencerthomas1722/nlpsys.git`

`cd nlpsys/assignment2`

`docker build -t st_app .`

`docker run -p 5000:5000 stapp`
