import unittest
import logging
import logging.config
import json
import ast

from pathlib import Path
from flask_testing import TestCase
from click.testing import CliRunner
from src.caps import __main__
from deepdiff import DeepDiff

import requests
import modelcatalog
from modelcatalog.rest import ApiException

logging_file = Path(__file__).parent.parent / "settings" / "logging.ini"
try:
    logging.config.fileConfig(logging_file)
except:
    logging.error("Logging config file does not exist {}".format(logging_file))
    exit(0)
logger = logging.getLogger(__name__)


username = "dhruvrpa@usc.edu"
password = "hRQo2ZdpCa836Q"

def make_request(request_uri, request_type, access_token, params):
    if request_type == "GET":
        headers = {"content-type": "application/json", "Authorization": "Bearer " + access_token}
        response = requests.get(request_uri, params = params, headers = headers)
        return response


def recursive_items(dictionary):
        if type(dictionary) is dict:
            for key, value in dictionary.items():
                    if type(value) is dict:
                        recursive_items(value)
                    elif type(value) is list:
                        for l in value:
                            recursive_items(l)
                    elif type(value) is str:
                        if key == 'id':
                            if("/w3id.org" in dictionary[key]):
                                dictionary[key] =  dictionary[key].split("/")[-1]
        return dictionary

class TestCapsCliCommands(unittest.TestCase):
    def test_configure_command(self):
        runner = CliRunner()
        result = runner.invoke(__main__.configure, ['--profile', 'test_profile'], input="mlsnfklsd\nkjahdkasj")
        self.assertEqual(result.exit_code, 0)


    def test_push_command_without_setup(self):
        
        # For current testing implementation please create a profile named dhruv with the above username and password

        runner = CliRunner()
        result = runner.invoke(__main__.push, ['--profile', 'dhruv', 'false', './examples/ModelConfigExample.yaml'])

        with open("./src/caps/tests/metadata/test_push_wo_setup_data.json") as f:
            input_data = json.loads(f.read())
        
        with open("./src/caps/tests/metadata/test_push_wo_setup_id.txt") as f:
            generated_id = f.read()
        
        # Verify if request and response are equal
        configuration = modelcatalog.Configuration()
        user_api_instance = modelcatalog.DefaultApi()

        if username and password:
            try:
                api_response = user_api_instance.user_login_get(username, password)
                data = json.dumps(ast.literal_eval(api_response))
                access_token = json.loads(data)["access_token"]
                configuration.access_token = access_token
            except ApiException as e:
                logging.info("Exception when calling DefaultApi->user_login_get: %s\n" % e)
        else:
            log.error("There is some issue while getting the username and password")
            exit(1)


        api_instance = modelcatalog.ModelConfigurationApi(modelcatalog.ApiClient(configuration))
        api_response = api_instance.custom_modelconfigurations_id_get(generated_id,username=username)
        
        #api_response = make_request("https://api.models.mint.isi.edu/v1.4.0/custom/modelconfigurations/" + generated_id, "GET", access_token, {"username": username})

        input_data["id"] = "https://w3id.org/okn/i/mint/" + generated_id
        #print(input_data)

        #print(api_response.to_dict())
        # input_data['author']=[]
        # input_data['contributor']=[]
        response = api_response.to_dict()
        res = recursive_items(response)
        #print(res)
        # response['author']=[]
        # response['contributor']=[]
        # input_data['type']=[]
        # response['type']=[]

        # print(input_data)
        # print(response)
        #
        #diff = DeepDiff(input_data, response, ignore_order=True)
        #logging.info(diff)

        # logger.info("Input Data")
        # logger.info(input_data)
        # logger.info("Response Data")
        # print(api_response.json())
        # if diff:
        #     logger.info("Mismatches {}".format(diff))

        #self.assertEqual(dict(diff), {})
        self.assertEqual(result.exit_code, 0)

if __name__ == '__main__':
    unittest.main()

