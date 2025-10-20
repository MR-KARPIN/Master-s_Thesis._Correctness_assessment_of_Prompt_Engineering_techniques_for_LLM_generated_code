import json
import matplotlib.pyplot as plt
import numpy as np

# extracts the data of a json into 4 variables
def extract_json_keys(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    if isinstance(data, dict):
        keys = [k for k in data.keys() if k != "iterations"]

        n_tests = 20
        # Initialize lists of lists for each index
        combined_errors = [[] for _ in range(n_tests)]
        combined_mem_usage = [[] for _ in range(n_tests)]
        combined_time_usage = [[] for _ in range(n_tests)]

        for key in keys:
            values = data.get(key)
            if isinstance(values, list) and len(values) >= 5:
                n_errors = values[0]
                mean_errors = values[1]
                errors = values[2]
                mem_usage = values[3]
                time_usage = values[4]

                for i in range(len(errors)):
                    combined_errors[i].append(errors[i])
                    combined_mem_usage[i].append(mem_usage[i])
                    combined_time_usage[i].append(time_usage[i])

        return keys, combined_errors, combined_mem_usage, combined_time_usage

    else:
        print("The JSON file does not contain a top-level object.")
        return [], [], [], []


def plot_heatmap_matplotlib(values_3d, keys, title):
    data = np.array(values_3d).T

    plt.figure(figsize=(12, 8))
    im = plt.imshow(data, aspect='auto', cmap='Reds')

    plt.colorbar(im)
    plt.xticks(ticks=range(data.shape[1]), labels=range(1, data.shape[1] + 1))
    plt.yticks(ticks=range(len(keys)), labels=keys)
    plt.xlabel('Index of tests')
    plt.ylabel('Keys')
    plt.title(title)
    plt.show()


folders = [f'problem{i}-4o' for i in range(1, 6)]
n_folders = len(folders)

# Assume we know the dimensions after first extraction
json_path = f'./{folders[0]}/failed_tests_summary.json'
key_list, errors_list, mem_usage_list, time_usage_list = extract_json_keys(json_path)

# Initialize sum accumulators
sum_errors = np.zeros_like(errors_list, dtype=float)
sum_mem_usage = np.zeros_like(mem_usage_list, dtype=float)
sum_time_usage = np.zeros_like(time_usage_list, dtype=float)

for folder in folders:
    json_path = f'./{folder}/failed_tests_summary.json'
    key_list, errors_list, mem_usage_list, time_usage_list = extract_json_keys(json_path)

    sum_errors = [np.add(sum_errors[i], 0.2 * np.array(errors_list[i])) for i in range(len(errors_list))]
    sum_mem_usage = [np.add(sum_mem_usage[i], 0.2 * np.array(mem_usage_list[i])) for i in range(len(mem_usage_list))]
    sum_time_usage = [np.add(sum_time_usage[i], 0.2 * np.array(time_usage_list[i])) for i in range(len(time_usage_list))]

# Prepare figure with 6 rows (5 folders + 1 sum)
fig, axs = plt.subplots(n_folders + 1, 3, figsize=(18, 4 * (n_folders + 1)))

for row_idx, folder in enumerate(folders):
    json_path = f'./{folder}/failed_tests_summary.json'
    key_list, errors_list, mem_usage_list, time_usage_list = extract_json_keys(json_path)

    data_list = [errors_list, mem_usage_list, time_usage_list]
    titles = ['Errors', 'Memory Usage', 'Time Usage']

    for col_idx, (values_3d, title) in enumerate(zip(data_list, titles)):
        data = np.array(values_3d).T
        ax = axs[row_idx, col_idx]
        im = ax.imshow(data, aspect='auto', cmap='Reds')
        ax.set_title(f'{folder} - {title}')
        ax.set_xlabel('Index of tests')
        ax.set_ylabel('Keys')
        ax.set_xticks(range(data.shape[1]))
        ax.set_xticklabels(range(1, data.shape[1] + 1))
        ax.set_yticks(range(len(key_list)))
        ax.set_yticklabels(key_list)
        fig.colorbar(im, ax=ax)

# Initialize accumulators for scores
error_scores = np.zeros(len(key_list))
mem_scores = np.zeros(len(key_list))
time_scores = np.zeros(len(key_list))

for folder in folders:
    json_path = f'./{folder}/failed_tests_summary.json'
    key_list, errors_list, mem_usage_list, time_usage_list = extract_json_keys(json_path)

    errors_arr = np.array(errors_list)
    mem_arr = np.array(mem_usage_list)
    time_arr = np.array(time_usage_list)

    # max per test (axis=1)
    max_errors = errors_arr.max(axis=1)
    max_mem = mem_arr.max(axis=1)
    max_time = time_arr.max(axis=1)

    # Avoid division by zero
    max_errors[max_errors == 0] = 1
    max_mem[max_mem == 0] = 1
    max_time[max_time == 0] = 1

    # Calculate normalized scores and sum
    error_scores += (errors_arr.T / max_errors).sum(axis=1)
    mem_scores += (mem_arr.T / max_mem).sum(axis=1)
    time_scores += (time_arr.T / max_time).sum(axis=1)

# Plot bar diagrams in the last row using the score aggregations
bar_data_list = [error_scores, mem_scores, time_scores]
bar_titles = ['Total Errors', 'Total Memory Usage', 'Total Time Usage']

for col_idx, (totals, title) in enumerate(zip(bar_data_list, bar_titles)):
    ax = axs[-1, col_idx]
    ax.bar(range(len(key_list)), totals)
    ax.set_title(f'Sum - {title}')
    ax.set_xlabel('Keys')
    ax.set_ylabel(title)
    ax.set_xticks(range(len(key_list)))
    ax.set_xticklabels(key_list, rotation=45, ha='right')

plt.tight_layout()
plt.show()