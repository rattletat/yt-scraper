#!/usr/bin/env python

import click
from click_helper import common_params, echov


@click.command()
@common_params
@click.argument('term')
def fetch(term, verbose):
    """ Fetches subtitles from past queries."""
    echov("Starting YTcrawl's fetching mode.", verbose)
