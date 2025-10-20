def weightedMedian(n, edges, queries):
    from collections import defaultdict, deque
    
    # Build the graph as an adjacency list
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))
    
    def find_path_and_weights(start, end):
        # Use DFS to find the path and calculate weights
        stack = [(start, -1, 0)]  # (current_node, parent, current_weight)
        parent = {start: None}
        weight_to = {start: 0}
        
        while stack:
            node, par, cur_weight = stack.pop()
            
            for neighbor, weight in graph[node]:
                if neighbor == par:
                    continue
                parent[neighbor] = node
                weight_to[neighbor] = cur_weight + weight
                stack.append((neighbor, node, cur_weight + weight))
                
                if neighbor == end:
                    path = []
                    total_weight = weight_to[end]
                    current = end
                    
                    # Backtrack to find the path from end to start
                    while current is not None:
                        path.append(current)
                        current = parent[current]
                    
                    path.reverse()  # We want the path from start to end
                    return path, total_weight
        
        return [], 0
    
    def find_weighted_median(path, total_weight):
        half_weight = total_weight / 2
        accumulated_weight = 0
        
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            for neighbor, weight in graph[u]:
                if neighbor == v:
                    accumulated_weight += weight
                    break
            if accumulated_weight >= half_weight:
                return v
        
        return path[-1]  # In case we need to return the last node in the path
    
    ans = []
    for uj, vj in queries:
        path, total_weight = find_path_and_weights(uj, vj)
        median_node = find_weighted_median(path, total_weight)
        ans.append(median_node)
    
    return ans


def generated_function(n,edges,queries):
    return weightedMedian(n,edges,queries)

import tracemalloc
import sys
import unittest
import time

total_results = []

def with_memory_trace(n,edges,queries):
    import signal

    class TimeoutException(Exception):
        pass

    def handler(signum, frame):
        raise TimeoutException("Test execution exceeded time limit")

    signal.signal(signal.SIGALRM, handler)
    signal.alarm(10)

    tracemalloc.start()
    snapshot1 = tracemalloc.take_snapshot()
    start_time = time.perf_counter()          # higher-resolution timer

    err = None
    try:
        result = generated_function(n,edges,queries)   # run the wrapped function
    except (Exception, TimeoutException) as e:
        print("Stopped due to error")
        result = -1000000                     # or whatever default
        err = e                                # remember the exception
    finally:
        signal.alarm(0)  # Cancel alarm
        end_time = time.perf_counter()
        snapshot2 = tracemalloc.take_snapshot()
        tracemalloc.stop()

        top_stats = snapshot2.compare_to(snapshot1, 'lineno')
        total_mem = sum(stat.size_diff for stat in top_stats)
        exec_time = (end_time - start_time) * 1000  # ms

        total_results.append((total_mem / 1024, exec_time))  # KB, ms

    if err is not None:
        raise err

    return result


class TestSuite(unittest.TestCase):

    def test_1_minimal_tree(self):
        n = 2
        edges = [[0, 1, 5]]
        queries = [[0, 1]]
        expected = [1]
        result = with_memory_trace(n, edges, queries)
        self.assertEqual(result, expected)

    def test_2_path_tree(self):
        n = 4
        edges = [[0, 1, 3], [1, 2, 2], [2, 3, 1]]
        queries = [[0, 3], [3, 0]]
        expected = [1, 1]
        result = with_memory_trace(n, edges, queries)
        self.assertEqual(result, expected)

    def test_3_star_tree(self):
        n = 5
        edges = [[0,1,1], [0,2,2], [0,3,3], [0,4,4]]
        queries = [[1,4], [2,3], [3,2], [4,1]]
        expected = [4, 3, 0, 0]
        result = with_memory_trace(n, edges, queries)
        self.assertEqual(result, expected)

    def test_4_binary_tree(self):
        # Can do more paths
        n = 7
        edges = [[0,1,1],[0,2,2],[1,3,3],[1,4,4],[2,5,5],[2,6,6]]
        queries = [[3,6], [5,4]]
        expected = [0, 1]
        result = with_memory_trace(n, edges, queries)
        self.assertEqual(result, expected)

    def test_5_equal_weights(self):
        n = 4
        edges = [[0,1,1],[1,2,1],[2,3,1]]
        queries = [[0,3]]
        expected = [2]
        result = with_memory_trace(n, edges, queries)
        self.assertEqual(result, expected)

    def test_6_heavy_leaf(self):
        n = 3
        edges = [[0,1,1],[1,2,10]]
        queries = [[0,2]]
        expected = [2]
        result = with_memory_trace(n, edges, queries)
        self.assertEqual(result, expected)

    def test_7_same_node(self):
        n = 3
        edges = [[0,1,2],[1,2,3]]
        queries = [[1,1]]
        expected = [1]
        result = with_memory_trace(n, edges, queries)
        self.assertEqual(result, expected)

    def test_8_unbalanced_path(self):
        n = 6
        edges = [[0,1,1],[1,2,1],[2,3,1],[3,4,10],[4,5,10]]
        queries = [[0,5], [5,0]]
        expected = [4, 3]
        result = with_memory_trace(n, edges, queries)
        self.assertEqual(result, expected)

    def test_9_deep_path(self):
        n = 10
        edges = [[i, i+1, i+1] for i in range(9)]
        queries = [[0,9]]
        expected = [7]
        result = with_memory_trace(n, edges, queries)
        self.assertEqual(result, expected)

    def test_10_root_to_leaf(self):
        n = 5
        edges = [[0,1,2], [0,2,3], [2,3,4], [2,4,5]]
        queries = [[0,4]]
        expected = [4]
        result = with_memory_trace(n, edges, queries)
        self.assertEqual(result, expected)

    def test_11_reversed_path(self):
        n = 5
        edges = [[0,1,2], [1,2,3], [2,3,4], [3,4,5]]
        queries = [[4,0]]
        expected = [2]
        result = with_memory_trace(n, edges, queries)
        self.assertEqual(result, expected)

    def test_12_light_vs_heavy(self):
        n = 3
        edges = [[0,1,1], [1,2,100]]
        queries = [[0,2]]
        expected = [2]
        result = with_memory_trace(n, edges, queries)
        self.assertEqual(result, expected)

    def test_13_problem_example(self):
        n = 5
        edges = [[0,1,2],[0,2,5],[1,3,1],[2,4,3]]
        queries = [[3,4],[1,2]]
        expected = [2,2]
        result = with_memory_trace(n, edges, queries)
        self.assertEqual(result, expected)

    def test_14_skewed_tree(self):
        n = 6
        edges = [[0,1,1],[1,2,2],[2,3,3],[3,4,4],[4,5,5]]
        queries = [[0,5]]
        expected = [4]
        result = with_memory_trace(n, edges, queries)
        self.assertEqual(result, expected)

    def test_15_uniform_tree(self):
        n = 6
        edges = [[0,1,2],[0,2,2],[1,3,2],[1,4,2],[2,5,2]]
        queries = [[3,5], [0,2], [0,5], [3,2], [4,3], [3,4]]
        expected = [0, 2, 2, 0, 1, 1]
        result = with_memory_trace(n, edges, queries)
        self.assertEqual(result, expected)

    def test_16_large_weight(self):
        n = 2
        edges = [[0,1,100000]]
        queries = [[0,1], [1,0]]
        expected = [1, 0]
        result = with_memory_trace(n, edges, queries)
        self.assertEqual(result, expected)

    def test_17_multiple_queries(self):
        n = 5
        edges = [[0,1,1], [1,2,2], [1,3,3], [3,4,4]]
        queries = [[0,2], [2,4], [0,4], [4,1], [1,4]]
        expected = [2, 3, 3, 3, 4]
        result = with_memory_trace(n, edges, queries)
        self.assertEqual(result, expected)

    def test_18_backtrack(self):
        n = 7
        edges = [[0,1,2],[0,2,2],[1,3,1],[1,4,1],[2,5,1],[2,6,1]]
        queries = [[3,6], [6,3], [4,5], [5,4], [1,2], [2,1]]
        expected = [0, 0, 0, 0, 0, 0]
        result = with_memory_trace(n, edges, queries)
        self.assertEqual(result, expected)

    def test_19_heavy_root(self):
        n = 4
        edges = [[0,1,100],[0,2,1],[2,3,1]]
        queries = [[1,3], [0,3]]
        expected = [0, 2]
        result = with_memory_trace(n, edges, queries)
        self.assertEqual(result, expected)

    def test_20_large_tree(self):
        n = 15
        edges = [[0,1,1],[1,2,1],[1,3,1],[0,4,1],[4,5,1],[4,6,1],[6,7,1],[7,8,1],[7,9,1],[9,10,1],[10,11,1],[11,12,1],[12,13,1],[13,14,1]]
        queries = [[2,14], [8,14], [5,14], [3,14]]
        expected = [9, 11, 10, 9]
        result = with_memory_trace(n, edges, queries)
        self.assertEqual(result, expected)

# To run the tests with custom result reporting
class CustomTestResult(unittest.TextTestResult):
    def stopTestRun(self):
        super().stopTestRun()
        print(f"\nMemory and time usage (KB, ms): {total_results}", file=sys.stderr, flush=True)

if __name__ == '__main__':
    runner = unittest.TextTestRunner(resultclass=CustomTestResult, buffer=False)
    runner.run(unittest.defaultTestLoader.loadTestsFromTestCase(TestSuite))
