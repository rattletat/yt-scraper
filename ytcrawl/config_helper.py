#!/usr/bin/env python

import click
import yaml
import os

APP_NAME = 'ytcrawl'

def load_config(base_dic, config_path=None):
    """ Fetches and returns an updated configuration dictionary.

    This function reads a YAML configuration file from either a provided
    path or the standard configuration directory. This configuration is 
    updated using the values provided by the `base_dic` parameter and then
    returned.

    Parameters
    ----------
    base_dic: dict
        Specifies configuration values that should replace or update those
        found in the configuration file.
    config_path: str, optional
        An optional file path to the configuration file if it is not in the
        default system-specific configuration folder.

    Returns
    -------
    dict
        Updated configuration values in a dictionary.
    """
    if config_path:
            config = yaml.safe_load(open(config_path))
    else:
        try:
            default_config_folder = click.get_app_dir(APP_NAME)
            default_config_path = os.path.join(default_config_folder, 'config.yml')
            config = yaml.safe_load(open(default_config_path))
        except FileNotFoundError:
            config = {}

        # TODO
        for key, value in base_dic.items():
            if value is not None:
                config[key] = value
    return config
