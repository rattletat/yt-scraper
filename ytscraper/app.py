from pprint import pprint

import click

from ytscraper.commands import fetch, search
from ytscraper.helper.config import load_config, update_config
from ytscraper.helper.echo import echov


@click.group()
@click.option("--config-path", "-c", type=click.Path(), help="YAML configuration file.")
@click.option("--verbose", "-v", is_flag=True, help="Show more output.")
@click.pass_context
def run(context, config_path, verbose):
    echov("Reading configuration file.", verbose)
    context.obj = {}
    update_config(context.obj, load_config(config_path))
    echov("Read the following configuration:", verbose)
    if verbose:
        pprint(context.obj)

    context.obj["verbose"] = verbose


run.add_command(search.search)
run.add_command(fetch.fetch)
