import logging
from caps import _utils, _metadata_schema
import os


# class NoAliasDumper(yaml.Dumper):
#     def ignore_aliases(self, data):
#         return True


def initialize(inputs=0, outputs=0, parameters=0, dir=None, force=False):

    outp = ""
    name = None

    # Checks if directory is given. Uses cd if none given
    if dir is None:
        path = os.getcwd()
    else:
        path = dir

    # If user did not give a name in dir then we will proved a default one
    hasName = os.path.splitext(path)
    if len(hasName[1]) <= 0:
        path = os.path.join(path, "caps_outline.yaml")

    # Checks if file already exists
    if os.path.isfile(path):
        logging.warning("\"" + path + "\" already exists")
        if not force:
            logging.info("Aborting YAML Generation. Use flag -f to force override")
            quit()
        else:
            logging.info("Overriding existing file")
            os.remove(path)

    # Checks if directory exists and finds file
    stream = None
    try:
        stream = open(path, 'w+')
    except FileNotFoundError:
        logging.error("Path does not exist.")
        quit()

    # Creates human readable text from _metadata_schema.py
    outp += _metadata_schema.get_hr_metadata()

    # Generate inputs outline
    if inputs > 0:
        outp += "\nhasInput:\n"

    for i in range(1, inputs + 1):
        outp += _metadata_schema.get_hr_inputs(i)

    # Generate outputs outline
    if outputs > 0:
        outp += "hasOutput:\n"

    for o in range(1, outputs + 1):
        outp += _metadata_schema.get_hr_outputs(o)

    # Generate parameters outline
    if parameters > 0:
        outp += "hasParameter:\n"

    for p in range(1, parameters + 1):
        outp += _metadata_schema.get_hr_parameters(p)

    if inputs == outputs == parameters == 0:
        logging.info("This yaml has been generated with no inputs, outputs, or parameters")
        logging.info("You can generate these using flag -i,-o,-p respectively")

    stream.write(outp)
    logging.info("Generated \"%s\"" % path)


def _main():
    _utils.init_logger()
    logging.info("Running from main")
    logging.info("Hmm, no one has put code in _initialize.py's main function. Quitting")


if __name__ == "__main__":
    try:
        _main()
    except Exception as e:
        logging.exception(e)