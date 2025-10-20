def minOperationsToNonDecreasing(nums):
    n = len(nums)
    operations = 0
    
    # Iterate through the array and check adjacent pairs
    i = 0
    while i < n - 1:
        if nums[i] > nums[i + 1]:
            # Replace adjacent pair with their sum
            nums[i + 1] = nums[i] + nums[i + 1]
            operations += 1
            # After replacement, we need to check from the start again
            i = 0
        else:
            # Move to the next pair
            i += 1
    
    return operations


def generated_function(nums):
    return minOperationsToNonDecreasing(nums)

import tracemalloc
import sys
import unittest
import time

total_results = []

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
        result = generated_function(nums)   # run the wrapped function
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
