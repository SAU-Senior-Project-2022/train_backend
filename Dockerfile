FROM python:3.10.1
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY documentation.html /usr/local/share/
COPY database.py /usr/local/share/
COPY endpoints.py /usr/local/share/
COPY server.py /usr/local/share/
COPY main.py /usr/local/share/train_backend

CMD ["python", "/usr/local/share/train_backend"]
