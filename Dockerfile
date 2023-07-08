# Make image as small as possible (that's why slim is used)
FROM python:3.10-slim

COPY ./entrypoint.sh /entrypoint.sh
COPY ./app /app
COPY ./requirements.txt /requirements.txt

RUN apt-get update && \
    apt-get install -y \
        python3-dev \
        python3-setuptools \
        tesseract-ocr \
        make \
        gcc \
    && python3 -m pip install -r requirements.txt \
    # Remove everything previously installed we don't need
    && apt-get remove -y --purge make gcc build-essential \
    # Remove anything else
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN chmod +x entrypoint.sh

CMD [ "./entrypoint.sh" ]