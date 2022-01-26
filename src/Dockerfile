FROM python:3.10.1
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN apt update && apt-get install -y sqlite3

WORKDIR /usr/local/share
COPY ./*.py ./
RUN mkdir static
RUN mkdir templates
COPY ./static/* ./static/
COPY ./templates/* ./templates/
RUN chmod +x main.py

ENTRYPOINT ["/usr/local/share/main.py", "--http", "--db-name", "train.db"]
