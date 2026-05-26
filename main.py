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

    # =========================
    # INPUT JUMLAH NODE
    # =========================
    total_node = int(
        input("Jumlah node (min 2): ")
    )

    while total_node < 2:
        print("Jumlah node minimal 2")

        total_node = int(
            input("Jumlah node (min 2): ")
        )

    # =========================
    # INPUT NAMA NODE
    # =========================
    print("\n===================================")
    print("Input Nama Node")
    print("===================================")

    nodes = []
    node_labels = {}

    for i in range(total_node):

        label = input(
            f"Nama node {i + 1}: "
        )

        node = Node()

        nodes.append(node)

        node_labels[node._id] = label

    # =========================
    # TOTAL MAX PATH
    # =========================
    maksimal_path = (
        total_node * (total_node - 1)
    ) // 2

    print("\n===================================")
    print(f"Max path: {maksimal_path}")
    print("===================================")

    # =========================
    # REGISTRY PATH
    # =========================
    used_paths = {}

    # =========================
    # SHOW PATH FUNCTION
    # =========================
    def show_paths():

        print("\n===================================")
        print("LIST PATH")
        print("===================================")

        for i in range(1, total_node + 1):
            for j in range(i + 1, total_node + 1):

                edge = tuple(sorted((i, j)))

                node1_label = node_labels[i]
                node2_label = node_labels[j]

                if edge in used_paths:

                    distance = used_paths[edge]

                    print(
                        f"{i} ({node1_label}) "
                        f"<--> "
                        f"{j} ({node2_label}) "
                        f"= {distance}"
                    )

                else:

                    print(
                        f"{i} ({node1_label}) "
                        f"<--> "
                        f"{j} ({node2_label}) "
                        f"= AVAILABLE"
                    )

    # =========================
    # HELP
    # =========================
    print("\n===================================")
    print("COMMAND")
    print("===================================")
    print("show")
    print("add node1 node2 distance")
    print("done")
    print("===================================")

    # =========================
    # MAIN LOOP
    # =========================
    while True:

        cmd = input("\nCommand: ").strip()

        # =========================
        # SHOW
        # =========================
        if cmd == "show":
            show_paths()
            continue

        # =========================
        # DONE
        # =========================
        if cmd == "done":

            total_registered = len(used_paths)

            minimal_path = total_node - 1

            if total_registered < minimal_path:

                print(
                    f"Minimal path belum terpenuhi. "
                    f"Minimal: {minimal_path}"
                )

                continue

            print("Input selesai")
            break

        # =========================
        # ADD PATH
        # =========================
        if cmd.startswith("add"):

            data = cmd.split()

            if len(data) != 4:
                print(
                    "Format salah. "
                    "Gunakan: add node1 node2 distance"
                )
                continue

            try:

                node1 = int(data[1])
                node2 = int(data[2])
                distance = int(data[3])

                # VALIDASI NODE
                if (
                    node1 < 1
                    or node1 > total_node
                    or node2 < 1
                    or node2 > total_node
                ):
                    print(
                        f"Node hanya boleh "
                        f"1 - {total_node}"
                    )
                    continue

                # VALIDASI SELF LOOP
                if node1 == node2:
                    print(
                        "Node tidak boleh sama"
                    )
                    continue

                # VALIDASI DISTANCE
                if distance <= 0:
                    print(
                        "Distance harus > 0"
                    )
                    continue

                # VALIDASI DUPLICATE
                edge = tuple(
                    sorted((node1, node2))
                )

                if edge in used_paths:
                    print(
                        "Path sudah diregistrasi"
                    )
                    continue

                # SIMPAN
                used_paths[edge] = distance

                Path(
                    nodes[node1 - 1],
                    nodes[node2 - 1],
                    distance
                )

                print("Path berhasil ditambahkan")

            except ValueError:
                print("Input harus angka")

            continue

        # =========================
        # UNKNOWN COMMAND
        # =========================
        print("Command tidak dikenali")

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