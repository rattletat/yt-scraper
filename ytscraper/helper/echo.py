#!/usr/bin/env python

"""Helper class for printing

This module contains helper functions to beautify or ease
the printing process to standard and error output.

It contains a color and a markup class, defining specific ANSI codes.
Moreover, four status badges for console output are defined,
as well as two wrapper functions around click.echo.

    * Color - color class containing ANSI color codes.
    * Markup - markup class containing ANSI markup codes.
    * echov - Wrapping around click.echo and adding a verbose option.
    * echof - Print to error output and exit afterwards.
"""
import os
import sys

import click

if sys.platform.lower() == "win32":
    os.system("color")


class _Color:
    """ A simple color class containing ANSI color codes. """

    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"


class _Markup:
    """ A simple markup class containing ANSI color codes. """

    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


_INFO = _Markup.BOLD + _Color.PURPLE + "[STATUS] " + _Markup.END
_USAGE = _Markup.BOLD + _Color.YELLOW + "[USAGE] " + _Markup.END
_FAIL = _Markup.BOLD + _Color.RED + "[ERROR] " + _Markup.END
_WARNING = _Markup.BOLD + _Color.YELLOW + "[WARNING] " + _Markup.END


def echov(text, verbose=True, new_line=True):
    """ Wraps around click.echo and expands it by a `verbose` option.

    Parameter
    ---------
    text: str
        Text that is printed to standard output.
    verbose: {True, False}, optional
        Determines whether something is printed at all.
    new_line: {True, False}, optional
        If set, a new line is added to the output.
    """
    if verbose:
        click.echo(_INFO + str(text), nl=new_line)


def echoe(text, error=None):
    """ Prints text to error output using click.echo and exits.

    Parameter
    ---------
    text: str
        Text that is printed to error output.
    """
    click.echo(_FAIL + str(text), err=True)
    if error:
        raise error
    sys.exit(1)


def echow(text):
    """ Prints text warning to standard output and prints message.

    Parameter
    ---------
    text: str
        Text that is printed to standard output.
    """
    click.echo(_WARNING + str(text))
