import configparser
import logging
import os
import sys
from pathlib import Path

import click

import semver

import caps
from caps import _utils, _metadata_schema

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
    print(inputs, outputs, parameters)


def push():
    pass

@cli.command(help="Validate the JSON obtained after creating one")
@click.argument("metadata_file_path", default=None, type=str)
def validate(metadata_file_path):
    _metadata_schema.validate_file(metadata_file_path)

