from .graph_data import Node, Path
from .ui import confirm, print_error, print_info, print_success, print_warning


class GraphSession:
    def __init__(self, view):
        self.view = view
        self.node_labels = {}
        self.used_paths = {}

    def display_name(self, node_id):
        return self.view.display_name(self.node_labels, node_id)

    def display_node(self, node_id):
        return self.view.display_node(self.node_labels, node_id)

    def find_node_by_label(self, label):
        label_lower = label.lower()
        for node_id, stored in self.node_labels.items():
            if stored and stored.lower() == label_lower:
                return node_id
        return None

    def validate_label(self, label, exclude_node_id=None):
        if not label or not label.strip():
            return "Label cannot be empty."
        if label.strip().isdigit():
            return "Label cannot contain only digits."
        existing = self.find_node_by_label(label)
        if existing is not None and existing != exclude_node_id:
            return f"Label '{label}' is already used by node {existing}."
        return None

    def try_resolve_node(self, value):
        if value.isdigit():
            node_id = int(value)
            if node_id in self.node_labels:
                return node_id, None
            return None, value
        found = self.find_node_by_label(value)
        if found is not None:
            return found, None
        return None, value

    def resolve_node(self, value):
        node_id, _ = self.try_resolve_node(value)
        if node_id is None:
            if value.isdigit():
                raise ValueError(f"Node {value} does not exist.")
            raise ValueError(f"Node '{value}' does not exist.")
        return node_id

    def create_node(self, label=""):
        if label:
            err = self.validate_label(label)
            if err:
                print_error(err)
                return None
        node = Node()
        self.node_labels[node._id] = label if label else ""
        return node._id

    def create_nodes_count(self, count):
        created = []
        for _ in range(count):
            node_id = self.create_node()
            if node_id is None:
                return created
            created.append(node_id)
        return created

    def remove_node(self, node_id):
        if node_id not in self.node_labels:
            return
        del self.node_labels[node_id]
        del Node._self_map[node_id]
        edges_to_remove = [edge for edge in self.used_paths if node_id in edge]
        for edge in edges_to_remove:
            del self.used_paths[edge]
        path_ids_to_remove = [
            path_id
            for path_id, path_obj in Path._self_map.items()
            if node_id in path_obj._path
        ]
        for path_id in path_ids_to_remove:
            del Path._self_map[path_id]

    def remove_nodes(self, node_ids):
        for node_id in node_ids:
            self.remove_node(node_id)

    def set_node_name(self, node_id, label):
        if node_id not in self.node_labels:
            print_error(f"Node {node_id} does not exist.")
            return
        err = self.validate_label(label, exclude_node_id=node_id)
        if err:
            print_error(err)
            return
        current = self.node_labels[node_id]
        if current:
            if not confirm(
                [
                    f"{self.display_node(node_id)} is currently named:",
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
        self.node_labels[node_id] = label
        print_success(
            f"{self.view.badge('OK', 'success')} {self.display_node(node_id)} renamed to '{label}'."
        )

    def create_path(self, node1_id, node2_id, distance):
        edge = tuple(sorted((node1_id, node2_id)))
        if edge in self.used_paths:
            print_warning("Path already registered.")
            return False
        self.used_paths[edge] = distance
        Path(Node._self_map[node1_id], Node._self_map[node2_id], distance)
        print_success(
            f"{self.view.badge('ADD', 'success')} {self.display_name(node1_id)} <--> "
            f"{self.display_name(node2_id)} = {distance}"
        )
        return True

    def edit_path(self, node1_id, node2_id, distance):
        edge = tuple(sorted((node1_id, node2_id)))
        if edge not in self.used_paths:
            print_warning("Path is not registered.")
            return False
        self.used_paths[edge] = distance
        for path_obj in Path._self_map.values():
            if tuple(sorted(path_obj._path)) == edge:
                path_obj.distance = distance
                break
        print_success(
            f"{self.view.badge('EDIT', 'success')} {self.display_name(node1_id)} <--> "
            f"{self.display_name(node2_id)} = {distance}"
        )
        return True

    def remove_path(self, node1_id, node2_id):
        edge = tuple(sorted((node1_id, node2_id)))
        if edge not in self.used_paths:
            print_warning("Path is not registered.")
            return False
        del self.used_paths[edge]
        target_path_id = None
        for path_id, path_obj in Path._self_map.items():
            if tuple(sorted(path_obj._path)) == edge:
                target_path_id = path_id
                break
        if target_path_id:
            del Path._self_map[target_path_id]
        print_success(
            f"{self.view.badge('DEL', 'success')} Removed path "
            f"{self.display_name(node1_id)} <--> {self.display_name(node2_id)}"
        )
        return True

    def get_longest_node_labels(self):
        if not self.node_labels:
            return 0
        return max(len(self.display_name(node_id)) for node_id in self.node_labels)

    def get_longest_node_id(self):
        return len(str(max(self.node_labels)))

    def node_count(self):
        return len(self.node_labels)

    def maksimal_path(self):
        total = self.node_count()
        return total * (total - 1) // 2

    def minimal_path(self):
        total = self.node_count()
        return max(0, total - 1) if total >= 2 else 0

    def show_node_list(self):
        rendered = self.view.show_node_list(self.node_labels, self.get_longest_node_id())
        if not rendered:
            print_info("No nodes have been created yet.")
            self.view.hint("Use 'node 5' or 'node Jakarta,Bandung' to start.")

    def show_paths(self):
        if self.node_count() < 2:
            self.view.section("PATH LIST", "All node pairs and whether a path is already registered.")
            print_info("At least 2 nodes are needed before paths can be inspected.")
            self.view.hint("Create nodes first, then use 'show' again.")
            return
        self.view.show_paths(
            self.node_labels,
            self.used_paths,
            self.get_longest_node_labels(),
            len(str(max(self.node_labels))),
        )

