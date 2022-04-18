# get-affe-data

A repository to query as much metadata as possible about AmW while it is still in the 1155 Opensea Storefront contract.

**HOW TO USE THIS REPO**

For convenience, a Dockerfile is provided, along with some useful bash scripts.
These instructions have only been written for Ubuntu based systems (they do work
on Windows, but have only been tested with a Docker installation based on WSL2.)

Pre-requisites:
- Have a working installation of Docker, and have Docker up and running.
- In the same directory where this repo is cloned to, create the following...
  - an empty folder called: data/
  - an env file called: local.env
    - This file should contain the Moralis API key of the person using this repo,
    as well as the path to the data folder WITHIN the container, which should not
    change unless you are going to customize this repo locally for your own needs.
    You should be able to copy the two lines below, exactly as-is, to create
    your own local.env file (and simply add your API key.)
------
DATA_PATH=/app/data

MORALIS_KEY=addYourOwnKeyHere

------
Again, unless your are customizing the docker build/run, you should not need to
modify that DATA_PATH above. This is a path **within** the docker container.

(NOTE! - The data directory, and the local.env file do not necessarily need to
reside in the same folder as this repo is copied to. However, if they are not
placed in the same directory the provided bash scripts will not work out-of-the-box
so it is recommended to place them in the same directory for ease of use.)

HOW TO EXECUTE THE CODE AND GET AFFE DATA
1) Clone the repository to your local environment.
2) Change directory into the folder where the repo was downloaded to.
3) Make the bash scripts executable by typing:

chmod +x bash_*


4) Build the docker image by typing:

./bash_script_1_docker_build.sh


5) Run the docker image by typing:

bash_script_2_docker_run.sh

**RESULTS**

Results will be placed in the data/ directory.
Any files used for intermediate steps will be in data/intermediate_files/ and
the file withe the fully compiled results will be in data/output/
