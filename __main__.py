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
