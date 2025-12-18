import unittest
from graph import Digraph, Node, WeightedEdge

def load_map(map_filename:str) -> Digraph:
    with open(map_filename, "r") as file:
        data = file.readlines()
    new_map = Digraph()
    for entry in data:
        source, destination, total_dist, outdoor_dist = entry.strip().split(' ')
        new_source = Node(source)
        if not new_map.has_node(new_source):
            new_map.add_node(new_source)
        new_dest = Node(destination)
        if not new_map.has_node(new_dest):
            new_map.add_node(new_dest)
        new_map.add_edge(WeightedEdge(source, destination, total_dist, outdoor_dist))
    return new_map

def get_best_path(digraph:Digraph, start:str, end:str, path:list[list[str],int], 
    max_dist_outdoors:int, best_dist:int, best_path:list[str]) -> tuple[str] | None:
    def best_path_helper(digraph:Digraph, start:str, end:str, path:list[list[str],int], 
    max_dist_outdoors:int, best_dist:int, best_path:list[str]):
        if not(digraph.has_node(Node(start)) and digraph.has_node(Node(end))):
            raise ValueError("Start or end node not in graph")
        elif start == end:
            if (best_path == [] or path[1] < best_dist) and path[2] <= max_dist_outdoors:
                return (path[0], path[1])
            else:
                return None
        else:
            for edge in digraph.get_edges_for_node(start):
                if edge.get_destination() in path[0]:
                    continue
                possible_path = best_path_helper(digraph, edge.get_destination(), end,
                    [path[0] + [edge.get_destination()], path[1] + edge.get_total_distance(),
                    path[2] + edge.get_outdoor_distance()], max_dist_outdoors, best_dist, best_path)
                if possible_path is not None:
                    if best_path == [] or possible_path[1] < best_dist:
                        best_path = possible_path[0]
                        best_dist = possible_path[1]
            if best_path == []:
                return None
            else:
                return (best_path, best_dist)
    result = best_path_helper(digraph, start, end, path, 
    max_dist_outdoors, best_dist, best_path)
    return tuple(result[0]) if result is not None else None

# Problem 3c: Implement directed_dfs
def directed_dfs(digraph, start, end, max_total_dist, max_dist_outdoors):
    path = get_best_path(digraph, start, end, [[start], 0, 0], max_dist_outdoors, max_total_dist, [])
    if path is None:
        raise ValueError("No path found")
    return list(path)


# ================================================================
# Begin tests -- you do not need to modify anything below this line
# ================================================================

class Ps2Test(unittest.TestCase):
    LARGE_DIST = 99999

    def setUp(self):
        self.graph = load_map("mit_map.txt")

    def test_load_map_basic(self):
        self.assertTrue(isinstance(self.graph, Digraph))
        self.assertEqual(len(self.graph.nodes), 37)
        all_edges = []
        for _, edges in self.graph.edges.items():
            all_edges += edges  # edges must be dict of node -> list of edges
        all_edges = set(all_edges)
        self.assertEqual(len(all_edges), 129)

    def _print_path_description(self, start, end, total_dist, outdoor_dist):
        constraint = ""
        if outdoor_dist != Ps2Test.LARGE_DIST:
            constraint = "without walking more than {}m outdoors".format(
                outdoor_dist)
        if total_dist != Ps2Test.LARGE_DIST:
            if constraint:
                constraint += ' or {}m total'.format(total_dist)
            else:
                constraint = "without walking more than {}m total".format(
                    total_dist)

        print("------------------------")
        print("Shortest path from Building {} to {} {}".format(
            start, end, constraint))

    def _test_path(self,
                   expectedPath,
                   total_dist=LARGE_DIST,
                   outdoor_dist=LARGE_DIST):
        start, end = expectedPath[0], expectedPath[-1]
        self._print_path_description(start, end, total_dist, outdoor_dist)
        dfsPath = directed_dfs(self.graph, start, end, total_dist, outdoor_dist)
        print("Expected: ", expectedPath)
        print("DFS: ", dfsPath)
        self.assertEqual(expectedPath, dfsPath)

    def _test_impossible_path(self,
                              start,
                              end,
                              total_dist=LARGE_DIST,
                              outdoor_dist=LARGE_DIST):
        self._print_path_description(start, end, total_dist, outdoor_dist)
        with self.assertRaises(ValueError):
            directed_dfs(self.graph, start, end, total_dist, outdoor_dist)

    def test_path_one_step(self):
        self._test_path(expectedPath=['32', '56'])

    def test_path_no_outdoors(self):
        self._test_path(
            expectedPath=['32', '36', '26', '16', '56'], outdoor_dist=0)

    def test_path_multi_step(self):
        self._test_path(expectedPath=['2', '3', '7', '9'])

    def test_path_multi_step_no_outdoors(self):
        self._test_path(
            expectedPath=['2', '4', '10', '13', '9'], outdoor_dist=0)

    def test_path_multi_step2(self):
        self._test_path(expectedPath=['1', '4', '12', '32'])

    def test_path_multi_step_no_outdoors2(self):
        self._test_path(
            expectedPath=['1', '3', '10', '4', '12', '24', '34', '36', '32'],
            outdoor_dist=0)

    def test_impossible_path1(self):
        self._test_impossible_path('8', '50', outdoor_dist=0)

if __name__ == "__main__":
    unittest.main()
