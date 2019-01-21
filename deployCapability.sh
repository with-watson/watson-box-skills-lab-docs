#!/bin/bash

if [ -z "$1" ]
  then
    echo "Usage: ./deployCapability.sh <CAPABILITY NAME>"
    exit 1
fi


docker run --rm -v "$PWD:/tmp" openwhisk/python3action bash  -c "cd tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirements.txt"
zip -r $1.zip virtualenv __main__.py ./src/action.py ./src/storage.py config.json ./src/bsk_utils.py ./src/__init__.py
bx wsk action update $1 --kind python:3 $1.zip --web true --timeout 600000
date

rm $1.zip
