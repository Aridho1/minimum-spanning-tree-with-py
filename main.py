import json
from platform import node


class Node:
    _id: int = 0
    _self_map = {}

    def __init__(self) -> None:
        ...

        Node._id += 1
        self._id = Node._id

        Node._self_map[Node._id] = self

class Path:
    _id: int = 0
    _self_map = {}
    _path = []
    _path_maps = []

    def __init__(self, node1: Node, node2: Node, distance: int = 0) -> None:
        ...

        Path._id += 1
        self._id = Path._id

        path = [node1._id, node2._id]

        # Path._self_map[Path._id] = {
        #     "id": Path._id,
        #     "path": path,
        #     "distance": distance
        # }

        # Path._path_maps

        self._path = path
        self.distance = distance

        # print(f"{Path._id = }")
        Path._self_map[Path._id] = self

    @classmethod
    def get_sorted_paths(cls):
        return sorted(
            cls._self_map.values(),
            key=lambda path: path.distance
        )

    @classmethod 
    def getSortedPathMaps(self, isConvertDataToDict: bool | int = True):
        ...

        _res = []

        for id, path in Path._self_map.items():
            ...
            # print(f"{id}: {path._id}")
            d = [path.distance, (path.__dict__, path)[not not isConvertDataToDict]]
            # print(path.__dict__)
            # print("d: " + json.dumps(path.__dict__, indent=4))
            
            _res.append(d)

        return _res
        return _res.sort(key=lambda x: x[1]._id)

        # return res

    @classmethod
    def getPathAndDistanceFromNodeOrNodeId(self, nodeOrNodeId: Node | int):
        ...
        
        if isinstance(nodeOrNodeId, Node):
            node = nodeOrNodeId
        elif isinstance(nodeOrNodeId, int):
            try:
                node = Node._self_map.get(id)
            except KeyError as err:
                raise ValueError("Data Tidak Valid karena 'node id' tidak valid")
        else:
            raise TypeError("Input harus berupa objek Node atau Integer ID")

        res = []
        print(f"{node._id = }")

        for key, path in Path._self_map.items():
            ...
            print(f"{path = }")
            if not isinstance(path, dict):
                # print(f"{path} itu bukan dict")
                continue
            
            if "id" not in path or "path" not in path or "distance" not in path:
                # print(f"node id {node._id} is not found in {path["path"]}")
                continue
            
            if node._id in path["path"]:
                res.append(path)
            else:
                ...
                # print(f"node id {node._id} is not found in {path["path"]}")
        
        return res

node1 = Node()
node2 = Node()
node3 = Node()
node4 = Node()
node5 = Node()

path1 = Path(node1, node2, 10)
path2 = Path(node1, node4, 7)
path3 = Path(node2, node3, 6)
path4 = Path(node2, node5, 5)
path5 = Path(node4, node3, 4 + 5)
path6 = Path(node4, node5, 9)
path7 = Path(node3, node5, 8)

def main():
    ...
    print("hello world\n\n")

    # sortedPathMap = Path.getSortedPathMaps()
    sortedPathMap = Path.get_sorted_paths()

    for path in sortedPathMap:
        ...
        print(path.__dict__)

    
    # print(sortedPathMap[0].__dict__)
    # print(json.dumps(Path.get_sorted_paths(), indent=4))

    # print(Path._self_map[1])
    # print(json.dumps(Node._self_map, indent=4))
    # print(json.dumps(Path._self_map[1].__dict__, indent=4))
    # print(json.dumps(Path._self_map, indent=4))

    # path1BelongsTo = Path.getPathAndDistanceFromNodeOrNodeId(node1)

    # print("\n\n\npath1BelongsTo = " + json.dumps(path1BelongsTo, indent=4))

if __name__ == "__main__":
    main()