#!/usr/bin/env python

import sys
from collections import deque
from pprint import pprint
from urllib import parse

import click
from googleapiclient.errors import HttpError

from ytscraper.helper.configfile import update_config
from ytscraper.helper.echo import echoe, echov, echow
from ytscraper.helper.export import export_to_csv, export_to_sql, filter_text
from ytscraper.helper.yt_api import (
    get_youtube_handle,
    related_search,
    video_info,
    video_search,
)

verbose = False


@click.command()
@click.argument(
    "search-type",
    default="term",
    type=click.Choice(["term", "url", "id", "input"]),
)
@click.argument("query", nargs=1, required=True)
@click.option(
    "--number",
    "-n",
    multiple=True,
    type=click.IntRange(1, 50),
    help="Number of videos fetched per level.",
)
@click.option(
    "--max-depth",
    "-d",
    type=click.IntRange(0, 100),
    help="Maximal number of recursion steps.",
)
@click.option(
    "--api-key", "-k", type=str, help="API Key to use YouTube API v3."
)
@click.option(
    "--output-dir",
    "-o",
    type=click.Path(file_okay=False, writable=True),
    default="",
    help="Path to directory where output files are saved.",
)
@click.option(
    "--output-format",
    "-f",
    type=click.Choice(["csv", "sql"]),
    help="The file format of output files.",
)
@click.option(
    "--output-name",
    "-b",
    type=str,
    help="The name prefix of the output files.",
)
@click.option(
    "--region-code",
    "-r",
    type=str,
    help="Return only videos that are unrestricted in a specified region.",
)
@click.option(
    "--lang-code",
    "-l",
    type=str,
    help="Return videos mostly relevant to a specified language.",
)
@click.option(
    "--safe-search",
    "-s",
    type=click.Choice(["none", "moderate", "strict"]),
    help="Return filtered results.",
)
@click.option(
    "--encoding",
    "-e",
    type=click.Choice(["ascii", "utf-8", "smart"]),
    help="Transforms text to another encoding.",
)
@click.option(
    "--unique",
    "-u",
    is_flag=True,
    default=False,
    help="Do not process nodes again.",
)
@click.pass_context
def search(context, search_type, query, **options):
    """Searches YouTube using a specified query."""

    global verbose
    verbose = context.obj["verbose"]

    config = get_config(context, options)
    validate(config)

    rename = {
        "region_code": "regionCode",
        "lang_code": "relevanceLanguage",
        "safe_search": "safeSearch",
    }
    api_options = {rename[key]: config[key] for key in rename if config[key]}
    handle = get_handle(config["keys"])

    start_videos = get_starter_videos(
        config, handle, api_options, search_type, query
    )
    nodes = build_nodes(config, handle, api_options, start_videos)
    # Filter nodes
    for node in nodes:
        for key in node:
            if isinstance(node[key], str):
                node[key] = filter_text(node[key], encoding=config["encoding"])

    if config["output_dir"] and config["output_format"] == "csv":
        echov("Query finished! Start exporting files to CSV!", verbose)
        export_to_csv(nodes, config["output_dir"], config["output_name"])
        echov(f"Exported results to: " + config["output_dir"])

    if config["output_dir"] and config["output_format"] == "sql":
        echov("Query finished! Start exporting files to SQL!", verbose)
        export_to_sql(nodes, config["output_dir"], config["output_name"])
        echov(f"Exported results to: " + config["output_dir"])

    if not config["output_dir"] or verbose:
        echov("Result:")
        for node in nodes:
            print(
                "    " * node["depth"],
                f"Depth: {node['depth']}, Rank: {node['rank']}, ID: {node['videoId']}",
            )
            print("    " * node["depth"], f"           Title: {node['title']}")
            print(
                "    " * node["depth"],
                "           Related Videos: {}".format(
                    node.get("relatedVideos")
                ),
            )


def get_config(context, options):
    """ Reads the configuration file and updates it
    with the given command-line options. """
    config = context.obj["config"]
    echov("Updating configuration with command line options.", verbose)

    update_config(config, options)
    echov("Done! Working with the following configuration:", verbose)
    if verbose:
        pprint(config)
    return config


def validate(config):
    """ Checks validity of configuration. """
    config["max_depth"] = int(config["max_depth"])

    # Force number to be a list or a tuple
    if isinstance(config["number"], int):
        config["number"] = tuple((config["number"],))

    # Force api_key to be a list of next index / key list.
    if isinstance(config["api_key"], str):
        config["keys"] = [0, [config["api_key"]]]

    if isinstance(config["api_key"], list):
        config["keys"] = [0, config["api_key"]]


def get_handle(keys):
    """ Obtains the YouTube resource handle using an API key. """
    echov("Starting YouTube authentication.", verbose)
    if not keys:
        echoe(
            """You need to provide an API key using `--api-key`
        or the configuration file in order to query YouTube's API.
        Please see README on how to obtain such a key."""
        )
    handle = get_youtube_handle(keys)
    echov("API access established.", verbose)
    return handle


def get_starter_videos(config, handle, api_options, search_type, query):
    echov(f"Starting search using query {query}.", verbose)
    if search_type == "term":
        return video_search(handle, config["number"][0], query, **api_options)
    if search_type == "id":
        return video_info(handle, query)
    if search_type == "url":
        # Parse URL
        qterm = parse.urlsplit(query).query
        video_id = parse.parse_qs(qterm)["v"][0]
        return video_info(handle, video_id)
    if search_type == "input":
        if query == "-":
            return video_info(handle, ",".join(sys.stdin))
        else:
            with open(query) as f:
                return video_info(handle, ",".join(f))

    raise click.BadParameter("Wrong search type.")


def build_nodes(config, handle, api_options, starter_videos):
    for rank, video in enumerate(starter_videos):
        video.update({"rank": rank, "depth": 0})
    queue = deque(starter_videos)
    processed = []
    processed_ids = set()
    while len(queue) > 0:
        video = queue.popleft()
        echov(
            f"Processing video {video['videoId']} (Depth: {video['depth']}).",
            verbose,
        )
        processed.append(video)
        processed_ids.add(video["videoId"])
        if video["depth"] >= config["max_depth"]:
            video["relatedVideos"] = list()
            continue
        # Add children
        num_children = _get_branching(config["number"], video["depth"])
        while True:
            try:
                children = related_search(
                    handle, num_children, video["videoId"], **api_options
                )
                video["relatedVideos"] = list(
                    map(lambda c: c["videoId"], children)
                )
                for rank, child in enumerate(children):
                    child.update({"rank": rank, "depth": video["depth"] + 1})
                if config["unique"]:
                    queue.extend(
                        child
                        for child in children
                        if child["videoId"] not in processed_ids
                    )
                else:
                    queue.extend(children)
                break
            except HttpError as e:
                sys.tracebacklimit = 0
                echow("Http error received:")
                echow(e)
                handle = get_youtube_handle(api_options["keys"])

    return processed


def _get_branching(container, index):
    """ Returns the nearest valid element from an interable container.

    This helper function returns an element from an iterable container.
    If the given `index` is not valid within the `container`,
    the function returns the closest element instead.

    Parameter
    ---------
        container:
            A non-empty iterable object.
        index:
            The index of an element that should be returned.

    Returns
    -------
        object
            The closest possible element from `container` for `index`.

    Example
    -------
    The `container` can be an arbitrary iterable object such as a list::

        l = ['a', 'b', 'c']
        c1 = _get_clamped_index(l, 5)
        c2 = _get_clamped_index(l, 1)
        c3 = _get_clamped_index(l, -4)

    The first call of the function using an index of 5 will return element 'c',
    the second call will return 'b' and the third call will return 'a'.
    """
    maximal_index = len(container) - 1
    minimal_index = 0
    clamped_index = min(maximal_index, index)
    clamped_index = max(minimal_index, clamped_index)
    return container[clamped_index]

    # except HttpError as e:
