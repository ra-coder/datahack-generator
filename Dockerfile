FROM python:3.10-buster
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY src src
ENTRYPOINT ["python", "src/main.py"]