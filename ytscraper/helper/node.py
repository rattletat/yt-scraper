#!/usr/bin/env python

from typing import NamedTuple, Tuple

from ytscraper.helper.yt_api import get_related_videos

class VideoNode(NamedTuple):
    videoId: str
    depth: int
    rank: int
    relatedVideos: Tuple

# TODO make it more obvious that number is only a maximal value
def build_node(handle, video_id, rank, depth, number):
    related_videos = get_related_videos(handle, video_id, number)
    video_node = VideoNode(video_id, depth, rank, tuple(related_videos))
    return video_node


def build_node_list(handle, video_ids, depth, number):
    video_nodes = []
    for rank, video_id in enumerate(video_ids):
        node = build_node(handle, video_id, rank, depth, number) 
        video_nodes.append(node)
    return video_nodes

