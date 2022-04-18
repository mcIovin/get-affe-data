FROM python:3.10.4-bullseye

WORKDIR /app

COPY requirements.txt /app
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

RUN mkdir crypto_apis
RUN git clone https://github.com/mcIovin/crypto-related-python-apis.git crypto_apis/
ENV PYTHONPATH "${PYTHONPATH}:/app/crypto_apis/"

RUN mkdir src
COPY src/* /app/src/

RUN mkdir drivers
WORKDIR /app/drivers
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz
RUN tar -xvzf geckodriver-v0.31.0-linux64.tar.gz
RUN rm geckodriver-v0.31.0-linux64.tar.gz
RUN chmod +x geckodriver
ENV PATH "$PATH:/app/drivers/"

WORKDIR /app/src
CMD [ "python", "get_affe_data.py"]
