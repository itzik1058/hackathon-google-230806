FROM python:3.11

WORKDIR /dist

COPY dist/solar-0.1.0-py3-none-any.wheel /dist/solar.wheel

RUN pip install -r /dist/solar.wheel

CMD ["solar"]
