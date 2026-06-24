import matplotlib.pyplot as plt
import networkx as nx

from .graph_data import Node, Path, get_graph_title


def kruskal():
    parent = {}

    for node_id in Node._self_map:
        parent[node_id] = node_id

    def find(node):
        while parent[node] != node:
            node = parent[node]
        return node

    def union(node1, node2):
        root1 = find(node1)
        root2 = find(node2)

        if root1 != root2:
            parent[root2] = root1
            return True

        return False

    mst = []
    total_distance = 0
    sorted_paths = Path.get_sorted_paths()
    steps = []

    print("\n=== PROSES KRUSKAL ===\n")

    for path in sorted_paths:
        node1 = path._path[0]
        node2 = path._path[1]

        print(
            f"Memeriksa jalur {node1} <--> {node2} "
            f"dengan jarak {path.distance}"
        )

        if union(node1, node2):
            mst.append(path)
            total_distance += path.distance
            accepted = True
            print("Ditambahkan ke MST\n")
        else:
            accepted = False
            print("Ditolak karena membentuk cycle\n")

        steps.append(
            {
                "path": path,
                "accepted": accepted,
                "mst_snapshot": list(mst),
            }
        )

    print("\n=== HASIL MST ===\n")

    for path in mst:
        print(
            f"Node {path._path[0]} "
            f"<--> Node {path._path[1]} "
            f"= {path.distance}"
        )

    print(f"\nTotal Minimum Distance = {total_distance}")

    return mst, steps


def draw_graph2(mst_paths):
    plt.figure()
    graph = nx.Graph()

    for node_id in Node._self_map:
        graph.add_node(node_id)

    for path in Path._self_map.values():
        graph.add_edge(path._path[0], path._path[1], weight=path.distance)

    pos = nx.spring_layout(graph)
    mst_edges = [(path._path[0], path._path[1]) for path in mst_paths]
    non_mst_edges = []

    for path in Path._self_map.values():
        edge = (path._path[0], path._path[1])
        if edge not in mst_edges:
            non_mst_edges.append(edge)

    nx.draw_networkx_nodes(graph, pos, node_size=2000)
    nx.draw_networkx_labels(graph, pos, font_size=12)
    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=non_mst_edges,
        style="dashed",
        edge_color="gray",
        width=1,
    )
    nx.draw_networkx_edges(
        graph,
        pos,
        edgelist=mst_edges,
        edge_color="black",
        width=2,
    )
    nx.draw_networkx_edge_labels(
        graph,
        pos,
        edge_labels=nx.get_edge_attributes(graph, "weight"),
    )

    graph_title = get_graph_title()
    plt.title(
        f"Minimum Spanning Tree"
        f"{f' - {graph_title}' if graph_title else ''}"
    )
