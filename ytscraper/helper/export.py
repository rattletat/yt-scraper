#!/usr/bin/env python
import csv
import os
import re
import sqlite3


def export_to_csv(nodes, output_dir, output_name):
    if output_name:
        nodes_path = os.path.join(output_dir, f"{output_name}_nodes.csv")
        edges_path = os.path.join(output_dir, f"{output_name}_edges.csv")
    else:
        nodes_path = os.path.join(output_dir, f"nodes.csv")
        edges_path = os.path.join(output_dir, f"edges.csv")

    node_path_exists = os.path.exists(nodes_path)
    edge_path_exists = os.path.exists(edges_path)

    edges = set(
        (node["videoId"], child)
        for node in nodes
        for child in node["relatedVideos"]
    )
    with open(edges_path, "a", newline="", encoding="utf8") as out:
        csv_out = csv.writer(out, delimiter="\t")
        if not edge_path_exists:
            csv_out.writerow(["origin", "target"])
        for origin, target in edges:
            csv_out.writerow([origin, target])

    with open(nodes_path, "a", newline="", encoding="utf8") as out:
        csv_out = csv.writer(out, delimiter="\t")
        if not node_path_exists:
            csv_out.writerow(nodes[0].keys())
        for node in nodes:
            del node["relatedVideos"]
            del node["description"]
            csv_out.writerow(node.values())


def export_to_sql(nodes, output_dir, output_name):
    if output_name:
        db_path = os.path.join(output_dir, f"{output_name}_db.sqlite")
    else:
        db_path = os.path.join(output_dir, f"db.sqlite")

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # Create tables if do not exist
    table_nodes = "CREATE TABLE IF NOT EXISTS NODES (videoId TEXT, rank INTEGER, depth INTEGER, title TEXT, channelId TEXT, channelTitle TEXT, description TEXT, publishedAt TEXT)"
    c.execute(table_nodes)

    table_edges = "CREATE TABLE IF NOT EXISTS EDGES (origin TEXT, target TEXT, FOREIGN KEY (origin) REFERENCES NODES (videoId), FOREIGN KEY (target) REFERENCES NODES (videoId))"
    c.execute(table_edges)

    # Insert nodes
    node_order = [
        "videoId",
        "rank",
        "depth",
        "title",
        "channelId",
        "channelTitle",
        "description",
        "publishedAt",
    ]
    node_sql = "INSERT INTO NODES ({}) VALUES ({})".format(
        ",".join(node_order), ",".join(["?"] * len(node_order))
    )
    node_tuples = [
        tuple(node[label] for label in node_order) for node in nodes
    ]
    c.executemany(node_sql, node_tuples)

    edge_sql = "INSERT INTO EDGES (origin,target) VALUES (?, ?)"
    edge_tuples = (
        (origin["videoId"], target)
        for origin in nodes
        for target in origin["relatedVideos"]
    )
    c.executemany(edge_sql, edge_tuples)
    conn.commit()
    c.close()


def filter_text(text, encoding="ascii"):
    if encoding == "smart":
        text = re.sub(r"<[^>]*>", " ", text)
        text = re.sub(r"\[[^\]]*\]", " ", text)
        text = re.sub(r"[^a-zA-ZäöüÄÖÜß\s]*", "", text)
        text = re.sub(r"\s+", " ", text).strip()
    else:
        text = text.encode(encoding, "ignore").decode()
    return text
