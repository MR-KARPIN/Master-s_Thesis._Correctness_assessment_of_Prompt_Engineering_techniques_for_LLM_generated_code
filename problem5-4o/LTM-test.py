def max_min_manhattan_distance(side, k, points):
    # Helper function to check if a distance d is feasible
    def can_select_k_points_with_distance(d):
        # Try selecting points greedily
        selected = [points[0]]
        
        for point in points[1:]:
            if all(abs(point[0] - sel[0]) + abs(point[1] - sel[1]) >= d for sel in selected):
                selected.append(point)
                if len(selected) >= k:
                    return True
        return False

    # Sort points to ease selection
    points.sort()
    
    # Binary search for the maximum minimum distance
    left, right = 0, 2 * side
    best_distance = 0
    
    while left <= right:
        mid = (left + right) // 2
        if can_select_k_points_with_distance(mid):
            best_distance = mid
            left = mid + 1
        else:
            right = mid - 1
    
    return best_distance


def generated_function(side,points,k):
    return max_min_manhattan_distance(side,points,k)

import tracemalloc
import sys
import unittest
import time

total_results = []

def with_memory_trace(side,k,points):
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
        result = generated_function(side,k,points)   # run the wrapped function
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

    def test_1_minimum_valid_input(self):
        side = 1
        k = 2
        points = [[0, 0], [1, 0]]
        expected = 1
        result = with_memory_trace(side, k, points)
        self.assertEqual(result, expected)

    def test_2_all_corners_choose_2(self):
        side = 2
        k = 2
        points = [[0, 0], [0, 2], [2, 0], [2, 2]]
        expected = 4
        result = with_memory_trace(side, k, points)
        self.assertEqual(result, expected)

    def test_3_all_corners_choose_3(self):
        side = 2
        k = 3
        points = [[0, 0], [0, 2], [2, 0], [2, 2]]
        expected = 2
        result = with_memory_trace(side, k, points)
        self.assertEqual(result, expected)

    def test_4_single_edge(self):
        side = 5
        k = 2
        points = [[0, 0], [0, 5], [0, 2]]
        expected = 5
        result = with_memory_trace(side, k, points)
        self.assertEqual(result, expected)

    def test_5_midpoints_of_edges(self):
        side = 4
        k = 2
        points = [[0, 2], [2, 0], [4, 2], [2, 4]]
        expected = 8
        result = with_memory_trace(side, k, points)
        self.assertEqual(result, expected)

    def test_6_equidistant_on_edge(self):
        side = 6
        k = 3
        points = [[0, 0], [0, 3], [0, 6]]
        expected = 3
        result = with_memory_trace(side, k, points)
        self.assertEqual(result, expected)

    def test_7_points_close_together(self):
        side = 4
        k = 2
        points = [[0, 0], [0, 1], [0, 2]]
        expected = 2
        result = with_memory_trace(side, k, points)
        self.assertEqual(result, expected)

    def test_8_dense_on_one_edge(self):
        side = 10
        k = 2
        points = [[0, i] for i in range(11)]
        expected = 10
        result = with_memory_trace(side, k, points)
        self.assertEqual(result, expected)

    def test_9_opposite_corners(self):
        side = 7
        k = 2
        points = [[0, 0], [7, 7]]
        expected = 14
        result = with_memory_trace(side, k, points)
        self.assertEqual(result, expected)

    def test_10_corners_and_midpoints(self):
        side = 6
        k = 4
        points = [[0, 0], [0, 6], [6, 0], [6, 6], [0, 3], [3, 0], [6, 3], [3, 6]]
        expected = 6
        result = with_memory_trace(side, k, points)
        self.assertEqual(result, expected)

    def test_11_uniform_on_perimeter(self):
        side = 4
        k = 2
        points = [[0, 0], [0, 2], [0, 4], [2, 4], [4, 4], [4, 2], [4, 0], [2, 0]]
        expected = 8
        result = with_memory_trace(side, k, points)
        self.assertEqual(result, expected)

    def test_12_all_points_same(self):
        side = 3
        k = 2
        points = [[0, 0], [0, 0], [0, 0]]
        expected = 0
        result = with_memory_trace(side, k, points)
        self.assertEqual(result, expected)

    def test_13_insufficient_separation(self):
        side = 10
        k = 5
        points = [[0, i] for i in range(5)]
        expected = 1
        result = with_memory_trace(side, k, points)
        self.assertEqual(result, expected)

    def test_14_choose_farthest_diff_edges(self):
        side = 8
        k = 2
        points = [[0, 0], [0, 8], [8, 0], [8, 8]]
        expected = 16
        result = with_memory_trace(side, k, points)
        self.assertEqual(result, expected)

    def test_15_only_vertical_edge(self):
        side = 10
        k = 3
        points = [[0, 0], [0, 5], [0, 10]]
        expected = 5
        result = with_memory_trace(side, k, points)
        self.assertEqual(result, expected)

    def test_16_only_horizontal_edge(self):
        side = 12
        k = 4
        points = [[0, 0], [4, 0], [8, 0], [12, 0]]
        expected = 4
        result = with_memory_trace(side, k, points)
        self.assertEqual(result, expected)

    def test_17_multiple_points_all_edges(self):
        side = 3
        k = 4
        points = [[0, 0], [1, 0], [2, 0], [3, 0], [0, 3], [1, 3], [2, 3], [3, 3]]
        expected = 3
        result = with_memory_trace(side, k, points)
        self.assertEqual(result, expected)

    def test_18_large_grid_corners_only(self):
        side = 10**6
        k = 2
        points = [[0, 0], [0, side], [side, 0], [side, side]]
        expected = 2_000_000
        result = with_memory_trace(side, k, points)
        self.assertEqual(result, expected)

    def test_19_large_evenly_spaced_points(self):
        side = 10000
        k = 100
        points = [[0, i * 100] for i in range(101)]
        expected = 100
        result = with_memory_trace(side, k, points)
        self.assertEqual(result, expected)

    def test_20_maxed_out_perimeter(self):
        side = 1000
        k = 100
        points = (
            [[0, i] for i in range(0, 1001, 10)] +
            [[1000, i] for i in range(0, 1001, 10)] +
            [[i, 0] for i in range(10, 1000, 10)] +
            [[i, 1000] for i in range(10, 1000, 10)]
        )
        
        result = with_memory_trace(side, k, points)
        self.assertTrue(isinstance(result, int) and result >= 0)


# To run the tests with custom result reporting
class CustomTestResult(unittest.TextTestResult):
    def stopTestRun(self):
        super().stopTestRun()
        print(f"\nMemory and time usage (KB, ms): {total_results}", file=sys.stderr, flush=True)

if __name__ == '__main__':
    runner = unittest.TextTestRunner(resultclass=CustomTestResult, buffer=False)
    runner.run(unittest.defaultTestLoader.loadTestsFromTestCase(TestSuite))
