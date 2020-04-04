#!/usr/bin/python

# This helper module handles the YouTube API v3 authentication.

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_youtube_handle(api_key):
    return build('youtube', 'v3', api_key)


