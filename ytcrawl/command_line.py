#!/usr/bin/env python

import click

from query import command as query
from fetch import command as fetch


@click.group()
def entry_point():
    pass

entry_point.add_command(query.query)
entry_point.add_command(fetch.fetch)

if __name__ == "__main__":
    entry_point()
