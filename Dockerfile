FROM python:3.6.3-alpine3.6


WORKDIR /


COPY ["requirements.txt", "main.py", "connector.py", "config.yml", "/"]

RUN pip install --no-cache-dir -r /requirements.txt

CMD ["python3", "-u", "/main.py"]
