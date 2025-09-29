FROM python:3.14-rc-slim-bookworm

MAINTAINER "CodeStrate"

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir --quiet -r requirements.txt

COPY . .

CMD ["python", "api/main.py"]
