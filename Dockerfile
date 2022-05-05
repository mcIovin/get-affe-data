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

# Install python via miniconda
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
RUN chmod +x Miniconda3-latest-Linux-x86_64.sh
RUN ./Miniconda3-latest-Linux-x86_64.sh -b
# You can't do something like: RUN source venv/bin/activate in a Dockerfile
# So below I specify /bin/bash -c and then run all the commands I need together
# after the 'source'. There is a probably a cleaner, more Docker-esque way to
# do this, but I'm not sure how at the moment.
RUN /bin/bash -c "source ~/miniconda3/bin/activate \
               && conda create -y --name conda_env_3_10 python=3.10 \
               && conda deactivate"

RUN apt autoremove -y --purge

WORKDIR /app

# Install all the requirements for the python code to run (and first upgrage pip)
COPY requirements.txt /app
RUN /bin/bash -c "source ~/miniconda3/bin/activate \
               && conda activate conda_env_3_10 \
               && python -m pip install --upgrade pip \
               && pip install -r requirements.txt \
               && conda deactivate"
# Show some info about the conda virtual environment
RUN /bin/bash -c "source ~/miniconda3/bin/activate \
               && conda activate conda_env_3_10 \
               && conda  info \
               && conda  info --envs \
               && python --version \
               && conda deactivate"

# install geckodriver
RUN mkdir drivers
WORKDIR /app/drivers
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.31.0/geckodriver-v0.31.0-linux64.tar.gz
RUN tar -xvzf geckodriver-v0.31.0-linux64.tar.gz
RUN rm geckodriver-v0.31.0-linux64.tar.gz
RUN chmod +x geckodriver
ENV PATH "$PATH:/app/drivers/"

# Grab the contents of another github repo, which has useful python code
# for querying crypto related APIs and copy it into the image so it can be used by the
# code in this repo.
WORKDIR /app
RUN mkdir crypto_apis
RUN git clone https://github.com/mcIovin/crypto-related-python-apis.git crypto_apis/
ENV PYTHONPATH "${PYTHONPATH}:/app/crypto_apis/"

# create a src directory in the image. When a container is run based on this
# images the local 'src' directory in the host should be mounted to this
# directory in the container.
RUN mkdir src

# use a script to execute a container
COPY entrypoint_commands.sh /app/entrypoint_commands.sh
RUN chmod +x /app/entrypoint_commands.sh
ENTRYPOINT ["/app/entrypoint_commands.sh"]
