#!/usr/bin/env python

"""

This module contains a video node class that groups information about
the search in which the video was found.
It incorporates the unique video id used by YouTube,
the rank and the depth within the recursive search result
and related children nodes.

    * VideoNode - Named tuple that bundles meta search information.
    * construct_node_list - Converts a list of video ids to video nodes.
    * _get_clamped_index - Helper function for faultless indexing.
"""

from typing import NamedTuple, Tuple

from ytscraper.helper.yt_api import get_related_videos


# TODO: Divide information into SearchNode and VideoNode,
#       for meta-search and search information.
class VideoNode(NamedTuple):
    """ Groups meta information about a video within a YouTube search."""

    videoId: str
    depth: int
    rank: int
    relatedVideos: Tuple


def construct_node_list(handle, video_ids, depth, branching_factors):
    """ Constructs a video node list from a search result.

    Parameter
    ---------
    handle: Resource object
        Needed for querying the YouTube API V3 to get related videos.
    video_id: str
        The video identifier found in a search.
    depth: int
        The number of recursion steps used to find the videos 
        specified in `video_ids`.
    branching_factors: tuple(int)
        An array of numbers indicating the branching factors on each level.
        Needed to determine how many related nodes to fetch.

    Returns
    -------
        list(VideoNode)
            Returns a list of annotated video ids.
    """
    # Get amount of related children nodes
    number_related = _get_clamped_index(branching_factors, depth + 1)
    # Construct node list
    video_nodes = []
    for rank, video_id in enumerate(video_ids):
        related_videos = get_related_videos(handle, video_id, number_related)
        video_nodes.append(VideoNode(video_id, depth, rank, tuple(related_videos)))
    return video_nodes


def _get_clamped_index(container, index):
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
