import os
import re
import subprocess
import json
import sys

# Given a string with the python function  code, extracts the name 
def extract_function_name(function_string):
    match = re.match(r"\s*def\s+(\w+)\s*\(", function_string)
    if match:
        return match.group(1)
    return None

# Given a string with the python code, extracts the main function 
def extract_function(code_block):
    function_lines = []
    inside_function = False
    function_name = ""
    for line in code_block.splitlines():
        if not inside_function and line.strip().startswith("def "):
            inside_function = True
            function_lines.append(line)
            function_name = extract_function_name(line)
        else:
            if line.strip() == "" or line.startswith(" ") or line.startswith("\t"):
                function_lines.append(line)
            else:
                break  # end of function when a non-indented, non-blank line appears
    return function_name if function_name else None, "\n".join(function_lines) if function_lines else None

# Extracts a python code block
def extract_python_code_block(text):
    match = re.search(r"```python(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

# Extracts the output of the python program
def extract_output(output):
    summary_line = ""
    error_pattern_line = ""
    error_pattern = []
    failed_tests = 0
    mem_and_time_usages = []
    for line in output.splitlines():
        match = re.search(r"[\.FE]+", line)
        if match and not error_pattern_line:
            error_pattern_line = match.group(0)
            error_pattern = [0 if ch == '.' else 1 for ch in error_pattern_line]
        if "FAILED" in line or "failures" in line or "errors" in line:
            summary_line = line.strip()
            break
        if "Memory and time usage" in line:
            match = re.search(r"Memory and time usage \(KB, ms\): \[(.*?)\]", line)
            if match:
                # Parse the full list of tuples from the string after the colon
                mem_and_time_usages = eval(line.split(":", 1)[1].strip())

    if "FAILED" in summary_line:
        # Extract failures and errors counts robustly
        failures = re.search(r'failures=(\d+)', summary_line)
        errors = re.search(r'errors=(\d+)', summary_line)
        if failures:
            failed_tests += int(failures.group(1))
        if errors:
            failed_tests += int(errors.group(1))
        print(f"Error pattern: {error_pattern}")

    return failed_tests, error_pattern, mem_and_time_usages


# Processes each response fille, extracts the function, adds it into a .py file and executes it
def process_response_files(fp, variables):
    test_file_path = f"{fp}test_cases.txt"
    if not os.path.exists(test_file_path):
        print(f"File {test_file_path} not found.")
        return

    failed_tests_summary = {}

    with open(test_file_path, 'r', encoding='utf-8') as test_f:
        test_code = test_f.read()
        for filename in os.listdir(fp):
            if filename.endswith("-response.txt"):
                file_path = os.path.join(fp, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    code = extract_python_code_block(content)
                    if code:
                        func_name, func_code = extract_function(code)
                        if func_code:
                            wrapper = f"def generated_function({variables}):\n    return {func_name}({variables})"
                            combined_code = func_code + "\n\n" + wrapper + "\n\n" + test_code
                            new_filename = filename.replace("-response.txt", "-test.py")
                            new_path = os.path.join(fp, new_filename)
                            with open(new_path, 'w', encoding='utf-8') as test_file:
                                test_file.write(combined_code)

                            print(f"Running tests in {new_filename} ...")
                            result = subprocess.run(["python3", new_path], capture_output=True, text=True)
                            print(result.stdout)
                            if result.stderr:
                                print("Errors:", result.stderr)

                            failed_tests, error_pattern, mem_and_time_usages = extract_output(result.stderr)
                            mem_usage = [x for x,y in mem_and_time_usages]
                            time_usage = [y for x, y in mem_and_time_usages]
                            failed_tests_summary[new_filename] = (failed_tests, error_pattern, mem_usage, time_usage)

    print("\nSummary of failed tests per file:")
    for file, fails in failed_tests_summary.items():
        print(f"{file}:")
        print(f"    fails      {fails[0]}")
        print(f"    test fails {fails[1]}")
        print(f"    mem usage  {fails[2]}")
        print(f"    time usage {fails[3]}")

    # Write or update failed_tests_summary to JSON file with merging
    json_path = os.path.join(fp, "failed_tests_summary.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as json_file:
            existing_summary = json.load(json_file)
        if "iterations" not in existing_summary:
            existing_summary["iterations"] = 1
        iterations = existing_summary["iterations"] + 1
    else:
        existing_summary = {}
        iterations = 0

    # Merge existing_summary with failed_tests_summary
    for key, (failed_count, pattern_list, mem_usage, time_usages) in failed_tests_summary.items():
        if mem_usage and time_usages:
            if key in existing_summary:
                # Concatenate error pattern lists
                existing_summary[key][0] += failed_count
                existing_summary[key][1] = existing_summary[key][0]/iterations
                existing_summary[key][2] = [x + y for x, y in zip(existing_summary[key][2], pattern_list)]
                existing_summary[key][3] = [x + y for x, y in zip(existing_summary[key][3], mem_usage)]
                existing_summary[key][4] = [x + y for x, y in zip(existing_summary[key][4], time_usages)]
            else:
                existing_summary[key] = [failed_count, failed_count, pattern_list, mem_usage, time_usages]

    with open(json_path, "w", encoding="utf-8") as json_file:
        existing_summary["iterations"] = iterations
        json.dump(existing_summary, json_file, indent=4)

    print(f"Updated summary saved to {json_path}")


folder_path =  sys.argv[1] if len(sys.argv) > 1 else "./problem2-4o/"
variables = sys.argv[2] if len(sys.argv) > 2 else "n, present, future, hierarchy, budget"
process_response_files(folder_path, variables)