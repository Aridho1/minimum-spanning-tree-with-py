import networkx as nx
import matplotlib.pyplot as plt


class Node:
    _id = 0
    _self_map = {}

    def __init__(self):
        Node._id += 1
        self._id = Node._id

        Node._self_map[self._id] = self


class Path:
    _id = 0
    _self_map = {}

    def __init__(self, node1, node2, distance=0):
        Path._id += 1
        self._id = Path._id

        self._path = [node1._id, node2._id]
        self.distance = distance

        Path._self_map[self._id] = self

    @classmethod
    def get_sorted_paths(cls):
        return sorted(
            cls._self_map.values(),
            key=lambda path: path.distance
        )

def reset_data():
    Node._id = 0
    Node._self_map = {}

    Path._id = 0
    Path._self_map = {}

def load_default_data():
    node1 = Node()
    node2 = Node()
    node3 = Node()
    node4 = Node()
    node5 = Node()

    Path(node1, node2, 10)
    Path(node1, node4, 7)
    Path(node2, node3, 6)
    Path(node2, node5, 5)
    Path(node4, node3, 9)
    Path(node4, node5, 9)
    Path(node3, node5, 8)

def input_custom_data():
    total_node = int(input("Jumlah node: "))

    nodes = []

    for i in range(total_node):
        node = Node()
        nodes.append(node)

    total_path = int(input("Jumlah jalur: "))

    print("\nFormat input:")
    print("node1 node2 jarak")
    print("Contoh: 1 2 10\n")

    for i in range(total_path):
        data = input(f"Jalur ke-{i+1}: ").split()

        node1 = int(data[0])
        node2 = int(data[1])
        distance = int(data[2])

        Path(
            nodes[node1 - 1],
            nodes[node2 - 1],
            distance
        )

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

            print("Ditambahkan ke MST\n")

        else:
            print("Ditolak karena membentuk cycle\n")

    print("\n=== HASIL MST ===\n")

    for path in mst:
        print(
            f"Node {path._path[0]} "
            f"<--> Node {path._path[1]} "
            f"= {path.distance}"
        )

    print(f"\nTotal Minimum Distance = {total_distance}")

    return mst


def draw_graph(mst_paths):
    plt.figure()
    G = nx.Graph()

    # Tambahkan semua node
    for node_id in Node._self_map:
        G.add_node(node_id)

    # Tambahkan semua edge
    for path in Path._self_map.values():
        node1 = path._path[0]
        node2 = path._path[1]

        G.add_edge(node1, node2, weight=path.distance)

    pos = nx.spring_layout(G)

    # Gambar semua node dan edge
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=2000,
        font_size=12
    )

    # Label jarak
    labels = nx.get_edge_attributes(G, 'weight')

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=labels
    )

    plt.title("Minimum Spanning Tree - Kabel Internet Antar Daerah")
    # plt.show()

def draw_graph2(mst_paths):
    plt.figure()
    G = nx.Graph()

    # Tambahkan semua node
    for node_id in Node._self_map:
        G.add_node(node_id)

    # Tambahkan semua edge
    for path in Path._self_map.values():
        node1 = path._path[0]
        node2 = path._path[1]

        G.add_edge(
            node1,
            node2,
            weight=path.distance
        )

    pos = nx.spring_layout(G)

    # =========================
    # Ambil edge MST
    # =========================
    mst_edges = []

    for path in mst_paths:
        mst_edges.append(
            (path._path[0], path._path[1])
        )

    # =========================
    # Ambil edge NON-MST
    # =========================
    non_mst_edges = []

    for path in Path._self_map.values():
        edge = (path._path[0], path._path[1])

        if edge not in mst_edges:
            non_mst_edges.append(edge)

    # =========================
    # Gambar node
    # =========================
    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=2000
    )

    nx.draw_networkx_labels(
        G,
        pos,
        font_size=12
    )

    # =========================
    # Edge NON-MST (dashed)
    # =========================
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=non_mst_edges,
        style="dashed",
        edge_color="gray",
        width=1
    )

    # =========================
    # Edge MST (normal)
    # =========================
    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=mst_edges,
        edge_color="black",
        width=2
    )

    # =========================
    # Label jarak
    # =========================
    labels = nx.get_edge_attributes(
        G,
        'weight'
    )

    nx.draw_networkx_edge_labels(
        G,
        pos,
        edge_labels=labels
    )

    plt.title(
        "Minimum Spanning Tree - Kabel Internet Antar Daerah"
    )

    # plt.show()

def main():
    print("PROJECT MST")
    print("Pemasangan Kabel Internet Antar Daerah")

    print("\n1. Gunakan data default")
    print("2. Input data sendiri")

    choice = input("\nPilih: ")

    reset_data()

    if choice == "2":
        input_custom_data()
    else:
        load_default_data()

    print("\n=== DAFTAR SEMUA JALUR ===\n")

    for path in Path.get_sorted_paths():
        print(
            f"Node {path._path[0]} "
            f"<--> Node {path._path[1]} "
            f"= {path.distance}"
        )

    mst = kruskal()

    draw_graph2(mst)

    plt.show()

if __name__ == "__main__":
    main()