#!/usr/bin/env python
import csv
import os


def export_to_csv(nodes, output_dir):
    nodes_path = os.path.join(output_dir, "nodes.csv")
    edges_path = os.path.join(output_dir, "edges.csv")

    edges = set(
        (node["videoId"], child) for node in nodes for child in node["relatedVideos"]
    )
    print(edges)
    with open(edges_path, "w", newline="") as out:
        csv_out = csv.writer(out)
        csv_out.writerow(["origin", "target"])
        for origin, target in edges:
            csv_out.writerow([origin, target])

    with open(nodes_path, "w", newline="") as out:
        csv_out = csv.writer(out)
        csv_out.writerow(nodes[0].keys())
        for node in nodes:
            csv_out.writerow(node.values())
