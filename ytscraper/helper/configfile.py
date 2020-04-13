#!/usr/bin/env python

"""Helper class for configuration

This module contains helper functions to deal with
an external configuration file based on TOML.

It contains a function to load the configuration file into
a python dictionary and another function to update
and existing dictionary.

    * load_config - Load a user config file from standard config directory.
    * update_config - Update an existing dictionary with some provided values.
"""
import os

import click
import toml

from ytscraper.helper.echo import echow

_APP_NAME = "YouTube Scraper"
DEFAULT_OPTIONS = {
    "verbose": False,
    "number": 1,
    "max_depth": 0,
    "api_key": "",
    "output_dir": "",
    "output_format": "csv",
    "output_name": "",
    "region_code": "de",
    "lang_code": "de",
    "safe_search": "none",
    "encoding": "utf-8",
    "unique": False,
}


def load_config(config_path=None):
    r"""Processes and returns the user configuration.

    This function reads a TOML configuration file from either a provided
    path or the standard configuration directory and returns it.

    Parameters
    ----------
    config_path: str, optional
        The file path to the configuration file. If not specified,
        the method tries to read the default system-specific
        configuration directory.

    Returns
    -------
    dict
        Configuration dictionary.

    Notes
    -----
        The standard configuration directory is system specific:
        - Mac OS X: "~/Library/Application Support/YouTube Scraper"
        - Unix: "~/.config/youtube-scraper"
        - Windows: C:\Users\<user>\AppData\Roaming\YouTube Scraper
    """
    if config_path:
        config = toml.load(config_path)
    else:
        try:
            config_path = _get_default_config_path()
            config = toml.load(config_path)
        except FileNotFoundError:
            echow("Configuration file not found:")
            echow(str(config_path))
            if click.confirm("Do you want to create a default configuration?"):
                config_path = _get_default_config_path(create=True)
                config = toml.load(config_path)
            else:
                config = {}

    return config


def write_config(config, config_path=None):
    # Check for valid keys
    for key in config:
        if key not in DEFAULT_OPTIONS:
            raise click.BadArgumentUsage(
                f"{key} is not a valid configuaration key!\n \
                        Allowed keys are:\n{list(DEFAULT_OPTIONS)}"
            )
    # Check if path is given
    if not config_path:
        config_path = _get_default_config_path()
    # Write config file
    with open(config_path, "w") as f:
        toml.dump(config, f)


def update_config(config, options={}):
    """ Updates a configuration dictionary and inserts default values.

        Parameters
        ----------
        config: dict
            A dictionary that should be updated.
        options: dict
            Values that should be put into `config`.
    """
    for key, value in options.items():
        if value or value == 0:
            if key in DEFAULT_OPTIONS:
                config[key] = value
            else:
                echow(f"Invalid option given: {key}")
    for key in DEFAULT_OPTIONS:
        if key not in config:
            config[key] = DEFAULT_OPTIONS[key]


def _get_default_config_path(create=False):
    config_dir = click.get_app_dir(_APP_NAME, roaming=True)
    config_path = os.path.join(config_dir, "config.toml")
    if create and not os.path.exists(config_dir):
        os.makedirs(config_dir)
        with open(config_path, "w"):
            pass
    return config_path
