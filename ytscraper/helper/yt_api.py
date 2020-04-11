#!/usr/bin/env python

"""Helper class for communicating with YouTube API v3

This module contains helper function to communicate with
Google"s YouTube API v3.
"""

import re

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from ratelimit import limits, sleep_and_retry

from ytscraper.helper.echo import echoe, echow


def related_search(handle, number, videoId, **api_options):
    api_options["relatedToVideoId"] = videoId
    api_options["maxResults"] = number + 1
    return _search(handle, number, **api_options)


def video_search(handle, number, search_term, **api_options):
    api_options["q"] = search_term
    api_options["maxResults"] = number
    return _search(handle, number, **api_options)


def _search(handle, number, **api_options):
    api_options["type"] = "video"
    api_options["part"] = "id,snippet"
    response = _get_response(handle.search(), **api_options)
    video_data = [_extract_data(video) for video in response["items"]]
    if len(video_data) < number:
        echow(
            f"API gave less number of videos than requested: {len(video_data)} instead of {number}!"
        )
    return video_data[:number]


def video_info(handle, video_id, **api_options):
    api_options["id"] = video_id
    api_options["part"] = "id,snippet"
    response = _get_response(handle.videos(), **api_options)
    video_data = [_extract_data(video) for video in response["items"]]
    return video_data


@sleep_and_retry
@limits(3_000_000, 100)
def _get_response(mod_handle, **api_options):
    return mod_handle.list(**api_options).execute()


def _extract_data(item):
    result = {}
    if "id" in item:
        # Result between search term and relatedToVideoId differs
        try:
            result["videoId"] = item["id"]["videoId"]
        except TypeError:
            result["videoId"] = item["id"]
    if "snippet" in item:
        result["channdelId"] = item["snippet"]["channelId"]
        result["title"] = item["snippet"]["title"]
        result["description"] = item["snippet"]["description"]
        result["publishedAt"] = item["snippet"]["publishedAt"]
        result["channelTitle"] = item["snippet"]["channelTitle"]
    return result


def get_youtube_handle(api_key):
    """ Returns the YouTube Data API v3 handle.

    Parameter
    ---------
    api_key: str
        An authorized API key.

    Returns
    -------
        An object for interacting with the YouTube API v3 service.
    """
    try:
        return build("youtube", "v3", developerKey=api_key)
    except HttpError:
        echoe(
            """ There was an error while connecting to the YouTube API.
        Please check your API key."""
        )
