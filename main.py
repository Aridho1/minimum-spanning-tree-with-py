import json
from platform import node


class Node:
    _id: int = 0
    _self_map = {}

    def __init__(self) -> None:
        Node._id += 1
        self._id = Node._id

        Node._self_map[Node._id] = self


class Path:
    _id: int = 0
    _self_map = {}

    def __init__(self, node1: Node, node2: Node, distance: int = 0) -> None:
        Path._id += 1
        self._id = Path._id

        self._path = [node1._id, node2._id]
        self.distance = distance

        Path._self_map[Path._id] = self

    @classmethod
    def get_sorted_paths(cls):
        return sorted(
            cls._self_map.values(),
            key=lambda path: path.distance
        )

    @classmethod
    def getSortedPathMaps(cls, isConvertDataToDict: bool = True):
        result = []

        for path in cls._self_map.values():
            data = (
                path.__dict__
                if isConvertDataToDict
                else path
            )

            result.append([path.distance, data])

        return result

    @classmethod
    def getPathAndDistanceFromNodeOrNodeId(cls, nodeOrNodeId: Node | int):

        if isinstance(nodeOrNodeId, Node):
            node = nodeOrNodeId

        elif isinstance(nodeOrNodeId, int):
            node = Node._self_map.get(nodeOrNodeId)

            if node is None:
                raise ValueError("Node ID tidak valid")

        else:
            raise TypeError("Input harus berupa objek Node atau Integer ID")

        result = []

        for path in cls._self_map.values():
            if node._id in path._path:
                result.append({
                    "id": path._id,
                    "path": path._path,
                    "distance": path.distance
                })

        return result


node1 = Node()
node2 = Node()
node3 = Node()
node4 = Node()
node5 = Node()

path1 = Path(node1, node2, 10)
path2 = Path(node1, node4, 7)
path3 = Path(node2, node3, 6)
path4 = Path(node2, node5, 5)
path5 = Path(node4, node3, 9)
path6 = Path(node4, node5, 9)
path7 = Path(node3, node5, 8)


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

    print("\n=== PROSES ALGORITMA KRUSKAL ===\n")

    for path in sorted_paths:
        node1 = path._path[0]
        node2 = path._path[1]

        print(
            f"Memeriksa jalur "
            f"{node1} <--> {node2} "
            f"dengan jarak {path.distance}"
        )

        if union(node1, node2):
            mst.append(path)
            total_distance += path.distance

            print("Jalur ditambahkan ke MST\n")

        else:
            print("Jalur ditolak karena membentuk cycle\n")

    print("\n=== HASIL MINIMUM SPANNING TREE ===\n")

    for path in mst:
        print(
            f"Node {path._path[0]} "
            f"<--> Node {path._path[1]} "
            f"= {path.distance}"
        )

    print(f"\nTotal Minimum Distance = {total_distance}")


def main():
    print("PROJECT MST")
    print("Pemasangan Kabel Internet Antar Daerah")

    print("\n=== DAFTAR SEMUA JALUR ===\n")

    sorted_paths = Path.get_sorted_paths()

    for path in sorted_paths:
        print(
            f"Node {path._path[0]} "
            f"<--> Node {path._path[1]} "
            f"= {path.distance}"
        )

    kruskal()


if __name__ == "__main__":
    main()