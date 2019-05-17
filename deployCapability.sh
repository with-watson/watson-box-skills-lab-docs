#!/bin/bash -e
# Copyright 2019 IBM All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

if [ -z "$1" ]
  then
    echo "Usage: ./deployCapability.sh <ACTION NAME>"
    exit 1
fi

docker run --rm -v "$PWD:/tmp" ibmfunctions/action-python-v3.7 bash -c "cd /tmp && virtualenv virtualenv && source virtualenv/bin/activate && pip install -r requirements.txt"
zip -r $1.zip virtualenv __main__.py ./src/action.py ./src/storage.py config.json ./src/bsk_utils.py ./src/__init__.py
ibmcloud fn action update $1 --kind python:3.7 $1.zip --web true --timeout 600000
date

rm $1.zip
