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

python3.9 src/get_affe_data.py
#tail -f /dev/null  > /app/null.log
