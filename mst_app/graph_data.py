_graph_title = "Kabel Internet Antar Daerah"


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
        return sorted(cls._self_map.values(), key=lambda path: path.distance)


def get_graph_title():
    return _graph_title


def set_graph_title(title):
    global _graph_title
    previous = _graph_title
    _graph_title = title
    return previous


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
    Path(node3, node4, 4)
    Path(node3, node5, 8)
    Path(node4, node5, 9)

