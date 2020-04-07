#!/usr/bin/env python

import click
from click_helper import common_params, echov, echof
from config_helper import load_config
from .api import get_youtube_handle, get_search_videos
from .tree import build_node_list
from collections import deque


@click.command()
@common_params
@click.argument('term')
@click.option('--number',
              '-n',
              default=10,
              type=click.IntRange(1, 50),
              help='Number of videos fetched per level.')
@click.option('--max-level',
              '-l',
              default=1,
              help='Maximal number of recursion levels.')
@click.option('--api-key',
              '-k',
              type=str,
              help='API Key to use YouTube API v3.')
@click.option('--config-path',
              '-c',
              type=click.Path(),
              help='YAML configuration file.')
def query(term, config_path, verbose, **options):
    """Queries YouTube using the specified search term."""
    echov(f"Starting YTcrawl's query mode using search term '{term}'.",
          verbose)

    # CONFIGURATION
    echov("Reading configuration file.", verbose)
    config = load_config(options, config_path)
    echov(f"Read the following values:\n{config}", verbose)

    # AUTHENTICATION
    echov("Starting YouTube authentication.", verbose)
    if 'api_key' not in config:
        echof("""You need to provide an API key using `--api-key` 
        or the configuration file in order to query YouTube's API.
        Please see README on how to obtain such a key.""")
    handle = get_youtube_handle(config['api_key'])

    # QUERY
    # TODO Support possibility of specifying number for each level
    number = config['number']
    video_ids = get_search_videos(handle, term, number)
    node_queue = deque(build_node_list(handle, video_ids, 0, number))
    processed_nodes = []
    while True:
        if len(node_queue) == 0:
            break
        node = node_queue.popleft()
        processed_nodes.append(node)
        echov('Current Video: ' + node.videoId, verbose)
        if node.level < config['max_level']:
            new_nodes = build_node_list(handle, node.relatedVideos,
                                        node.level + 1, number)
            node_queue.extend(new_nodes)

# TODO Save to file
    print("Found the following edges:")
    print(processed_nodes)
