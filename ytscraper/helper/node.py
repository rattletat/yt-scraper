#!/usr/bin/env python

from typing import NamedTuple, Tuple

from ytscraper.helper.yt_api import get_related_videos


class VideoNode(NamedTuple):
    videoId: str
    depth: int
    rank: int
    relatedVideos: Tuple


# TODO make it more obvious that number is only a maximal value
def build_node(handle, video_id, rank, depth, related_number):
    related_videos = get_related_videos(handle, video_id, related_number)
    video_node = VideoNode(video_id, depth, rank, tuple(related_videos))
    return video_node


def get_clamp_index(container, index):
    clamped_index = max(0, min(index, len(container) - 1))
    return container[clamped_index]


def convert_to_node_list(handle, video_ids, depth, numbers):
    # Related videos are one step deeper
    related_number = get_clamp_index(numbers, depth + 1)
    video_nodes = []
    for rank, video_id in enumerate(video_ids):
        node = build_node(handle, video_id, rank, depth, related_number)
        video_nodes.append(node)
    return video_nodes
