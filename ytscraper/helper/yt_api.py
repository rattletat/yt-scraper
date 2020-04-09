#!/usr/bin/env python

"""Helper class for communicating with YouTube API v3

This module contains helper function to communicate with
Google's YouTube API v3.

It contains a method to collect the authorized API handle
and two functions to fetch search results.

    * get_youtube_handle - Retrieves the YouTube API resource handle.
    * get_search_videos - Returns video results for a given search term.
    * get_related_videos - Returns related videos for a given video.
"""

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from ratelimit import limits, sleep_and_retry

from ytscraper.helper.echo import echoe


def get_youtube_handle(api_key):
    """ Returns the YouTube Data API v3 handle.

    This method returns the handle for the YouTube Data API v3
    in order to request data.

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


@sleep_and_retry
@limits(3_000_000, 100)
def check_rate_limit():
    """ Sentinel method that limits the requests per 100 seconds. """


# TODO relevanceLanguage parameter
def get_search_videos(
    handle, search_term, max_results, region_code="de", safe_search="none"
):
    """ Returns video ids from a search using the YouTube API v3.

    Parameter
    ---------
        handle: YouTube resource object
            Needed to do authorized queries to the YouTube API.
        search_term:
            Query that is used to search for videos.
        max_results:
            The maximum number of videos to retrieve.
        region_code: str, optional, default="de"
            The search prefers videos from the region 
            indicated by the `region_code`.
        safe_search: str, optional, default="none", [none, moderate, strict]
            Whether to filter some videos based on `region_code`.

    Returns
    -------
        list(str)
            Returns a list of video ids that match the search criteria.
    """
    check_rate_limit()
    response = (
        handle.search()
        .list(
            q=search_term,
            part="id",
            type="video",
            maxResults=max_results,
            safeSearch=safe_search,
            regionCode=region_code,
        )
        .execute()
    )
    extract_video_id = lambda dictionary: dictionary["id"]["videoId"]
    video_ids = map(extract_video_id, response["items"])
    return list(video_ids)


# TODO Why is related videos so weird?
def get_related_videos(
    handle, video_id, max_results, region_code="de", safe_search="none"
):
    """ Returns video that are related to a specific video id.

    Parameter
    ---------
        handle: YouTube resource object
            Needed to do authorized queries to the YouTube API.
        video_id:
            YouTube's unique id for a specific video 
            that is used to search for related videos.
        max_results:
            The maximum number - 1 of videos to retrieve.
            This seems to be an API inconsistency.
        region_code: str, optional, default="de"
            The search prefers videos from the region 
            indicated by the `region_code`.
        safe_search: str, optional, default="none", [none, moderate, strict]
            Whether to filter some videos based on `region_code`.

    Returns
    -------
        list(str)
            Returns a list of videos that are related to the specified video id.
    """

    check_rate_limit()
    response = (
        handle.search()
        .list(
            relatedToVideoId=video_id,
            part="id",
            type="video",
            maxResults=max_results + 1,  # relatedToVideoId returns 1 less
            safeSearch=safe_search,
            regionCode=region_code,
        )
        .execute()
    )
    extract_video_id = lambda dictionary: dictionary["id"]["videoId"]
    video_ids = map(extract_video_id, response["items"])
    return list(video_ids)[:max_results]
