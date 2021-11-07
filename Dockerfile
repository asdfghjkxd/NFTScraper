FROM python:3.9.7

WORKDIR /usr/src/streamlit
COPY requirements.txt ./
RUN pip install -r ./requirements.txt
COPY . .

ENTRYPOINT ["streamlit", "run", "app.py"]