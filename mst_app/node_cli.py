import time

from .ui import confirm, print_error, print_info, print_success


def handle_node_command(parts, deps):
    view = deps["view"]
    node_labels = deps["node_labels"]
    validate_label = deps["validate_label"]
    create_nodes_count = deps["create_nodes_count"]
    create_node = deps["create_node"]
    display_node = deps["display_node"]
    display_name = deps["display_name"]
    set_node_name = deps["set_node_name"]
    remove_nodes = deps["remove_nodes"]
    delay = deps["delay"]

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
        deps["show_node_list"]()
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
        print_success(f"{view.badge('DEL', 'success')} Node(s) removed successfully.")
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
        print_success(f"{view.badge('ADD', 'success')} Added {count} node(s).")
        for node_id in node_ids:
            print(f"  {display_node(node_id)}")
        return

    if arg.isdigit():
        count = int(arg)
        if count <= 0:
            print_error("Node count must be greater than 0.")
            return
        create_nodes_count(count)
        print_success(f"{view.badge('ADD', 'success')} Added {count} node(s).")
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
            time.sleep(delay)
            node_id = create_node(label)
            if node_id:
                print(f"  {view.badge(node_id, 'accent')} {display_name(node_id)}")
        return

    err = validate_label(arg)
    if err:
        print_error(err)
        return
    node_id = create_node(arg)
    print_success(f"{view.badge('ADD', 'success')} {display_node(node_id)}")

