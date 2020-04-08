#!/usr/bin/env python

import click

from ytscraper.helper.echo import echov, echoe


@click.command()
@click.argument('term')
@click.pass_context
def fetch(context, term):
    """ Fetches subtitles from past queries."""
    # config = context['config']
    verbose = context.obj['verbose']
    echov("Starting YTcrawl's fetching mode.", verbose)
    echoe("Not implemented yet!")
