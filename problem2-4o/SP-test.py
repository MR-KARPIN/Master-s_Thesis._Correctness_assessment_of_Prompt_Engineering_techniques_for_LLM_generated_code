def calculateEffectiveCosts(n, present, hierarchy):
    from collections import defaultdict, deque

    # Build the tree from hierarchy
    tree = defaultdict(list)
    for boss, employee in hierarchy:
        tree[boss].append(employee)

    # Effective costs array
    effective_costs = present[:]

    # Use BFS or DFS to apply the discount policy
    def applyDiscounts(boss):
        for employee in tree[boss]:
            # Apply the discount if the boss buys their stock
            effective_costs[employee - 1] = min(effective_costs[employee - 1], present[employee - 1] // 2)
            applyDiscounts(employee)

    # Start from the CEO (employee 1)
    applyDiscounts(1)

    return effective_costs


def generated_function(n,present,future,hierarchy,budget):
    return calculateEffectiveCosts(n,present,future,hierarchy,budget)

import unittest
from typing import List
import tracemalloc
import sys
import unittest
import time

total_results = []

def with_memory_trace(n, present, future, hierarchy, budget):
    tracemalloc.start()
    snapshot1 = tracemalloc.take_snapshot()
    start_time = time.perf_counter()          # higher-resolution timer

    err = None
    try:
        result = generated_function(n, present, future, hierarchy, budget)   # run the wrapped function
    except Exception as e:
        result = -1000000                     # or whatever default
        err = e                               # remember the exception
    finally:
        end_time = time.perf_counter()
        snapshot2 = tracemalloc.take_snapshot()
        tracemalloc.stop()

        top_stats = snapshot2.compare_to(snapshot1, 'lineno')
        total_mem = sum(stat.size_diff for stat in top_stats)
        exec_time = (end_time - start_time) * 1000  # ms

        total_results.append((total_mem / 1024, exec_time))  # KB, ms

    # Propagate the original exception *after* logging the stats
    if err is not None:
        raise err

    return result

class TestSuite(unittest.TestCase):
    def test_1_basic_test(self):
        n = 1
        present = [5]
        future = [10]
        hierarchy = []
        budget = 5
        expected = 5  
        result = with_memory_trace(n, present, future, hierarchy, budget)
        self.assertEqual(result, expected)

    def test_2_basic_line(self):
        n = 2
        present = [5, 10]
        future = [10, 15]
        hierarchy = [[1, 2]]
        budget = 10
        expected = 15
        result = with_memory_trace(n, present, future, hierarchy, budget)
        self.assertEqual(result, expected)

    def test_3_basic_decision(self):
        n = 3
        present = [5, 10, 10]
        future = [15, 20, 25]
        hierarchy = [[1, 2], [1, 3]]
        budget = 15
        expected = 30
        result = with_memory_trace(n, present, future, hierarchy, budget)
        self.assertEqual(result, expected)

    def test_4_choose_who_is_the_best(self):
        n = 4
        present = [8, 9, 10, 7]
        future = [15, 18, 21, 12]
        hierarchy = [[1, 2], [2, 3], [3, 4]]
        budget = 10
        expected = 11
        result = with_memory_trace(n, present, future, hierarchy, budget)
        self.assertEqual(result, expected)

    def test_5_whole_line_but_one(self):
        n = 5
        present = [5, 6, 7, 8, 9]
        future = [10, 12, 14, 16, 18]
        hierarchy = [[1, 2], [2, 3], [3, 4], [4, 5]]
        budget = 15
        expected = 37
        result = with_memory_trace(n, present, future, hierarchy, budget)
        self.assertEqual(result, expected)

    def test_6_chooose_different_paths(self):
        n = 5
        present = [5, 5, 5, 5, 5]
        future = [15, 15, 15, 15, 15]
        hierarchy = [[1, 2], [1, 3], [1, 4], [1, 5]]
        budget = 12
        expected = 49
        result = with_memory_trace(n, present, future, hierarchy, budget)
        self.assertEqual(result, expected)

    def test_7_decision_without_discount(self):
        n = 3
        present = [10, 20, 30]
        future = [30, 30, 30]
        hierarchy = [[1, 2], [1, 3]]
        budget = 25
        expected = 20
        result = with_memory_trace(n, present, future, hierarchy, budget)
        self.assertEqual(result, expected)

    def test_8_only_one_option_because_of_budget(self):
        n = 4
        present = [10, 20, 30, 40]
        future = [50, 60, 70, 80]
        hierarchy = [[1, 2], [2, 3], [3, 4]]
        budget = 15
        expected = 40
        result = with_memory_trace(n, present, future, hierarchy, budget)
        self.assertEqual(result, expected)

    def test_9_exclude_ceo(self):
        n = 3
        present = [35, 20, 30]
        future = [40, 50, 60]
        hierarchy = [[1, 2], [2, 3]]
        budget = 40
        expected = 75
        result = with_memory_trace(n, present, future, hierarchy, budget)
        self.assertEqual(result, expected)

    def test_10_zero_budget(self):
        n = 3
        present = [10, 20, 30]
        future = [15, 25, 35]
        hierarchy = [[1, 2], [1, 3]]
        budget = 0
        expected = 0
        result = with_memory_trace(n, present, future, hierarchy, budget)
        self.assertEqual(result, expected)

    def test_11_choose_two_independent_investors(self):
        n = 4
        present = [15, 10, 15, 5]
        future = [25, 18, 30, 13]
        hierarchy = [[1, 2], [2, 3], [3, 4]]
        budget = 15
        expected = 400
        result = with_memory_trace(n, present, future, hierarchy, budget)
        self.assertEqual(result, expected)

    def test_12_complex_tree_with_negative_buys(self):
        n = 5
        present = [10, 20, 30, 40, 50]
        future = [30, 30, 30, 30, 30]
        hierarchy = [[1, 2], [1, 3], [2, 4], [2, 5]]
        budget = 60
        expected = 65
        result = with_memory_trace(n, present, future, hierarchy, budget)
        self.assertEqual(result, expected)

    def test_13_all_negative_profit(self):
        n = 4
        present = [30, 40, 50, 60]
        future = [10, 20, 30, 40]
        hierarchy = [[1, 2], [2, 3], [3, 4]]
        budget = 100
        expected = 0
        result = with_memory_trace(n, present, future, hierarchy, budget)
        self.assertEqual(result, expected)

    def test_14_free_stocks_with_budget_equal_to_one(self):
        n = 4
        present = [1, 1, 1, 1]
        future = [100, 100, 100, 100]
        hierarchy = [[1, 2], [2, 3], [3, 4]]
        budget = 1
        expected = 399
        result = with_memory_trace(n, present, future, hierarchy, budget)
        self.assertEqual(result, expected)

    def test_15_only_one_option_within_budget(self):
        n = 3
        present = [10, 5, 7]
        future = [15, 10, 8]
        hierarchy = [[1, 2], [1, 3]]
        budget = 5
        expected = 3
        result = with_memory_trace(n, present, future, hierarchy, budget)
        self.assertEqual(result, expected)

    def test_16_all_the_same(self):
        n = 5
        present = [10, 10, 10, 10, 10]
        future = [20, 20, 20, 20, 20]
        hierarchy = [[1, 2], [2, 3], [3, 4], [4, 5]]
        budget = 25
        expected = 55
        result = with_memory_trace(n, present, future, hierarchy, budget)
        self.assertEqual(result, expected)

    def test_17_midway_decision(self):
        n = 4
        present = [10, 10, 6, 4, 2]
        future = [20, 20, 18, 10, 4]
        hierarchy = [[1, 2], [2, 3], [3, 4], [3, 5]]
        budget = 10
        expected = 23
        result = with_memory_trace(n, present, future, hierarchy, budget)
        self.assertEqual(result, expected)

    def test_18_tree_structure(self):
        n = 7
        present = [5, 5, 10, 20, 10, 30, 15]
        future = [20, 10, 20, 30, 15, 50, 25]
        hierarchy = [[1, 2], [1, 3], [2, 4], [2, 5], [3, 6], [3, 7]]
        budget = 40
        expected = 93
        result = with_memory_trace(n, present, future, hierarchy, budget)
        self.assertEqual(result, expected)

    def test_19_exclude_ceo_with_two_leaves(self):
        n = 3
        present = [10, 2, 2]
        future = [5, 20, 20]
        hierarchy = [[1, 2], [1, 3]]
        budget = 4
        expected = 36
        result = with_memory_trace(n, present, future, hierarchy, budget)
        self.assertEqual(result, expected)

    def test_20(self):
        n = 10
        present = [10,9,8,7,6,5,4,3,2,1]
        future = [20,18,16,14,12,10,8,6,4,2]
        hierarchy = [[1,2],[1,3],[2,4],[2,5],[3,6],[3,7],[4,8],[4,9],[5,10]]
        budget = 15
        expected = 41
        result = with_memory_trace(n, present, future, hierarchy, budget)
        self.assertEqual(result, expected)

# To run the tests with custom result reporting
class CustomTestResult(unittest.TextTestResult):
    def stopTestRun(self):
        super().stopTestRun()
        print(f"\nMemory and time usage (KB, ms): {total_results}", file=sys.stderr, flush=True)

if __name__ == '__main__':
    runner = unittest.TextTestRunner(resultclass=CustomTestResult, buffer=False)
    runner.run(unittest.defaultTestLoader.loadTestsFromTestCase(TestSuite))
