FROM python:3.10-buster

# Install OpenJDK-11
RUN apt-get update && \
    apt-get install -y openjdk-11-jre-headless && \
    apt-get clean;

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY src src
ENTRYPOINT ["python", "main.py"]