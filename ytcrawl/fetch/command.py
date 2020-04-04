#!/usr/bin/env python

import click
from click_helper import common_params
from color_helper import info


@click.command()
@common_params
@click.argument('term')
def fetch(term, verbose):
    """ Fetches subtitles from past queries."""
    if verbose:
        click.echo(info + "Starting YTcrawl's fetching mode.")
