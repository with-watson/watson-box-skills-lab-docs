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

import json
import os

from src.action import Action
from src.storage import Storage


def main(args):
    """Coordinate the skill. Main function called in IBM Cloud Functions"""
    ### Helper Functions ###

    def do_cleanup(paths: list) -> None:
        """Cleanup the leftover paths

           Args:
                paths: a list of paths to clean up
        """
        for path in paths:
            os.remove(path)

    def get_config(config_file_path: str) -> dict:
        """Load the skill config

           Args:
                config_file_path: location of config file
        """
        config = {}
        with open(config_file_path) as config_file:
            config = json.load(config_file)
        return config

    ### Main Function ###

    # Get args
    request_body = args
    config_file = args.get('config', './config.json')
    config = get_config(config_file)

    # # Build pieces
    storage = Storage(config, request_body)
    action = Action(config)

    # # Download --> ACTION --> Upload
    file_data = storage.file_data  # {name: "", id: 0000}
    file_path = storage.download_file()

    # Run Action
    action.do_action(file_path, file_data['id'])

    # Upload/Update new file
    results = action.push2storage(storage)

    # Clean up local files
    do_cleanup([file_path])

    # Return status
    return {"status":"success"}
