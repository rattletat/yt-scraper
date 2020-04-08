#!/usr/bin/env python

import functools
import sys

import click


class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'


class markup:
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


info = markup.BOLD + color.PURPLE + "[STATUS] " + markup.END
usage = markup.BOLD + color.YELLOW + "[USAGE] " + markup.END
fail = markup.BOLD + color.RED + "[ERROR] " + markup.END
warning = markup.BOLD + color.YELLOW + "[WARNING] " + markup.END


def echov(text, verbose=True, nl=True):
    """ Wraps around click.echo and expands it by a `verbose` option.

    Parameter
    ---------
    text: str
        Text that is printed to standard output.
    verbose: {True, False}, optional
        Determines whether something is printed at all.
    nl: {True, False}, optional
        If set, a new line is added to the output.
    """
    if verbose:
        click.echo(info + text, nl=nl)


def echoe(text):
    """ Prints text to error output using click.echo and exits.

    Parameter
    ---------
    text: str
        Text that is printed to error output.
    """
    click.echo(fail + text, err=True)
    sys.exit(1)
