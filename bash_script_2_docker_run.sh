#!/bin/bash

docker run \
    --name cnt_affe \
    --rm \
    --env-file local.env \
    -v "$PWD/src":/app/src \
    -v "$PWD/data":/app/data \
    img_affe