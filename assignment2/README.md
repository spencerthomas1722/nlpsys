This was made and tested using Python 3.11.0.
The modules required are listed in `requirements.txt`:
* pandas==1.5.3
* spacy==3.4.4
* spacy-streamlit==1.0.4
* streamlit==1.20.0
* streamlit_extras==0.2.6

To run this program, I ran the following in Powershell:

``docker build -t st_app .
docker run -p 5000:5000 stapp``