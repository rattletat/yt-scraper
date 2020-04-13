#!/usr/bin/env python

import click

from ytscraper.commands import config, search
from ytscraper.helper.configfile import load_config, update_config
from ytscraper.helper.echo import echov


@click.group()
@click.option("--config-path", "-c", type=click.Path(), help="YAML configuration file.")
@click.option("--verbose", "-v", is_flag=True, help="Show more output.")
@click.version_option(None, "--version", "-V", message=f"Version: %(version)s")
@click.pass_context
def run(context, config_path, verbose):
    echov("Reading configuration file.", verbose)
    context.obj = {}
    context.obj["config"] = load_config(config_path)
    context.obj["verbose"] = verbose
    context.obj["config_path"] = config_path


run.add_command(search.search)
run.add_command(config.config)
