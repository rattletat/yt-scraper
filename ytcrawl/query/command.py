#!/usr/bin/env python

import click
from click_helper import common_params, echov, load_config
# from authorization import 
from color_helper import info

@click.command()
@common_params
@click.argument('term')
@click.option('--number', '-n', default=10, 
        help='Number of videos fetched per level.')
@click.option('--level', '-l', default=1, 
        help='Number of recursion levels.')
@click.option('--api-key', '-k', 
        help='API Key to use YouTube API v3.')
@click.option('--config-path', '-c', type=click.Path(),
        help='YAML configuration file.')
def query(term, number, level, api_key, config_path, verbose):
    """Queries YouTube using the specified search term."""
    echov(info + f"Starting YTcrawl's query mode using search term '{term}'.", verbose)

    
    echov(info + "Starting YouTube authentication.", verbose)


def read_config(config_path, verbose):
    if config_path:
        echov(info + f"Reading configuration from {config_path}.", verbose)
        config = load_config(config_path)
