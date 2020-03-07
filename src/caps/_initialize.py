import yaml
import json
import logging
from caps import _utils

class NoAliasDumper(yaml.Dumper):
    def ignore_aliases(self, data):
        return True


def initialize(inputs=0, outputs=0, parameters=0):
    try:
        with open("./files/initialize_schema.json", "r") as fp:
            json_obj = json.load(fp)
    except FileNotFoundError:
        logging.error("Cannot initialize unless your cd is in the src file. (this should be changed to work in any dir)")

    template_obj = {}
    if inputs > 0:
        template_obj["hasInput"] = []
        for _ in range(inputs):
            template_obj["hasInput"].append(json_obj["schema"]["DatasetSpecification"])

    if outputs > 0:
        template_obj["hasOutput"] = []
        for _ in range(outputs):
            template_obj["hasOutput"].append(json_obj["schema"]["DatasetSpecification"])

    if parameters > 0:
        template_obj["hasParameter"] = []
        for _ in range(parameters):
            template_obj["hasParameter"].append(json_obj["schema"]["Parameter"])

    try:
        with open("./insertion_template.yaml", "w") as fp:
            yaml.dump(template_obj, fp, Dumper = NoAliasDumper)

        logging.info("Generated the insertion template file in the root directory")
    except Exception as e:
        logging.error(str(e))
        quit()


def _main():
    _utils.init_logger()
    logging.info("Running from main")
    logging.info("Hmm, no one has put code in _initialize.py's main function. Quitting")


if __name__ == "__main__":
    try:
        _main()
    except Exception as e:
        logger.exception(e)