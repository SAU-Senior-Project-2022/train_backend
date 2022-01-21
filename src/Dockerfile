FROM python:3.10.1
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /usr/local/share
COPY ./*.py ./
RUN chmod +x main.py
RUN ls -l ./
RUN which python
RUN python --version

ENTRYPOINT ["/usr/local/share/main.py", "--debug", "--http", "--db-url", "mariadb", "--fresh","--seed"]
