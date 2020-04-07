#!/usr/bin/env python

import click

from fetch import command as fetch
from query import command as query


@click.group()
def entry_point():
    pass


entry_point.add_command(query.query)
entry_point.add_command(fetch.fetch)

if __name__ == "__main__":
    entry_point()
