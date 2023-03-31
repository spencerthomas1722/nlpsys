FROM python:3.11-slim

WORKDIR /app

COPY . .

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_lg

# ENV PATH="${PATH}:C:\Users\rltho\AppData\Roaming\Python\Python311\Scripts"

EXPOSE 5000

ENTRYPOINT [ "streamlit", "run" ]

CMD [ "Home.py" ]