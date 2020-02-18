import configparser
import logging
import os
import sys
from pathlib import Path
import json

import click

import semver

import caps
from caps import _utils, _metadata_schema, _transform_data

__DEFAULT_CAPS_CLI_CREDENTIALS_FILE__ = "~/.caps-cli/credentials"


@click.group()
@click.option("--verbose", "-v", default=0, count=True)
def cli(verbose):
    _utils.init_logger()
    lv = ".".join(_utils.get_latest_version().split(".")[:3])
    cv = ".".join(caps.__version__.split(".")[:3])

    if semver.compare(lv, cv) > 0:
        click.secho(
            f"""WARNING: You are using caps-cli version {caps.__version__}, however version {lv} is available.
You should consider upgrading via the 'pip install --upgrade caps' command.""",
            fg="yellow",
        )


@cli.command(help="Show caps-cli version.")
def version(debug=False):
    click.echo(f"{Path(sys.argv[0]).name} v{caps.__version__}")

@cli.command(help="Create an empty JSON template to fill the data to be inserted in Model Catalog")
@click.option(
    "--inputs",
    "-i",
    type=int,
    default=0,
)
@click.option(
    "--outputs",
    "-o",
    type=int,
    default=0,
)
@click.option(
    "--parameters",
    "-p",
    type=int,
    default=0,
)
def initialize(inputs = 0, outputs = 0, parameters = 0):

    with open("template.json", "r") as fp:
        json_obj = json.load(fp.read())

    if inputs > 0:
        temp_obj = json_obj["hasInput"][0]
        json_obj["hasInput"] = []
        for _ in inputs:
            json_obj["hasInput"].append(temp)
    
    if outputs > 0:
        temp_obj = json_obj["hasOutput"][0]
        json_obj["hasOutput"] = []
        for _ in outputs:
            json_obj["hasOutput"].append(temp)
    
    if parameters > 0:
        temp_obj = json_obj["hasParameter"][0]
        json_obj["hasParameter"] = []
        for _ in parameters:
            json_obj["hasParameter"].append(temp)

@cli.command(help="Transform the input YAML into a Valid JSON for posting the file to Model Catalog")
@click.argument("yaml_file_path", default=None, type=str)
def push(yaml_file_path):
    transformed_json = _transform_data.create_json(yaml_file_path)
    print(json.dumps(transformed_json))

@cli.command(help="Validate the JSON obtained after creating one")
@click.argument("metadata_file_path", default=None, type=str)
def validate(metadata_file_path):
    _metadata_schema.validate_file(metadata_file_path)

