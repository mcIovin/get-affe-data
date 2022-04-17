FROM python:3.10.4-bullseye

WORKDIR /app

COPY requirements.txt /app
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir crypto_apis
RUN mkdir src
RUN git clone https://github.com/mcIovin/crypto-related-python-apis.git crypto_apis/
COPY src/* /app/src/

ENV PYTHONPATH "${PYTHONPATH}:/app/crypto_apis"

WORKDIR /app/src
CMD [ "python", "get_affe_data.py"]
