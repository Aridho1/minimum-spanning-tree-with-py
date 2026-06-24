import shlex
import time

from .graph_data import Node, Path, get_graph_title, set_graph_title
from .ui import (
    COLORS,
    THEME,
    clear_screen,
    confirm,
    print_error,
    print_info,
    print_success,
    print_warning,
)

DEFAULT_DELAY_LOOP_IN_MS = 0.1
SECTION_WIDTH = 60


def input_custom_data():
    node_labels = {}
    used_paths = {}

    def rule(char="=", color_key="secondary"):
        return f"{THEME[color_key]}{char * SECTION_WIDTH}{COLORS['reset']}"

    def section(title, subtitle=None):
        print(f"\n{rule()}")
        print(f"{COLORS['bold']}{THEME['primary']}{title}{COLORS['reset']}")
        if subtitle:
            print(f"{THEME['muted']}{subtitle}{COLORS['reset']}")
        print(rule())

    def prompt():
        return (
            f"\n{THEME['primary']}mst-cli"
            f"{COLORS['reset']} "
            f"{THEME['secondary']}>{COLORS['reset']} "
        )

    def hint(message):
        print(f"{THEME['muted']}Hint: {message}{COLORS['reset']}")

    def badge(label, color_key="info"):
        return f"{THEME[color_key]}[{label}]{COLORS['reset']}"

    def display_name(node_id):
        label = node_labels.get(node_id, "")
        return label if label else f"Node {node_id}"

    def display_node(node_id):
        return f"{badge(node_id, 'accent')} {display_name(node_id)}"

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
                    f"{display_node(node_id)} is currently named:",
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
        print_success(f"{badge('OK', 'success')} {display_node(node_id)} renamed to '{label}'.")

    def create_path(node1_id, node2_id, distance):
        edge = tuple(sorted((node1_id, node2_id)))
        if edge in used_paths:
            print_warning("Path already registered.")
            return False
        used_paths[edge] = distance
        Path(Node._self_map[node1_id], Node._self_map[node2_id], distance)
        print_success(
            f"{badge('ADD', 'success')} {display_name(node1_id)} <--> "
            f"{display_name(node2_id)} = {distance}"
        )
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
        print_success(
            f"{badge('EDIT', 'success')} {display_name(node1_id)} <--> "
            f"{display_name(node2_id)} = {distance}"
        )
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
        print_success(
            f"{badge('DEL', 'success')} Removed path "
            f"{display_name(node1_id)} <--> {display_name(node2_id)}"
        )
        return True

    def show_node_list():
        section("NODE LIST", "Registered nodes and current labels.")
        if not node_labels:
            print_info("No nodes have been created yet.")
            hint("Use 'node 5' or 'node Jakarta,Bandung' to start.")
            return

        longest_id = get_longest_node_id()
        for node_id in sorted(node_labels):
            label = node_labels[node_id]
            color = THEME["primary"] if label else THEME["warning"]
            print(
                f"  {badge(f'{node_id:{longest_id}}', 'accent')} "
                f"{color}{display_name(node_id)}{COLORS['reset']}"
            )

    def get_longest_node_labels():
        if not node_labels:
            return 0
        return max(len(display_name(node_id)) for node_id in node_labels)

    def get_longest_node_id():
        return len(str(max(node_labels)))

    def node_count():
        return len(node_labels)

    def maksimal_path():
        total = node_count()
        return total * (total - 1) // 2

    def minimal_path():
        total = node_count()
        return max(0, total - 1) if total >= 2 else 0

    def log_update(previous, current, label=""):
        tag = badge(label or "INFO", "info")
        if previous != current:
            print_success(f"{tag} '{previous}' updated to '{current}'")
        else:
            print_info(f"{tag} '{current}' is already in use")

    def show_help():
        section("HELP / STATUS", "Interactive CRUD for MST graph input.")
        print(f"Graph title      : {THEME['primary']}{get_graph_title()}{COLORS['reset']}")
        print(f"Node count       : {THEME['info']}{node_count()}{COLORS['reset']}")
        print(f"Min paths        : {THEME['info']}{minimal_path()}{COLORS['reset']}")
        print(
            f"Registered paths : {THEME['info']}{len(used_paths)}"
            f"{COLORS['reset']} / {THEME['muted']}{maksimal_path()}{COLORS['reset']}"
        )
        print(f"\n{COLORS['bold']}{THEME['secondary']}Commands{COLORS['reset']}")
        print(f"  {badge('help')} Show command summary and status")
        print(f"  {badge('clear')} Clear screen and redraw help")
        print(f"  {badge('show')} Show all possible paths and availability")
        print(f"  {badge('title <graph title>')} Rename graph title")
        print(f"  {badge('node list')} Show current node list")
        print(f"  {badge('node <count>')} Create unnamed nodes")
        print(f"  {badge('node <label>')} Create one named node")
        print(f"  {badge('node <label1,label2,...>')} Create multiple named nodes")
        print(f"  {badge('node <count> <label1,label2,...>')} Create many nodes with labels")
        print(f"  {badge('node name <id> <label>')} Rename a node")
        print(f"  {badge('node remove <id>')} Delete one node")
        print(f"  {badge('node remove <id1,id2,...>')} Delete multiple nodes")
        print(f"  {badge('add <node1> <node2> <distance>')} Create a path")
        print(f"  {badge('edit <node1> <node2> <distance>')} Update a path distance")
        print(f"  {badge('remove <node1> <node2>')} Delete a path")
        print(f"  {badge('done')} Finish input and run MST")
        hint("Use quotes for names with spaces, for example: node \"Jakarta Selatan\"")

    def show_paths():
        section("PATH LIST", "All node pairs and whether a path is already registered.")
        if node_count() < 2:
            print_info("At least 2 nodes are needed before paths can be inspected.")
            hint("Create nodes first, then use 'show' again.")
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
                    status_or_distance = f"{THEME['warning']}AVAILABLE{COLORS['reset']}"
                    node_index_color = THEME["accent"]
                    node_label_color = THEME["info"]
                else:
                    distance = used_paths[edge]
                    status_or_distance = f"{THEME['primary']}{distance}{COLORS['reset']}"
                    node_index_color = THEME["secondary"]
                    node_label_color = THEME["info"]

                line = (
                    f"{node_index_color}{i:{longest_index}} "
                    f"{node_label_color}{f'({label1})':{longest_name + 2}} "
                    f"{THEME['secondary']}<--> "
                    f"{node_index_color}{j:{longest_index}} "
                    f"{node_label_color}{f'({label2})':{longest_name + 2}} "
                    f"{THEME['secondary']}= {status_or_distance}{COLORS['reset']}"
                )
                print(line)

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
            raw_ids = [value.strip() for value in parts[2].split(",") if value.strip()]
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
                    *[f"  {display_node(node_id)}" for node_id in node_ids],
                    "",
                    "All connected paths will also be removed.",
                ],
                default_yes=False,
            ):
                print_info("Cancelled.")
                return
            remove_nodes(node_ids)
            print_success(f"{badge('DEL', 'success')} Node(s) removed successfully.")
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
            labels = [label.strip() for label in labels_part.split(",") if label.strip()]
            for label in labels:
                err = validate_label(label)
                if err:
                    print_error(err)
                    return
            if len(labels) != count:
                extra = abs(len(labels) - count)
                if len(labels) < count:
                    detail = f"The remaining {extra} nodes will use default names."
                else:
                    detail = f"Only the first {count} names will be used."
                if not confirm(
                    [
                        f"Name count ({len(labels)}) does not match requested node count ({count}).",
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
            print_success(f"{badge('ADD', 'success')} Added {count} node(s).")
            for node_id in node_ids:
                print(f"  {display_node(node_id)}")
            return

        if arg.isdigit():
            count = int(arg)
            if count <= 0:
                print_error("Node count must be greater than 0.")
                return
            create_nodes_count(count)
            print_success(f"{badge('ADD', 'success')} Added {count} node(s).")
            for node_id in sorted(node_labels)[-count:]:
                print(f"  {display_node(node_id)}")
            return

        if "," in arg:
            labels = [label.strip() for label in arg.split(",") if label.strip()]
            for label in labels:
                err = validate_label(label)
                if err:
                    print_error(err)
                    return
            print_info(f"Creating {len(labels)} node(s)...")
            for label in labels:
                time.sleep(DEFAULT_DELAY_LOOP_IN_MS)
                node_id = create_node(label)
                if node_id:
                    print(f"  {badge(node_id, 'accent')} {THEME['primary']}{label}{COLORS['reset']}")
            return

        err = validate_label(arg)
        if err:
            print_error(err)
            return
        node_id = create_node(arg)
        print_success(f"{badge('ADD', 'success')} {display_node(node_id)}")

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
                    print_info(f"Auto-created node '{name}'.")
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
                examples="edit 1 2 20\nedit Jakarta Bekasi 20",
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
                examples="remove 1 2\nremove Jakarta Bekasi",
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
    section("CUSTOM MST INPUT", "Build your graph with terminal CRUD commands.")
    hint("Type 'help' to see all commands. Type 'done' when minimum paths are satisfied.")
    show_help()

    while True:
        command = input(prompt()).strip()
        if not command:
            hint("No command entered. Type 'help' if you need guidance.")
            continue

        try:
            parts = shlex.split(command)
        except ValueError as exc:
            print_error(f"Invalid command syntax: {exc}")
            hint("Check quotes and spacing, then try again.")
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
                    examples="title Kabel Internet Antar Daerah",
                )
                continue
            previous = set_graph_title(" ".join(parts[1:]))
            log_update(previous, get_graph_title(), "TITLE")
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
                hint("Add more nodes before finishing.")
                continue
            if len(used_paths) < minimal_path():
                print_warning(f"Minimum paths not met. Required: {minimal_path()}")
                hint("Add more paths until the graph can connect all nodes.")
                continue
            print_success(f"{badge('OK', 'success')} Input complete.")
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

        print_error("Unknown command.", usage="Type 'help' for available commands.")
        hint("Command names are: help, clear, show, title, node, add, edit, remove, done.")

