FROM python:3


WORKDIR /

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

COPY main.py /main.py
COPY connector.py /connector.py
COPY deploy-config.yml /config.yml

RUN chmod 0600 /main.py

CMD ["python3", "-u", "/main.py"]
