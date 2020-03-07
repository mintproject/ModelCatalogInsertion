import yaml
import json
import logging
from caps import _utils, _transform_data
import requests
import modelcatalog
from modelcatalog.rest import ApiException
from pprint import pprint
import ast

def push(yaml_file_path):

    try:
        transformed_json = _transform_data.create_json(yaml_file_path)
    except FileNotFoundError:
        logging.error("Could not fine \"" + yaml_file_path + "\" please for typos in path name")
        quit()

    configuration = modelcatalog.Configuration()
    user_api_instance = modelcatalog.DefaultApi()
    username = "dhruvrpa@usc.edu"
    password = "hRQo2ZdpCa836Q"
    # Login the user into the API to get the access token
    api_instance = modelcatalog.DefaultApi()


    configuration = modelcatalog.Configuration()
# Configure Bearer authorization (JWT): BearerAuth

    try:
        api_response = api_instance.user_login_get(username, password)
        pprint(api_response)
        data = json.dumps(ast.literal_eval(api_response))
        access_token = json.loads(data)["access_token"]
        configuration.access_token=access_token

    except ApiException as e:
        logging.error("Exception when calling DefaultApi->user_login_get: %s\n" % e)
        quit()

    # create an instance of the API class
    #modelcatalog.ApiClient().deserialize(transformed_json,modelcatalog.ModelConfiguration())
    api_instance = modelcatalog.ModelConfigurationApi(modelcatalog.ApiClient(configuration))
    #user = 'user_example' # str | Username
    #model_configuration = modelcatalog.ModelConfiguration() # ModelConfiguration | A new ModelConfigurationto be created (optional)

    try:
        # Create a ModelConfiguration
        api_response = api_instance.modelconfigurations_post(username, model_configuration=transformed_json)
        print(api_response)
        pprint(api_response)
    except ApiException as e:
        logging.error("Exception when calling ModelConfigurationApi->modelconfigurations_post: %s\n" % e)
        quit()

    #logging.info(json.dumps(transformed_json))


def _main():
    _utils.init_logger()
    logging.info("Running from main")
    logging.info("Hmm, no one has put code in _push.py's main function. Quitting")


if __name__ == "__main__":
    try:
        _main()
    except Exception as e:
        logger.exception(e)
