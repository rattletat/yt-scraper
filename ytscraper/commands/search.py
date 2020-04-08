#!/usr/bin/env python

from collections import deque
from pprint import pprint
from urllib import parse

import click

from ytscraper.helper.config import update_config
from ytscraper.helper.echo import echoe, echov
from ytscraper.helper.node import build_node_list
from ytscraper.helper.yt_api import get_search_videos, get_youtube_handle


@click.command()
@click.argument('search-type',
                default='query',
                type=click.Choice(['term', 'url', 'id']))
@click.argument('query', 
        nargs=1, 
        required=True)
@click.option('--number',
              '-n',
              multiple=True,
              type=click.IntRange(1, 50),
              help='Number of videos fetched per level.')
@click.option('--depth',
              '-d',
              help='Number of recursion steps.')
@click.option('--api-key',
              '-k',
              type=str,
              help='API Key to use YouTube API v3.')
@click.pass_context
def search(context, search_type, query, **options):
    """Searches YouTube using a specified query."""
    config = context.obj

    # CONFIGURATION
    echov("Updating configuration with command line options.", config['verbose'])
    update_config(config, options)
    echov("Done! Working with the following configuration:", config['verbose'])
    if config['verbose']:
        pprint(config)

    # AUTHENTICATION
    echov("Starting YouTube authentication.", config['verbose'])
    if 'api_key' not in config:
        echoe("""You need to provide an API key using `--api-key` 
        or the configuration file in order to query YouTube's API.
        Please see README on how to obtain such a key.""")
    handle = get_youtube_handle(config['api_key'])
    echov("API access established.", config['verbose'])

    # ARGUMENT PARSING
    if search_type == 'term':
        echov("Starting search using query {query}.", config['verbose'])
        start_ids = get_search_videos(handle, query, config['number'][0])
    elif search_type == 'id':
        echov("Starting search using video id {query}.", config['verbose'])
        start_ids = [query]
    elif search_type == 'url':
        echov("Starting search using the following video url:", config['verbose'])
        echov(query, config['verbose'])
        qterm = parse.urlsplit(query).query
        video_id = parse.parse_qs(qterm)['v']
        start_ids = [video_id]

    # QUERY
    node_list = build_node_list(handle, start_ids, 0, config['number'][0])
    node_queue = deque(node_list)
    processed_nodes = []
    while True:
        if len(node_queue) == 0:
            break
        node = node_queue.popleft()
        processed_nodes.append(node)
        echov('Current Video: ' + node.videoId, config['verbose'])
        if node.depth < config['depth']:
            # Clamp level_branch index to specified branch array.
            number = config['number'][max(0, min(node.depth + 1, len(config['number'])-1))]
            new_nodes = build_node_list(handle, node.relatedVideos,
                                        node.depth + 1, number)
            node_queue.extend(new_nodes)

    echov("Query finished! Result:")
    for node in processed_nodes:
        pprint(node)

    # TODO Save to file
