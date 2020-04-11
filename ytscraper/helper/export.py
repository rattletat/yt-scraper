#!/usr/bin/env python
import csv
import os
import sys
import re


def export_to_csv(nodes, output_dir):
    nodes_path = os.path.join(output_dir, "nodes.csv")
    edges_path = os.path.join(output_dir, "edges.csv")

    edges = set(
        (node["videoId"], child) for node in nodes for child in node["relatedVideos"]
    )
    print(edges)
    with open(edges_path, "w", newline="") as out:
        csv_out = csv.writer(out, delimiter="\t")
        csv_out.writerow(["origin", "target"])
        for origin, target in edges:
            csv_out.writerow([origin, target])

    with open(nodes_path, "w", newline="") as out:
        csv_out = csv.writer(out, delimiter="\t")
        csv_out.writerow(nodes[0].keys())
        for node in nodes:
            del node["relatedVideos"]
            del node["description"]
            csv_out.writerow(node.values())


def get_call_directory():
    return os.path.dirname(sys.argv[0])


def filter_text(text, encoding="ascii"):
    text = text.encode(encoding, "ignore").decode()
    # text = re.sub(r"<[^>]*>", " ", text)
    # text = re.sub(r"\[[^\]]*\]", " ", text)
    # text = re.sub(r'[^a-zA-ZäöüÄÖÜß\s]*', '', text)
    # text = re.sub(r"\s+", " ", text).strip()
    return text
