import yaml
import json
import logging
from caps import _utils, _transform_data
import requests
import modelcatalog
from modelcatalog.rest import ApiException
from pprint import pprint
import ast
from pathlib import Path
import os
import configparser

__DEFAULT_MINT_API_CREDENTIALS_FILE__ = "~/.mint_api/credentials"

def push(yaml_file_path, profile):

    credentials_file = Path(
        os.getenv("MINT_API_CREDENTIALS_FILE", __DEFAULT_MINT_API_CREDENTIALS_FILE__)
    ).expanduser()
    
    credentials = configparser.ConfigParser()
    credentials.optionxform = str

    if credentials_file.exists():
        credentials.read(credentials_file)
    
    username = credentials[profile]["api_username"]
    password = credentials[profile]["api_password"]

    try:
        transformed_json = _transform_data.create_json(yaml_file_path)
    except FileNotFoundError:
        logging.error("Could not fine \"" + yaml_file_path + "\" please for typos in path name")
        quit()

    # Login the user into the API to get the access token
    api_instance = modelcatalog.DefaultApi()
    configuration = modelcatalog.Configuration()

    try:
        api_response = api_instance.user_login_get(username, password)
        pprint(api_response)
        data = json.dumps(ast.literal_eval(api_response))
        access_token = json.loads(data)["access_token"]
        configuration.access_token=access_token

    except ApiException as e:
        logging.error("Exception when calling DefaultApi->user_login_get: %s\n" % e)
        quit()

    api_instance = modelcatalog.ModelConfigurationApi(modelcatalog.ApiClient(configuration))

    try:
        # Create a ModelConfiguration
        api_response = api_instance.modelconfigurations_post(username, model_configuration=transformed_json)
        print(api_response)
        pprint(api_response)
    except ApiException as e:
        logging.error("Exception when calling ModelConfigurationApi->modelconfigurations_post: %s\n" % e)
        quit()


def _main():
    _utils.init_logger()
    logging.info("Running from main")
    logging.info("Hmm, no one has put code in _push.py's main function. Quitting")


if __name__ == "__main__":
    try:
        _main()
    except Exception as e:
        logger.exception(e)
