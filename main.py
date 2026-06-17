import os
import shlex

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


def print_error(title, usage=None, examples=None):
    print(f"{COLORS['red']}{title}{COLORS['reset']}")
    if usage:
        print(f"\n{COLORS['bold']}Usage:{COLORS['reset']}\n")
        print(usage)
    if examples:
        print(f"\n{COLORS['bold']}Examples:{COLORS['reset']}\n")
        print(examples)


def print_success(msg):
    print(f"{COLORS['green']}{msg}{COLORS['reset']}")


def print_warning(msg):
    print(f"{COLORS['yellow']}{msg}{COLORS['reset']}")


def print_info(msg):
    print(f"{COLORS['cyan']}{msg}{COLORS['reset']}")


def confirm(prompt_lines, default_yes=False):
    color = COLORS["cyan"] if default_yes else COLORS["yellow"]
    suffix = "[Y/n]" if default_yes else "[y/N]"
    for line in prompt_lines:
        print(line)
    answer = input(f"{color}{suffix}{COLORS['reset']}: ").strip().lower()
    if not answer:
        return default_yes
    return answer in ("y", "yes")


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

    node_labels = {}
    used_paths = {}

    def display_name(node_id):
        label = node_labels.get(node_id, "")
        return label if label else f"Node {node_id}"

    def find_node_by_label(label):
        label_lower = label.lower()
        for node_id, stored in node_labels.items():
            if stored and stored.lower() == label_lower:
                return node_id
        return None

    def validate_label(label, exclude_node_id=None):
        if not label or not label.strip():
            return "Label cannot be empty."
        if label.strip().isdigit():
            return "Label cannot contain only digits."
        existing = find_node_by_label(label)
        if existing is not None and existing != exclude_node_id:
            return f"Label '{label}' is already used by node {existing}."
        return None

    def try_resolve_node(value):
        if value.isdigit():
            node_id = int(value)
            if node_id in node_labels:
                return node_id, None
            return None, value
        found = find_node_by_label(value)
        if found is not None:
            return found, None
        return None, value

    def resolve_node(value):
        node_id, missing = try_resolve_node(value)
        if node_id is None:
            if value.isdigit():
                raise ValueError(f"Node {value} does not exist.")
            raise ValueError(f"Node '{value}' does not exist.")
        return node_id

    def create_node(label=""):
        if label:
            err = validate_label(label)
            if err:
                print_error(err)
                return None
        node = Node()
        node_labels[node._id] = label if label else ""
        return node._id

    def create_nodes_count(count):
        created = []
        for _ in range(count):
            node_id = create_node()
            if node_id is None:
                return created
            created.append(node_id)
        return created

    def remove_node(node_id):
        if node_id not in node_labels:
            return
        del node_labels[node_id]
        del Node._self_map[node_id]
        edges_to_remove = [edge for edge in used_paths if node_id in edge]
        for edge in edges_to_remove:
            del used_paths[edge]
        path_ids_to_remove = [
            path_id
            for path_id, path_obj in Path._self_map.items()
            if node_id in path_obj._path
        ]
        for path_id in path_ids_to_remove:
            del Path._self_map[path_id]

    def remove_nodes(node_ids):
        for node_id in node_ids:
            remove_node(node_id)

    def set_node_name(node_id, label):
        if node_id not in node_labels:
            print_error(f"Node {node_id} does not exist.")
            return
        err = validate_label(label, exclude_node_id=node_id)
        if err:
            print_error(err)
            return
        current = node_labels[node_id]
        if current:
            if not confirm(
                [
                    f"Node {node_id} is currently named:",
                    "",
                    f"  {current}",
                    "",
                    "Rename to:",
                    "",
                    f"  {label}",
                ],
                default_yes=True,
            ):
                return
        node_labels[node_id] = label
        print_success(f"Node {node_id} renamed to '{label}'.")

    def create_path(node1_id, node2_id, distance):
        edge = tuple(sorted((node1_id, node2_id)))
        if edge in used_paths:
            print_warning("Path already registered.")
            return False
        used_paths[edge] = distance
        Path(Node._self_map[node1_id], Node._self_map[node2_id], distance)
        print_success("Path added successfully.")
        return True

    def edit_path(node1_id, node2_id, distance):
        edge = tuple(sorted((node1_id, node2_id)))
        if edge not in used_paths:
            print_warning("Path is not registered.")
            return False
        used_paths[edge] = distance
        for path_obj in Path._self_map.values():
            if tuple(sorted(path_obj._path)) == edge:
                path_obj.distance = distance
                break
        print_success("Path updated successfully.")
        return True

    def remove_path(node1_id, node2_id):
        edge = tuple(sorted((node1_id, node2_id)))
        if edge not in used_paths:
            print_warning("Path is not registered.")
            return False
        del used_paths[edge]
        target_path_id = None
        for path_id, path_obj in Path._self_map.items():
            if tuple(sorted(path_obj._path)) == edge:
                target_path_id = path_id
                break
        if target_path_id:
            del Path._self_map[target_path_id]
        print_success("Path removed successfully.")
        return True

    def show_node_list():
        print("\n===================================")
        print("NODE LIST")
        print("===================================")
        if not node_labels:
            print_info("  (no nodes)")
        else:
            for node_id in sorted(node_labels):
                label = node_labels[node_id]
                color = COLORS["green"] if label else COLORS["yellow"]
                print(
                    f"  {node_id} "
                    f"{color}{display_name(node_id)}{COLORS['reset']}"
                )
        print("===================================")

    def get_longest_node_labels():
        if not node_labels:
            return 0
        return max(len(display_name(node_id)) for node_id in node_labels)

    def node_count():
        return len(node_labels)

    def maksimal_path():
        n = node_count()
        return n * (n - 1) // 2

    def minimal_path():
        n = node_count()
        return max(0, n - 1) if n >= 2 else 0

    def _log_update(_from, _to, label=""):
        print(
            ("", f"[{label}]")[bool(label)],
            (
                f"'{_from}' updated to '{_to}'"
                if _from != _to
                else f"'{_to}' is already in use"
            ),
        )

    def show_help():
        print("\n===================================")
        print("HELP / STATUS")
        print("===================================")
        print(f"Node count       : {node_count()}")
        # print(f"Max paths        : {maksimal_path()}")
        print(f"Min paths        : {minimal_path()}")
        print(f"Registered paths : {len(used_paths)} / {maksimal_path()}")
        print("\n--- Commands ---")
        print("  help")
        print("  clear")
        print("  show")
        print("  title <graph title>")
        print("  node list")
        print("  node <count>")
        print("  node <label>")
        print("  node <label1,label2,...>")
        print("  node <count> <label1,label2,...>")
        print("  node name <id> <label>")
        print("  node remove <id>")
        print("  node remove <id1,id2,...>")
        print("  add <node1> <node2> <distance>")
        print("  edit <node1> <node2> <distance>")
        print("  remove <node1> <node2>")
        print("  done")
        print("===================================")

    def show_paths():
        print("\n===================================")
        print("PATH LIST")
        print("===================================")
        if node_count() < 2:
            print_info("  (need at least 2 nodes)")
            print("===================================")
            return

        longest_name = get_longest_node_labels()
        longest_index = len(str(max(node_labels)))

        for i in sorted(node_labels):
            for j in sorted(node_labels):
                if i >= j:
                    continue

                edge = (i, j)
                label1 = display_name(i)
                label2 = display_name(j)
                is_available = edge not in used_paths

                if is_available:
                    status_or_distance = (
                        f"{COLORS['yellow']}AVAILABLE{COLORS['reset']}"
                    )
                    node_index_color = COLORS["blue"]
                    node_label_color = COLORS["cyan"]
                else:
                    distance = used_paths[edge]
                    status_or_distance = (
                        f"{COLORS['green']}{distance}{COLORS['reset']}"
                    )
                    node_index_color = COLORS["magenta"]
                    node_label_color = COLORS["cyan"]

                line = (
                    f"{node_index_color}{i:{longest_index}} "
                    f"{node_label_color}{f'({label1})':{longest_name + 2}} "
                    f"{COLORS['magenta']}<--> "
                    f"{node_index_color}{j:{longest_index}} "
                    f"{node_label_color}{f'({label2})':{longest_name + 2}} "
                    f"{COLORS['magenta']}= {status_or_distance}{COLORS['reset']}"
                )
                print(line)

        print(f"{COLORS['reset']}===================================")

    def handle_node_command(parts):
        if len(parts) < 2:
            print_error(
                "Invalid node command.",
                usage=(
                    "node <count>\n"
                    "node <label>\n"
                    "node <label1,label2,...>\n"
                    "node <count> <label1,label2,...>\n"
                    "node list\n"
                    "node name <id> <label>\n"
                    "node remove <id>\n"
                    "node remove <id1,id2,...>"
                ),
                examples=(
                    "node 5\n"
                    "node Jakarta\n"
                    "node Jakarta,Bandung\n"
                    "node 5 Jakarta,Bandung\n"
                    'node "Jakarta Selatan"\n'
                    "node list\n"
                    "node name 5 Jakarta\n"
                    'node name 5 "Jakarta Selatan"\n'
                    "node remove 5\n"
                    "node remove 5,6,7"
                ),
            )
            return

        sub = parts[1].lower()

        if sub == "list":
            show_node_list()
            return

        if sub == "remove":
            if len(parts) != 3:
                print_error(
                    "Invalid node remove command.",
                    usage="node remove <id>\nnode remove <id1,id2,...>",
                    examples="node remove 5\nnode remove 5,6,7",
                )
                return
            raw_ids = [s.strip() for s in parts[2].split(",") if s.strip()]
            node_ids = []
            for raw in raw_ids:
                if not raw.isdigit():
                    print_error(f"Invalid node ID: {raw}")
                    return
                node_id = int(raw)
                if node_id not in node_labels:
                    print_error(f"Node {node_id} does not exist.")
                    return
                node_ids.append(node_id)
            if not confirm(
                [
                    "The following nodes will be removed:",
                    "",
                    *[f"  {node_id}" for node_id in node_ids],
                    "",
                    "All connected paths will also be removed.",
                ],
                default_yes=False,
            ):
                print_info("Cancelled.")
                return
            remove_nodes(node_ids)
            print_success("Node(s) removed successfully.")
            return

        if sub == "name":
            if len(parts) < 4:
                print_error(
                    "Invalid node name command.",
                    usage="node name <id> <label>",
                    examples=(
                        "node name 5 Jakarta\n"
                        'node name 5 "Jakarta Selatan"'
                    ),
                )
                return
            if not parts[2].isdigit():
                print_error("Node ID must be a number.")
                return
            node_id = int(parts[2])
            label = " ".join(parts[3:])
            set_node_name(node_id, label)
            return

        arg = parts[1]
        labels_part = parts[2] if len(parts) > 2 else None

        if labels_part is not None:
            if not arg.isdigit():
                print_error(
                    "Invalid node command.",
                    usage="node <count> <label1,label2,...>",
                    examples="node 5 Jakarta,Bandung",
                )
                return
            count = int(arg)
            if count <= 0:
                print_error("Node count must be greater than 0.")
                return
            labels = [
                label.strip()
                for label in labels_part.split(",")
                if label.strip()
            ]
            for label in labels:
                err = validate_label(label)
                if err:
                    print_error(err)
                    return
            if len(labels) != count:
                extra = abs(len(labels) - count)
                if len(labels) < count:
                    detail = (
                        f"The remaining {extra} nodes will use default names."
                    )
                else:
                    detail = f"Only the first {count} names will be used."
                if not confirm(
                    [
                        f"Name count ({len(labels)}) does not match "
                        f"requested node count ({count}).",
                        "",
                        detail,
                    ],
                    default_yes=False,
                ):
                    print_info("Cancelled.")
                    return
                labels = labels[:count]
            create_nodes_count(count)
            node_ids = sorted(node_labels)[-count:]
            for node_id, label in zip(node_ids, labels):
                node_labels[node_id] = label
            for node_id in node_ids:
                print_success(f"  {display_name(node_id)}")
            return

        if arg.isdigit():
            count = int(arg)
            if count <= 0:
                print_error("Node count must be greater than 0.")
                return
            create_nodes_count(count)
            for node_id in sorted(node_labels)[-count:]:
                print_success(f"  {display_name(node_id)}")
            return

        if "," in arg:
            labels = [label.strip() for label in arg.split(",") if label.strip()]
            for label in labels:
                err = validate_label(label)
                if err:
                    print_error(err)
                    return
            for label in labels:
                create_node(label)
                print_success(f"  {label}")
            return

        err = validate_label(arg)
        if err:
            print_error(err)
            return
        create_node(arg)
        print_success(f"  {arg}")

    def handle_add_command(parts):
        if len(parts) != 4:
            print_error(
                "Invalid add command.",
                usage="add <node1> <node2> <distance>",
                examples=(
                    "add 1 2 10\n"
                    "add Jakarta Bekasi 10\n"
                    'add "Jakarta Selatan" Bekasi 10'
                ),
            )
            return
        try:
            distance = int(parts[3])
        except ValueError:
            print_error(
                "Distance must be a number.",
                usage="add <node1> <node2> <distance>",
                examples="add 1 2 10",
            )
            return
        if distance <= 0:
            print_error("Distance must be greater than 0.")
            return

        node1_val, node2_val = parts[1], parts[2]
        id1, miss1 = try_resolve_node(node1_val)
        id2, miss2 = try_resolve_node(node2_val)
        missing = []
        if miss1:
            missing.append(miss1)
        if miss2:
            missing.append(miss2)

        if missing:
            unique_missing = list(dict.fromkeys(missing))
            for name in unique_missing:
                if name.isdigit():
                    print_error(f"Node {name} does not exist.")
                    return
                err = validate_label(name)
                if err:
                    print_error(err)
                    return
            if not confirm(
                [
                    "The following nodes do not exist:",
                    "",
                    *[f"  {name}" for name in unique_missing],
                    "",
                    "Create them automatically?",
                ],
                default_yes=False,
            ):
                print_info("Cancelled.")
                return
            for name in unique_missing:
                if try_resolve_node(name)[0] is None:
                    create_node(name)
            id1, _ = try_resolve_node(node1_val)
            id2, _ = try_resolve_node(node2_val)

        if id1 is None or id2 is None:
            return
        if id1 == id2:
            print_error("Nodes cannot be the same.")
            return
        create_path(id1, id2, distance)

    def handle_edit_command(parts):
        if len(parts) != 4:
            print_error(
                "Invalid edit command.",
                usage="edit <node1> <node2> <distance>",
                examples=(
                    "edit 1 2 20\n"
                    "edit Jakarta Bekasi 20"
                ),
            )
            return
        try:
            distance = int(parts[3])
        except ValueError:
            print_error(
                "Distance must be a number.",
                usage="edit <node1> <node2> <distance>",
                examples="edit 1 2 20",
            )
            return
        if distance <= 0:
            print_error("Distance must be greater than 0.")
            return
        try:
            node1_id = resolve_node(parts[1])
            node2_id = resolve_node(parts[2])
        except ValueError as exc:
            print_error(str(exc))
            return
        if node1_id == node2_id:
            print_error("Nodes cannot be the same.")
            return
        edit_path(node1_id, node2_id, distance)

    def handle_remove_command(parts):
        if len(parts) != 3:
            print_error(
                "Invalid remove command.",
                usage="remove <node1> <node2>",
                examples=(
                    "remove 1 2\n"
                    "remove Jakarta Bekasi"
                ),
            )
            return
        try:
            node1_id = resolve_node(parts[1])
            node2_id = resolve_node(parts[2])
        except ValueError as exc:
            print_error(str(exc))
            return
        if node1_id == node2_id:
            print_error("Nodes cannot be the same.")
            return
        remove_path(node1_id, node2_id)

    clear_screen()
    show_help()

    while True:
        command = input("\nCommand: ").strip()
        if not command:
            continue

        try:
            parts = shlex.split(command)
        except ValueError as exc:
            print_error(f"Invalid command syntax: {exc}")
            continue

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
            if len(parts) < 2:
                print_error(
                    "Graph title is required.",
                    usage="title <graph title>",
                    examples='title Kabel Internet Antar Daerah',
                )
                continue
            prev = _graph_title
            _graph_title = " ".join(parts[1:])
            _log_update(prev, _graph_title, "Title")
            continue

        if action == "show":
            show_paths()
            continue

        if action == "node":
            handle_node_command(parts)
            continue

        if action == "done":
            if node_count() < 2:
                print_warning("At least 2 nodes are required.")
                continue
            if len(used_paths) < minimal_path():
                print_warning(
                    f"Minimum paths not met. Required: {minimal_path()}"
                )
                continue
            print_success("Input complete.")
            break

        if action == "add":
            handle_add_command(parts)
            continue

        if action == "edit":
            handle_edit_command(parts)
            continue

        if action == "remove":
            handle_remove_command(parts)
            continue

        print_error(
            "Unknown command.",
            usage="Type 'help' for available commands.",
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