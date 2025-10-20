import tracemalloc
import sys
import unittest
import time

total_results = []

from heapq import heappush, heappop, heapify


def minimumPairRemoval(nums):
    n = len(nums)
    nums.append(float("inf"))  # Sentinel to avoid bounds check
    left = [-1] + list(range(n))  # Simulated left pointers
    right = list(range(1, n + 1))  # Simulated right pointers

    # Initialize heap with all adjacent pairs
    heap = [(nums[i] + nums[i+1], i) for i in range(n - 1)]
    heapify(heap)

    # Count initial bad pairs
    bad = sum(nums[i] > nums[i + 1] for i in range(n - 1))
    ans = 0

    while bad > 0:
        total, i = heappop(heap)
        j = right[i]

        # Skip invalid pairs (already updated)
        if left[j] != i or nums[i] + nums[j] != total:
            continue

        rr = right[j]

        # Count bad pairs before merging
        pre_bad = int(nums[left[i]] > nums[i]) + int(nums[i] > nums[j]) + int(nums[j] > nums[rr])
        
        # Merge i and j
        nums[i] = total
        right[i] = rr
        if rr < len(nums):
            left[rr] = i

        # Count bad pairs after merging
        post_bad = int(nums[left[i]] > nums[i]) + int(nums[i] > nums[rr])
        bad += post_bad - pre_bad

        # Push updated neighbors into the heap
        if left[i] >= 0:
            heappush(heap, (nums[left[i]] + nums[i], left[i]))
        if rr < n:
            heappush(heap, (nums[i] + nums[rr], i))

        ans += 1

    return ans



def with_memory_trace(nums):
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
        result = minimumPairRemoval(nums)   # run the wrapped function
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

    def test_1_already_non_decreasing(self):
        nums = [1, 2, 3, 4]
        expected = 0
        result = with_memory_trace(nums)
        self.assertEqual(result, expected)

    def test_2_all_elements_equal(self):
        nums = [5, 5, 5, 5]
        expected = 0
        result = with_memory_trace(nums)
        self.assertEqual(result, expected)

    def test_3_strictly_decreasing(self):
        nums = [4, 3, 2, 1]
        expected = 2
        result = with_memory_trace(nums)
        self.assertEqual(result, expected)

    def test_4_two_elements_decreasing(self):
        nums = [3, 1]
        expected = 1
        result = with_memory_trace(nums)
        self.assertEqual(result, expected)

    def test_5_valley_in_the_middle(self):
        nums = [1, 5, 2, 6]
        expected = 3
        result = with_memory_trace(nums)
        self.assertEqual(result, expected)

    def test_6_single_element(self):
        nums = [7]
        expected = 0
        result = with_memory_trace(nums)
        self.assertEqual(result, expected)

    def test_7_two_equal_elements(self):
        nums = [2, 2]
        expected = 0
        result = with_memory_trace(nums)
        self.assertEqual(result, expected)

    def test_8_zigzag_pattern(self):
        nums = [5, 1, 6, 2, 7]
        expected = 4
        result = with_memory_trace(nums)
        self.assertEqual(result, expected)

    def test_9_min_sum_multiple_times(self):
        nums = [3, 1, 4, 1, 5]
        expected = 2
        result = with_memory_trace(nums)
        self.assertEqual(result, expected)

    def test_10_small_dip_at_end(self):
        nums = [1, 2, 3, 0]
        expected = 2
        result = with_memory_trace(nums)
        self.assertEqual(result, expected)

    def test_11_alternating_up_and_down(self):
        nums = [1, 3, 2, 4, 3, 5]
        expected = 4
        result = with_memory_trace(nums)
        self.assertEqual(result, expected)

    def test_12_peak_in_middle(self):
        nums = [1, 6, 1, 2, 3]
        expected = 2
        result = with_memory_trace(nums)
        self.assertEqual(result, expected)

    def test_13_negative_numbers(self):
        nums = [-3, -5, -2, 0]
        expected = 1
        result = with_memory_trace(nums)
        self.assertEqual(result, expected)

    def test_14_large_gap_at_start(self):
        nums = [100, 1, 2, 3]
        expected = 3
        result = with_memory_trace(nums)
        self.assertEqual(result, expected)

    def test_15_reverse_sorted_with_duplicates(self):
        nums = [4, 4, 3, 3, 2, 2]
        expected = 4
        result = with_memory_trace(nums)
        self.assertEqual(result, expected)

    def test_16_empty_array(self):
        nums = []
        expected = 0
        result = with_memory_trace(nums)
        self.assertEqual(result, expected)

    def test_17_large_identical_values(self):
        nums = [10**6] * 10
        expected = 0
        result = with_memory_trace(nums)
        self.assertEqual(result, expected)

    def test_18_large_non_decreasing(self):
        nums = list(range(10**5))
        expected = 0
        result = with_memory_trace(nums)
        self.assertEqual(result, expected)

    def test_19_large_reverse_sorted(self):
        nums = list(range(10**5, 0, -1))
        expected = 99999
        result = with_memory_trace(nums)
        self.assertEqual(result, expected)

    def test_20_large_alternating_high_low(self):
        nums = [i if i % 2 == 0 else 10**6 - i for i in range(10**5)]
        # expected value unknown (can be estimated by running the function)
        result = with_memory_trace(nums)
        self.assertTrue(isinstance(result, int) and result >= 0)

# To run the tests with custom result reporting
class CustomTestResult(unittest.TextTestResult):
    def stopTestRun(self):
        super().stopTestRun()
        print(f"\nMemory and time usage (KB, ms): {total_results}", file=sys.stderr, flush=True)

if __name__ == '__main__':
    runner = unittest.TextTestRunner(resultclass=CustomTestResult, buffer=False)
    runner.run(unittest.defaultTestLoader.loadTestsFromTestCase(TestSuite))
