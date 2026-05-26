import os

import networkx as nx
import matplotlib.pyplot as plt

_graph_title = "Kabel Internet Antar Daerah"

COLORS = {
    # reset & style
    "reset": "\033[0m",
    "resetcolor": "\033[0m",
    "bold": "\033[1m",

    # foreground colors
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",

    # background colors (standard)
    "bg_black": "\033[40m",
    "bg_red": "\033[41m",
    "bg_green": "\033[42m",
    "bg_yellow": "\033[43m",
    "bg_blue": "\033[44m",
    "bg_magenta": "\033[45m",
    "bg_cyan": "\033[46m",
    "bg_white": "\033[47m",

    # background colors (bright)
    "bg_bright_black": "\033[100m",
    "bg_bright_red": "\033[101m",
    "bg_bright_green": "\033[102m",
    "bg_bright_yellow": "\033[103m",
    "bg_bright_blue": "\033[104m",
    "bg_bright_magenta": "\033[105m",
    "bg_bright_cyan": "\033[106m",
    "bg_bright_white": "\033[107m",
}

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


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
    global _graph_title
    
    while True:
        try:
            total_node = int(input("Jumlah node (min 2): "))
            if total_node >= 2:
                break
            print("Jumlah node minimal 2")
        except ValueError:
            print("Input harus angka")

    nodes = [Node() for _ in range(total_node)]
    node_labels = {i: f"Node {i}" for i in range(1, total_node + 1)}
    used_paths = {}

    def get_longest_node_labels():
        ...
        return max(len(label) for label in node_labels.values())


    def maksimal_path():
        return total_node * (total_node - 1) // 2

    def minimal_path():
        return total_node - 1
    
    def _log_update(_from, _to, label = ""):
        ...
        print(
            ("", f"[{label}]")[not not label],
            f"'{_from}' berhasil diubah menjadi '{_to}'" if _from != _to else f"'{_to}' Sudah digunakan"
        )

    def show_help():
        print("\n===================================")
        print("BANTUAN / STATUS")
        print("===================================")
        print(f"Jumlah node      : {total_node}")
        print(f"Max path         : {maksimal_path()}")
        print(f"Minimal path     : {minimal_path()}")
        print(f"Path terdaftar   : {len(used_paths)} / {maksimal_path()}")
        print("\n--- Daftar Node ---")
        for i in range(1, total_node + 1):
            print(f"  {i}. {node_labels[i]}")
        print("\n--- Perintah ---")
        print("  help")
        print("  clear")
        print("  show")
        print("  title <graph title>")
        print("  name <no> <nama>")
        print("  edit <no> <nama>")
        print("  remove <no> <nama>")
        print("  add <node1> <node2> <distance>")
        print("  done")
        print("===================================")

    def show_paths():
        print("\n===================================")
        print("LIST PATH")
        print("===================================")
        longestName = get_longest_node_labels()
        
        # PERBAIKAN 1: Ambil panjang digit langsung dari total_node maksimal
        longestIndex = len(str(total_node))

        for i in range(1, total_node + 1):
            for j in range(i + 1, total_node + 1):

                edge = (i, j)

                label1 = node_labels[i]
                label2 = node_labels[j]

                # =========================
                # STATUS PATH
                # =========================
                is_available = edge not in used_paths

                if is_available:

                    statusOrDistance = (
                        f"{COLORS['yellow']}"
                        "AVAILABLE"
                        f"{COLORS['reset']}"
                    )

                    nodeIndexColor = COLORS["blue"]
                    nodeLabelColor = COLORS["cyan"]

                else:

                    distance = used_paths[edge]

                    statusOrDistance = (
                        f"{COLORS['green']}"
                        f"{distance}"
                        f"{COLORS['reset']}"
                    )

                    nodeIndexColor = COLORS["magenta"]
                    nodeLabelColor = COLORS["cyan"]

                # =========================
                # FORMAT BARIS
                # =========================
                line = (
                    f"{nodeIndexColor}"
                    f"{i:{longestIndex}} "

                    f"{nodeLabelColor}"
                    f"{f'({label1})':{longestName+2}} "

                    f"{COLORS['magenta']}"
                    "<--> "

                    f"{nodeIndexColor}"
                    f"{j:{longestIndex}} "

                    f"{nodeLabelColor}"
                    f"{f'({label2})':{longestName+2}} "

                    f"{COLORS['magenta']}"
                    "= "

                    f"{statusOrDistance}"
                    f"{COLORS['reset']}"
                )

                print(line)

        print(
            # f"\n{COLORS['bold']}"
            # f"{COLORS['cyan']}"
            f"{COLORS['reset']}"
            "==================================="
        )

        return
        for i in range(1, total_node + 1):
            for j in range(i + 1, total_node + 1):

                edge = (i, j)

                label1 = node_labels[i]
                label2 = node_labels[j]

                # =========================
                # STATUS PATH
                # =========================
                is_available = edge not in used_paths

                if is_available:

                    statusOrDistance = (
                        f"{COLORS['yellow']}"
                        f"AVAILABLE"
                        f"{COLORS['reset']}"
                    )

                    lineColor = COLORS["blue"]

                else:

                    distance = used_paths[edge]

                    statusOrDistance = (
                        f"{COLORS['green']}"
                        f"{distance}"
                        f"{COLORS['reset']}"
                    )

                    lineColor = COLORS["cyan"]

                # =========================
                # FORMAT BARIS
                # =========================
                line = (
                    f"{lineColor}"
                    f"{i:{longestIndex}} "
                    f"{f'({label1})':{longestName+2}} "
                    f"{COLORS['magenta']}"
                    "<--> "
                    f"{lineColor}"
                    f"{j:{longestIndex}} "
                    f"{f'({label2})':{longestName+2}} "
                    f"{COLORS['magenta']}"
                    "= "
                    f"{statusOrDistance}"
                    f"{COLORS['reset']}"
                )

                print(line)

        print(
            f"\n{COLORS['bold']}"
            f"{COLORS['cyan']}"
            "==================================="
            f"{COLORS['reset']}"
        )

        return

        for i in range(1, total_node + 1):
            for j in range(i + 1, total_node + 1):
                edge = (i, j)
                label1, label2 = node_labels[i], node_labels[j]

                # Typo fix: "AVAILABLE" (huruf A kurang satu)
                statusOrDistance = "AVAILABLE" if edge not in used_paths else used_paths[edge]

                # PERBAIKAN 2: Berikan format rata kiri :{longestName+2} pada label kedua juga
                print(
                    f"{i:{longestIndex}} {f'({label1})':{longestName+2}} <--> "
                    f"{j:{longestIndex}} {f'({label2})':{longestName+2}} = {statusOrDistance}"
                )

    clear_screen()
    show_help()

    while True:
        _input_cmd = input("\nCommand: ")
        parts = _input_cmd.strip().split()
        if not parts:
            continue

        action = parts[0].lower()

        if action == "help":
            show_help()
            continue

        if action == "clear":
            clear_screen()
            show_help()
            continue
            
        if action == "title":
            ...
            if len(parts) < 2:
                ...
                print("Berikan title nya")
                continue

            _prev = _graph_title
            _graph_title = " ".join(parts[1:])
            _log_update(_prev, _graph_title, "Title")

            continue

        if action == "show":
            show_paths()
            continue

        if action == "name":
            if len(parts) < 3:
                print("Format: name <no> <nama>")
                continue
            try:
                idx = int(parts[1])
                if idx < 1 or idx > total_node:
                    print(f"Node hanya boleh 1 - {total_node}")
                    continue
                
                name = " ".join(parts[2:])
                _prev = node_labels[idx]
                node_labels[idx] = name
                _log_update(_prev, name, f"Node {idx}")
            except ValueError:
                print("Nomor node harus angka")
            continue

        if action == "done":
            if len(used_paths) < minimal_path():
                print(
                    f"Minimal path belum terpenuhi. "
                    f"Minimal: {minimal_path()}"
                )
                continue
            print("Input selesai")
            break

        if action == "add":
            if len(parts) != 4:
                print("Format: add <node1> <node2> <distance>")
                continue
            try:
                node1, node2, distance = (
                    int(parts[1]),
                    int(parts[2]),
                    int(parts[3]),  
                )
                if not (1 <= node1 <= total_node and 1 <= node2 <= total_node):
                    print(f"Node hanya boleh 1 - {total_node}")
                    continue
                if node1 == node2:
                    print("Node tidak boleh sama")
                    continue
                if distance <= 0:
                    print("Distance harus > 0")
                    continue
                edge = tuple(sorted((node1, node2)))
                if edge in used_paths:
                    print("Path sudah diregistrasi")
                    continue
                used_paths[edge] = distance
                Path(nodes[node1 - 1], nodes[node2 - 1], distance)
                print("Path berhasil ditambahkan")
            except ValueError:
                print("Input harus angka")
            continue

        if action == "edit":

            if len(parts) != 4:
                print(
                    "Format: edit "
                    "<node1> <node2> <distance>"
                )
                continue

            try:
                node1 = int(parts[1])
                node2 = int(parts[2])
                distance = int(parts[3])

                # =========================
                # VALIDASI NODE
                # =========================
                if not (
                    1 <= node1 <= total_node
                    and
                    1 <= node2 <= total_node
                ):
                    print(
                        f"Node hanya boleh "
                        f"1 - {total_node}"
                    )
                    continue

                # =========================
                # VALIDASI SELF LOOP
                # =========================
                if node1 == node2:
                    print(
                        "Node tidak boleh sama"
                    )
                    continue

                # =========================
                # VALIDASI DISTANCE
                # =========================
                if distance <= 0:
                    print(
                        "Distance harus > 0"
                    )
                    continue

                edge = tuple(
                    sorted((node1, node2))
                )

                # =========================
                # VALIDASI EXIST
                # =========================
                if edge not in used_paths:
                    print(
                        "Path belum diregistrasi"
                    )
                    continue

                # =========================
                # UPDATE USED PATH
                # =========================
                used_paths[edge] = distance

                # =========================
                # UPDATE PATH OBJECT
                # =========================
                for path_obj in Path._self_map.values():

                    current_edge = tuple(
                        sorted(path_obj._path)
                    )

                    if current_edge == edge:
                        path_obj.distance = distance
                        break

                print("Path berhasil diupdate")

            except ValueError:
                print("Input harus angka")

            continue
        
        if action == "remove":

            if len(parts) != 3:
                print(
                    "Format: remove <node1> <node2>"
                )
                continue

            try:
                node1 = int(parts[1])
                node2 = int(parts[2])

                # =========================
                # VALIDASI NODE
                # =========================
                if not (
                    1 <= node1 <= total_node
                    and
                    1 <= node2 <= total_node
                ):
                    print(
                        f"Node hanya boleh "
                        f"1 - {total_node}"
                    )
                    continue

                # =========================
                # VALIDASI SELF LOOP
                # =========================
                if node1 == node2:
                    print(
                        "Node tidak boleh sama"
                    )
                    continue

                edge = tuple(
                    sorted((node1, node2))
                )

                # =========================
                # VALIDASI EXIST
                # =========================
                if edge not in used_paths:
                    print(
                        "Path belum diregistrasi"
                    )
                    continue

                # =========================
                # REMOVE PATH
                # =========================
                del used_paths[edge]

                target_path_id = None

                for path_id, path_obj in Path._self_map.items():

                    current_edge = tuple(
                        sorted(path_obj._path)
                    )

                    if current_edge == edge:
                        target_path_id = path_id
                        break

                if target_path_id:
                    del Path._self_map[target_path_id]

                print("Path berhasil dihapus")

            except ValueError:
                print("Input harus angka")

            continue

        print("Command tidak dikenali. Ketik 'help' untuk bantuan.")

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

    plt.title(
        f"Minimum Spanning Tree"
        f"{f' - {_graph_title}' if _graph_title else ''}"
    )
    # plt.title(f"Minimum Spanning Tree{(f" - {_graph_title}", "")[not not _graph_title]}")
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

    # print(f"{_graph_title = }")
    plt.title(
        f"Minimum Spanning Tree"
        f"{f' - {_graph_title}' if _graph_title else ''}"
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