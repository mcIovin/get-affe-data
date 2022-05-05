#!/bin/bash

function print_a_message () {
  echo $1
}

print_a_message "-- STARTING ENTRYPOINT ACTIONS --"

# command below is simply to keep the docker container
# running. (Piping the command to a file should allow the other
# commands above to continue sending their outpot to the console,
# which is useful for seeing the ganache output on the console
# where the container was started.)

source ~/miniconda3/bin/activate
conda activate conda_env_3_10
python --version
python src/get_affe_data.py

# NOTE: The commands above can be commented-out, and the commands below
# uncommented in order to run the container in a way that won't terminate
# immediately (so it can be interacted with.) In this case, once the container
# starts, the commands above should be run manually inside the container if
# one wants to run the program.
#touch /app/log.txt
#tail -f /dev/null  > /app/log.txt