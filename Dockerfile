FROM ubuntu:20.04

RUN apt update
RUN apt upgrade -y

# If a timezone is not set the installation further below of software-properties-common
# interrupts the Docker build in order to ask for location information. Setting
# the timezone in advance allows for the Docker build to proceed without that blocker.
RUN apt install -y tzdata
ENV TZ "America/Bogota"

# Install some pre-requisites
RUN apt install -y build-essential
RUN apt install -y software-properties-common
RUN apt install -y git
RUN apt install -y wget

# Install firefox
RUN add-apt-repository -y ppa:mozillateam/ppa
RUN apt update
RUN apt install -y firefox

# Install python
RUN apt install -y python3.9
RUN apt install -y python3-pip

RUN apt autoremove -y --purge

WORKDIR /app

# Install all the requirements for the python code to run
COPY requirements.txt /app
RUN python3.9 -m pip install --upgrade pip
RUN python3.9 -m pip install -r requirements.txt

# install geckodriver
RUN mkdir drivers
WORKDIR /app/drivers
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz
RUN tar -xvzf geckodriver-v0.31.0-linux64.tar.gz
RUN rm geckodriver-v0.31.0-linux64.tar.gz
RUN chmod +x geckodriver
ENV PATH "$PATH:/app/drivers/"

# Grab the contents of another github repo, which has useful python code
# for querying crypto related APIs and copy it into the container so it can be used by the
# code in this repo.
WORKDIR /app
RUN mkdir crypto_apis
RUN git clone https://github.com/mcIovin/crypto-related-python-apis.git crypto_apis/
ENV PYTHONPATH "${PYTHONPATH}:/app/crypto_apis/"

# copy repo code into container
RUN mkdir src
COPY src/* /app/src/

# use a script to execute a container
COPY entrypoint_commands.sh /app/entrypoint_commands.sh
RUN chmod +x /app/entrypoint_commands.sh
ENTRYPOINT ["/app/entrypoint_commands.sh"]
