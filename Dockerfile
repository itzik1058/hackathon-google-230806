FROM python:3.11-slim

ENV PYTHONUNBUFFERED True

WORKDIR /code

COPY . /code

RUN pip install -e /code

EXPOSE 8000/tcp

CMD ["solar"]
