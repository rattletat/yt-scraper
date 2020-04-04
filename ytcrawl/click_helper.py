#!/usr/bin/env python

import click
import os
import yaml
import functools

APP_NAME = 'ytcrawl'

def common_params(func):
    @click.option('--verbose', '-v', is_flag=True, help='Show more verbose output.')
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

def echov(text, verbose=True):
    if verbose:
        click.echo(text)

def load_config(path):
    cfg = os.path.join(click.get_app_dir(APP_NAME), 'config.yml')
    return yaml.safe_load(open(cfg)) 

