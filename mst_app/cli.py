import shlex

from .cli_view import CliView
from .graph_data import get_graph_title, set_graph_title
from .graph_session import GraphSession
from .node_cli import handle_node_command
from .path_cli import handle_add_command, handle_edit_command, handle_remove_command
from .ui import clear_screen, print_error, print_info, print_success, print_warning

DEFAULT_DELAY_LOOP_IN_MS = 0.1


def input_custom_data():
    view = CliView()
    session = GraphSession(view)

    def log_update(previous, current, label=""):
        tag = view.badge(label or "INFO", "info")
        if previous != current:
            print_success(f"{tag} '{previous}' updated to '{current}'")
        else:
            print_info(f"{tag} '{current}' is already in use")

    def show_help():
        view.show_help(
            session.node_count(),
            session.minimal_path(),
            len(session.used_paths),
            session.maksimal_path(),
        )

    clear_screen()
    view.show_welcome()
    show_help()

    while True:
        command = input(view.prompt()).strip()
        if not command:
            view.hint("No command entered. Type 'help' if you need guidance.")
            continue

        try:
            parts = shlex.split(command)
        except ValueError as exc:
            print_error(f"Invalid command syntax: {exc}")
            view.hint("Check quotes and spacing, then try again.")
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
            session.show_paths()
            continue

        if action == "node":
            handle_node_command(parts, session, DEFAULT_DELAY_LOOP_IN_MS)
            continue

        if action == "done":
            if session.node_count() < 2:
                print_warning("At least 2 nodes are required.")
                view.hint("Add more nodes before finishing.")
                continue
            if len(session.used_paths) < session.minimal_path():
                print_warning(
                    f"Minimum paths not met. Required: {session.minimal_path()}"
                )
                view.hint("Add more paths until the graph can connect all nodes.")
                continue
            print_success(f"{view.badge('OK', 'success')} Input complete.")
            break

        if action == "add":
            handle_add_command(parts, session)
            continue

        if action == "edit":
            handle_edit_command(parts, session)
            continue

        if action == "remove":
            handle_remove_command(parts, session)
            continue

        print_error("Unknown command.", usage="Type 'help' for available commands.")
        view.hint("Command names are: help, clear, show, title, node, add, edit, remove, done.")

