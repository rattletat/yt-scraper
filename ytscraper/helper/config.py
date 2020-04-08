#!/usr/bin/env python

import os
from pathlib import Path

import click
import toml
from ytscraper.helper.echo import warning

APP_NAME = "YouTube Scraper"


def update_config(config, options):
    """ Updates a configuration dictionary.

        Parameters
        ----------
        config: dict
            A dictionary that should be updated.
        options: dict
            Values that should be put into `config`.
    """
    for key, value in options.items():
        if value:
            config[key] = value


def load_config(config_path=None):
    r"""Processes and returns the user configuration.

    This function reads a TOML configuration file from either a provided
    path or the standard configuration directory and returns it.

    Parameters
    ----------
    config_path: str, optional
        The file path to the configuration file. If not specified, 
        the method tries to read the default system-specific 
        configuration folder.

    Returns
    -------
    dict
        Configuration dictionary.

    Notes
    -----
        The standard configuration directory is system specific:
        - Mac OS X: "~/Library/Application Support/YouTube Scraper"
        - Unix: "~/.config/youtube-scraper"
        - Win7: C:\Users\<user>\AppData\Roaming\YouTube Scraper
    """
    if config_path:
        config = toml.load(config_path)
    else:
        try:
            config_folder = click.get_app_dir(APP_NAME, roaming=True)
            config_path = os.path.join(config_folder, 'config.toml')
            config = toml.load(config_path)
        except FileNotFoundError:
            click.echo(warning + "Configuration file not found:")
            click.echo(warning + config_path)
            config = {}

    return config
