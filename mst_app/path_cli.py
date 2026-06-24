from .ui import confirm, print_error, print_info


def handle_add_command(parts, session):
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
    id1, miss1 = session.try_resolve_node(node1_val)
    id2, miss2 = session.try_resolve_node(node2_val)
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
            err = session.validate_label(name)
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
            if session.try_resolve_node(name)[0] is None:
                session.create_node(name)
                print_info(f"Auto-created node '{name}'.")
        id1, _ = session.try_resolve_node(node1_val)
        id2, _ = session.try_resolve_node(node2_val)

    if id1 is None or id2 is None:
        return
    if id1 == id2:
        print_error("Nodes cannot be the same.")
        return
    session.create_path(id1, id2, distance)


def handle_edit_command(parts, session):
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
        node1_id = session.resolve_node(parts[1])
        node2_id = session.resolve_node(parts[2])
    except ValueError as exc:
        print_error(str(exc))
        return
    if node1_id == node2_id:
        print_error("Nodes cannot be the same.")
        return
    session.edit_path(node1_id, node2_id, distance)


def handle_remove_command(parts, session):
    if len(parts) != 3:
        print_error(
            "Invalid remove command.",
            usage="remove <node1> <node2>",
            examples="remove 1 2\nremove Jakarta Bekasi",
        )
        return
    try:
        node1_id = session.resolve_node(parts[1])
        node2_id = session.resolve_node(parts[2])
    except ValueError as exc:
        print_error(str(exc))
        return
    if node1_id == node2_id:
        print_error("Nodes cannot be the same.")
        return
    session.remove_path(node1_id, node2_id)

