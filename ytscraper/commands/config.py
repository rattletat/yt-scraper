#!/usr/bin/env python

import ast
from pprint import pprint

import click

from ytscraper.helper.configfile import (
    DEFAULT_OPTIONS,
    load_config,
    write_config,
    update_config,
)
from ytscraper.helper.echo import echov, echow


@click.group()
@click.pass_context
def config(context):
    """ Shows and modifies default configurations. """
    verbose = context.obj["verbose"]
    echov("Starting YTcrawl's config mode.", verbose)
    echov("Read the following configuration:", verbose)
    if verbose:
        pprint(context.obj["config"])
    pass


@config.command()
@click.argument("option", type=click.Choice(DEFAULT_OPTIONS), metavar="KEY")
@click.argument("value")
@click.pass_context
def set(context, option, value):
    """ Sets default options."""
    config = context.obj["config"]
    verbose = context.obj["verbose"]
    config_path = context.obj["config"]["config_path"]

    try:
        value = ast.literal_eval(value)
    except:
        if value == "true":
            value = True
        if value == "false":
            value = False
    # TODO does not support List or Tuple types
    target_type = type(DEFAULT_OPTIONS[option])
    if not isinstance(value, target_type):
        raise click.BadArgumentUsage(
            f"Given value '{value}' is not a valid type for '{option}'. Please provide type '{target_type.__name__}'."
        )
    elif target_type is int and value < 0:
        raise click.BadArgumentUsage(
            f"Given integer '{value}' is negative! Please provide a non-negative value.."
        )

    config[option] = value
    echov("The new configurations file is:", verbose)
    if verbose:
        pprint(config)
    write_config(config, config_path)
    echov("Successfully changed!")


@config.command()
@click.argument("option", type=click.Choice(DEFAULT_OPTIONS), metavar="KEY")
@click.pass_context
def unset(context, option):
    """ Unsets a default option."""
    config = context.obj["config"]
    verbose = context.obj["verbose"]
    config_path = context.obj["config"]["config_path"]

    if option in config:
        del config[option]

    echov("The new configurations file is:", verbose)
    if verbose:
        pprint(config)
    write_config(config, config_path)
    echov("Successfully written!")


# TODO: Add all: to show everything
@config.command()
@click.argument("option", type=click.Choice(DEFAULT_OPTIONS), metavar="KEY")
@click.pass_context
def get(context, option):
    """ Shows a default option."""
    config = context.obj["config"]
    update_config(config)
    if option in config:
        echov(f"The value of '{option}' is set to '{config[option]}'.")
    else:
        echow(f"The value of '{option}' is not set!")


@config.command()
@click.pass_context
def clear(context):
    """ Clears all configurations. """
    config_path = context.obj["config"]["config_path"]

    if click.confirm(f"Do you really want to clear the configuration file?"):
        # Erase content of configuration file
        write_config({}, config_path)
        echov("Configuration file cleared!")
    else:
        echov("Aborted! Nothing changed.")


@config.command()
@click.pass_context
def show(context):
    """ Clear all configurations. """
    config = context.obj["config"]
    update_config(config)
    pprint(config)


@config.command()
@click.pass_context
def where(context):
    """ Shows the configuration file path. """
    config_path = context.obj["config"]["config_path"]
    print(config_path)
