#!/usr/bin/env python

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
    """
    try:
        return build('youtube', 'v3', developerKey=api_key)
    except HttpError:
        echoe(""" There was an error while connecting to the YouTube API.
        Please check your API key.""")


@sleep_and_retry
@limits(3_000_000, 100)
def check_rate_limit():
    """ Sentinel method that limits the requests per 100 seconds. """
    pass


# TODO relevanceLanguage parameter
def get_search_videos(handle,
                      query,
                      maxResults,
                      regionCode='de',
                      safeSearch='none'):
    check_rate_limit()
    response = handle.search().list(
        q=query,
        part='id',
        type='video',
        safeSearch=safeSearch,  # none, moderate, strict
        regionCode=regionCode,
        maxResults=maxResults).execute()
    return list(map(lambda l: l['id']['videoId'], response['items']))


def get_related_videos(handle,
                       videoId,
                       maxResults,
                       regionCode='de',
                       safeSearch='none'):
    check_rate_limit()
    response = handle.search().list(
        relatedToVideoId=videoId,
        part='id',
        type='video',
        safeSearch=safeSearch,  # none, moderate, strict
        regionCode=regionCode,
        maxResults=maxResults).execute()
    return list(map(lambda l: l['id']['videoId'], response['items']))
