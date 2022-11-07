from math import inf
import os
import sys
import psutil
import time


# penalties
GAP_PENALTY = 30
MISMATCH_PENALTY = {
    'AC': 110, 'CA': 110,
    'AG': 48, 'GA': 48,
    'AT': 94, 'TA': 94,
    'CG': 118, 'GC': 118,
    'CT': 48, 'TC': 48,
    'GT': 110, 'TG': 110,
}

# get penalty
def get_penalty(c1: str, c2: str) -> int:
    if not c1 and not c2 or c1 == '_' or c2 == '_':
        return GAP_PENALTY
    if c1 == c2:
        return 0

    return MISMATCH_PENALTY[c1 + c2]

# calculate the cost of 2 strings
def calculate_cost(x: str, y: str) -> int:
    result = 0
    for i in range(len(x)):
        result += get_penalty(x[i], y[i])
    return result

# construct the 2 strings from a file
def construct_strings(path: str) -> list[str]:
    result = []
    with open(path) as f:
        lines = f.read().splitlines()

        for line in lines:
            if line.isnumeric():
                index = int(line) + 1
                string = result[-1]
                result[-1] = string[:index] + string + string[index:]
            else:
                result.append(line)
    
    return result

# get memory usage
def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed

# get costs
def get_costs(x: str, y: str) -> list[int]:
    n, m = len(x), len(y)
    opt = [[0 for _ in range(2)] for _ in range(m + 1)] 
 
    for i in range(2): 
        opt[0][i] = i * GAP_PENALTY 
    for i in range(m + 1): 
        opt[i][0] = i * GAP_PENALTY 

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            opt[j][1] = min(
                get_penalty(x[i - 1], y[j - 1]) + opt[j - 1][0],
                GAP_PENALTY + opt[j - 1][1],
                GAP_PENALTY + opt[j][0]
                )
        
        for row in opt:
            row[0] = row[1]
            row[1] = 0
        opt[0][1] = (i + 1) * GAP_PENALTY

    return [row[0] for row in opt]
    

# solution
def solve_alignment(x: str, y: str) -> list[str]:
    n, m = len(x), len(y)
    if not x and not y:
        return [x, y]
    elif not x:
        return ['_' * m, y]
    elif not y:
        return [x, '_' * n]

    x_split_index = n // 2
    x_left, x_right = x[:x_split_index], x[x_split_index:]

    cost_left = get_costs(x_left, y)
    cost_right = get_costs(x_right[::-1], y[::-1])

    min_cost = inf
    y_split_index = 0
    for i in range(m + 1):
        cost = cost_left[i] + cost_right[m - i]
        if cost <= min_cost:
            min_cost = cost
            y_split_index = i

    y_left, y_right = y[:y_split_index], y[y_split_index:]

    if not x_left and not y_left:
        a, b = len(x_right), len(y_right)
        if a < b:
            x_right += '_' * (b - a)
        elif a > b:
            y_right += '_' * (a - b)
        return [x_right, y_right]
    else:
        alignments_left = solve_alignment(x_left, y_left)
        alignments_right = solve_alignment(x_right, y_right)

        return [alignments_left[0] + alignments_right[0][::-1], alignments_left[1] + alignments_right[1][::-1]]


def try_get_argv(index, defualt):
    try:
        return sys.argv[index]
    except:
        return defualt

def main():
    sys.setrecursionlimit(100000)

    input_file = try_get_argv(1, 'SampleTestCases/input5.txt')
    output_file = try_get_argv(2, 'test/efficient-output.txt')
    
    start_time = time.time()

    strings = construct_strings(input_file)
    solution = solve_alignment(strings[0], strings[1])

    time_used = (time.time() - start_time) * 1000
    memory_used = process_memory()

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        f.write('{}\n{}\n{}\n{}\n{}'.format(calculate_cost(solution[0], solution[1]), solution[0], solution[1], time_used, memory_used))


if __name__ == "__main__":
    main()