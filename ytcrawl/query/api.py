#!/usr/bin/env python

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from click_helper import echof


def get_youtube_handle(api_key):
    try:
        return build('youtube', 'v3', developerKey=api_key)
    except HttpError:
        echof(""" There was an error while connecting to the YouTube API.
        Please check your API key.""")

# TODO relevanceLanguage parameter
def get_search_videos(handle,
                      query,
                      maxResults,
                      regionCode='de',
                      safeSearch='none'):
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
    response = handle.search().list(
        relatedToVideoId=videoId,
        part='id',
        type='video',
        safeSearch=safeSearch,  # none, moderate, strict
        regionCode=regionCode,
        maxResults=maxResults).execute()
    return list(map(lambda l: l['id']['videoId'], response['items']))

