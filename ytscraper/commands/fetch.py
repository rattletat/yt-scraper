#!/usr/bin/env python

import click

from ytscraper.helper.echo import echoe, echov


@click.command()
@click.pass_context
def fetch(context):
    """ Fetches subtitles from past queries."""
    # config = context['config']
    verbose = context.obj["verbose"]
    echov("Starting YTcrawl's fetching mode.", verbose)
    echoe("Not implemented yet!")
