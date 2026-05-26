import networkx as nx
import matplotlib.pyplot as plt


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


node1 = Node()
node2 = Node()
node3 = Node()
node4 = Node()
node5 = Node()

path1 = Path(node1, node2, 10)
path2 = Path(node1, node4, 7)
path3 = Path(node2, node3, 6)
path4 = Path(node2, node5, 5)
path5 = Path(node4, node3, 4)
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

    # Highlight MST
    mst_edges = []

    for path in mst_paths:
        mst_edges.append((path._path[0], path._path[1]))

    nx.draw_networkx_edges(
        G,
        pos,
        edgelist=mst_edges,
        width=4
    )

    plt.title("Minimum Spanning Tree - Kabel Internet Antar Daerah")
    plt.show()



def main():
    print("PROJECT MST")
    print("Pemasangan Kabel Internet Antar Daerah")

    print("\n=== DAFTAR SEMUA JALUR ===\n")

    for path in Path.get_sorted_paths():
        print(
            f"Node {path._path[0]} "
            f"<--> Node {path._path[1]} "
            f"= {path.distance}"
        )

    mst = kruskal()

    draw_graph(mst)


if __name__ == "__main__":
    main()