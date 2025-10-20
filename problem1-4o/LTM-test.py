def min_insertions_palindrome(s: str) -> str:
    n = len(s)
    
    # dp[i][j] will store the minimum number of insertions needed to make s[i:j+1] a palindrome
    dp = [[0] * n for _ in range(n)]
    
    # Build the dp table
    for length in range(2, n + 1):  # length of the substring
        for i in range(n - length + 1):
            j = i + length - 1
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1]
            else:
                dp[i][j] = min(dp[i + 1][j], dp[i][j - 1]) + 1

    # Reconstruct the palindrome using the dp table
    i, j = 0, n - 1
    res = []
    while i <= j:
        if s[i] == s[j]:
            res.append(s[i])
            i += 1
            j -= 1
        elif dp[i + 1][j] < dp[i][j - 1]:
            res.append(s[i])
            i += 1
        else:
            res.append(s[j])
            j -= 1

    # The first half of the palindrome is in res
    # The second half is the reverse of the first half, without the middle character if the length is odd
    second_half = res[::-1]
    if i - 1 == j + 1:  # odd length palindrome
        res = res + second_half[1:]
    else:
        res = res + second_half

    return ''.join(res)


def generated_function(word):
    return min_insertions_palindrome(word)

import tracemalloc
import sys
import unittest
import time

total_results = []
def with_memory_trace(word):
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
        result = generated_function(word)   # run the wrapped function
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

class TestBuildPalindrome(unittest.TestCase):

    def test_basic_case_1_1(self):
        input_str = 'race'
        expected = 'ecarace'
        result = with_memory_trace(input_str)
        self.assertEqual(result, expected)

    def test_basic_case_2_2(self):
        input_str = 'google'
        expected = 'elgoogle'
        result = with_memory_trace(input_str)
        self.assertEqual(result, expected)

    def test_basic_case_3_3(self):
        input_str = 'abcda'
        expected = 'adcbcda'
        result = with_memory_trace(input_str)
        self.assertEqual(result, expected)

    def test_basic_case_4_4(self):
        input_str = 'adefgfdcba'
        expected = 'abcdefgfedcba'
        result = with_memory_trace(input_str)
        self.assertEqual(result, expected)

    def test_edge_case_empty_5(self):
        input_str = ''
        expected = ''
        result = with_memory_trace(input_str)
        self.assertEqual(result, expected)

    def test_edge_case_single_character_6(self):
        input_str = 'a'
        expected = 'a'
        result = with_memory_trace(input_str)
        self.assertEqual(result, expected)

    def test_edge_case_double_character_7(self):
        input_str = 'aa'
        expected = 'aa'
        result = with_memory_trace(input_str)
        self.assertEqual(result, expected)

    def test_edge_case_two_different_characters_8(self):
        input_str = 'ab'
        expected = 'aba'
        result = with_memory_trace(input_str)
        self.assertEqual(result, expected)

    def test_small_insertion_1_9(self):
        input_str = 'abc'
        expected = 'abcba'
        result = with_memory_trace(input_str)
        self.assertEqual(result, expected)

    def test_small_insertion_2_10(self):
        input_str = 'abb'
        expected = 'abba'
        result = with_memory_trace(input_str)
        self.assertEqual(result, expected)

    def test_small_insertion_3_11(self):
        input_str = 'abba'
        expected = 'abba'
        result = with_memory_trace(input_str)
        self.assertEqual(result, expected)

    def test_small_insertion_4_12(self):
        input_str = 'abcd'
        expected = 'abcdcba'
        result = with_memory_trace(input_str)
        self.assertEqual(result, expected)

    def test_multiple_possible_outputs_1_13(self):
        input_str = 'cab'
        expected = 'bacab'
        result = with_memory_trace(input_str)
        self.assertEqual(result, expected)

    def test_multiple_possible_outputs_2_14(self):
        input_str = 'aabc'
        expected = 'cabaabc'
        result = with_memory_trace(input_str)
        self.assertEqual(result, expected)

    def test_longer_string_1_15(self):
        input_str = 'abcdefgh'
        expected = 'abcdefghgfedcba'
        result = with_memory_trace(input_str)
        self.assertEqual(result, expected)

    def test_longer_string_2_16(self):
        input_str = 'aabbcc'
        expected = 'aabbccbbaa'
        result = with_memory_trace(input_str)
        self.assertEqual(result, expected)

    def test_longer_string_3_17(self):
        input_str = 'banana'
        expected = 'anabanana'
        result = with_memory_trace(input_str)
        self.assertEqual(result, expected)

    def test_case_with_mixed_case_2_18(self):
        input_str = 'aAbB'
        expected = 'aAbBbAa'
        result = with_memory_trace(input_str)
        self.assertEqual(result, expected)

    def test_case_with_mixed_case_3_19(self):
        input_str = 'aaAAaA'
        expected = 'AaaAAaaA'
        result = with_memory_trace(input_str)
        self.assertEqual(result, expected)

    def test_error_case_invalid_input_20(self):
        input_str = 'abc1'
        expected = ''  # Error should be handled and return empty string
        result = with_memory_trace(input_str)
        self.assertEqual(result, expected)


# To run the tests with custom result reporting
class CustomTestResult(unittest.TextTestResult):
    def stopTestRun(self):
        super().stopTestRun()
        print(f"\nMemory and time usage (KB, ms): {total_results}", file=sys.stderr, flush=True)

if __name__ == '__main__':
    runner = unittest.TextTestRunner(resultclass=CustomTestResult, buffer=False)
    runner.run(unittest.defaultTestLoader.loadTestsFromTestCase(TestBuildPalindrome))
