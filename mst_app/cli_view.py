from .graph_data import get_graph_title
from .ui import COLORS, THEME

SECTION_WIDTH = 60


class CliView:
    def rule(self, char="=", color_key="secondary"):
        return f"{THEME[color_key]}{char * SECTION_WIDTH}{COLORS['reset']}"

    def section(self, title, subtitle=None):
        print(f"\n{self.rule()}")
        print(f"{COLORS['bold']}{THEME['primary']}{title}{COLORS['reset']}")
        if subtitle:
            print(f"{THEME['muted']}{subtitle}{COLORS['reset']}")
        print(self.rule())

    def prompt(self):
        return (
            f"\n{THEME['primary']}mst-cli"
            f"{COLORS['reset']} "
            f"{THEME['secondary']}>{COLORS['reset']} "
        )

    def hint(self, message):
        print(f"{THEME['muted']}Hint: {message}{COLORS['reset']}")

    def badge(self, label, color_key="info"):
        return f"{THEME[color_key]}[{label}]{COLORS['reset']}"

    def display_name(self, node_labels, node_id):
        label = node_labels.get(node_id, "")
        return label if label else f"Node {node_id}"

    def display_node(self, node_labels, node_id):
        return f"{self.badge(node_id, 'accent')} {self.display_name(node_labels, node_id)}"

    def show_node_list(self, node_labels, longest_id):
        self.section("NODE LIST", "Registered nodes and current labels.")
        if not node_labels:
            return False

        for node_id in sorted(node_labels):
            label = node_labels[node_id]
            color = THEME["primary"] if label else THEME["warning"]
            print(
                f"  {self.badge(f'{node_id:{longest_id}}', 'accent')} "
                f"{color}{self.display_name(node_labels, node_id)}{COLORS['reset']}"
            )
        return True

    def show_help(self, node_count, minimal_path, used_path_count, maksimal_path):
        self.section("HELP / STATUS", "Interactive CRUD for MST graph input.")
        print(f"Graph title      : {THEME['primary']}{get_graph_title()}{COLORS['reset']}")
        print(f"Node count       : {THEME['info']}{node_count}{COLORS['reset']}")
        print(f"Min paths        : {THEME['info']}{minimal_path}{COLORS['reset']}")
        print(
            f"Registered paths : {THEME['info']}{used_path_count}"
            f"{COLORS['reset']} / {THEME['muted']}{maksimal_path}{COLORS['reset']}"
        )
        print(f"\n{COLORS['bold']}{THEME['secondary']}Commands{COLORS['reset']}")
        print(f"  {self.badge('help')} Show command summary and status")
        print(f"  {self.badge('clear')} Clear screen and redraw help")
        print(f"  {self.badge('show')} Show all possible paths and availability")
        print(f"  {self.badge('title <graph title>')} Rename graph title")
        print(f"  {self.badge('node list')} Show current node list")
        print(f"  {self.badge('node <count>')} Create unnamed nodes")
        print(f"  {self.badge('node <label>')} Create one named node")
        print(f"  {self.badge('node <label1,label2,...>')} Create multiple named nodes")
        print(f"  {self.badge('node <count> <label1,label2,...>')} Create many nodes with labels")
        print(f"  {self.badge('node name <id> <label>')} Rename a node")
        print(f"  {self.badge('node remove <id>')} Delete one node")
        print(f"  {self.badge('node remove <id1,id2,...>')} Delete multiple nodes")
        print(f"  {self.badge('add <node1> <node2> <distance>')} Create a path")
        print(f"  {self.badge('edit <node1> <node2> <distance>')} Update a path distance")
        print(f"  {self.badge('remove <node1> <node2>')} Delete a path")
        print(f"  {self.badge('done')} Finish input and run MST")
        print(f"  {self.badge('exit')} Exit custom input")
        self.hint("Use quotes for names with spaces, for example: node \"Jakarta Selatan\"")

    def show_paths(self, node_labels, used_paths, longest_name, longest_index):
        self.section("PATH LIST", "All node pairs and whether a path is already registered.")
        for i in sorted(node_labels):
            for j in sorted(node_labels):
                if i >= j:
                    continue

                edge = (i, j)
                label1 = self.display_name(node_labels, i)
                label2 = self.display_name(node_labels, j)
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

    def show_welcome(self):
        self.section("CUSTOM MST INPUT", "Build your graph with terminal CRUD commands.")
        self.hint("Type 'help' to see all commands. Type 'done' when minimum paths are satisfied.")
