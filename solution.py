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

# get a penalty
def get_penalty(c1: str, c2: str) -> int:
    if not c1 and not c2:
        return GAP_PENALTY
    if c1 == c2:
        return 0

    return MISMATCH_PENALTY[c1 + c2]

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

# basic solution
def solve_alignment(string1: str, string2: str) -> dict:
    n, m = len(string1), len(string2)
    opt = [[0 for _ in range(n + 1)] for _ in range(m + 1)] 
 
    for i in range(n + 1): 
        opt[0][i] = i * GAP_PENALTY 
    for i in range(m + 1): 
        opt[i][0] = i * GAP_PENALTY 

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            opt[j][i] = min(
                get_penalty(string1[i - 1], string2[j - 1]) + opt[j - 1][i - 1],
                GAP_PENALTY + opt[j - 1][i],
                GAP_PENALTY + opt[j][i - 1]
                )
    
    alignment1, alignment2 = '', ''
    # i, j = n, m
    # while i > 0 or j > 0:
    #     value = opt[j][i]
    #     if value == get_penalty(string1[i - 1], string2[j - 1]) + opt[j - 1][i - 1]:
    #         alignment1 = string1[i - 1] + alignment1
    #         alignment2 = string2[j - 1] + alignment2
    #         i -= 1
    #         j -= 1
    #     elif value == GAP_PENALTY + opt[j - 1][i]:
    #         alignment1 = string1[i - 1] + alignment1
    #         alignment2 = '_' + alignment2
    #         i -= 1
    #     elif value == GAP_PENALTY + opt[j][i - 1]:
    #         alignment1 = '_' + alignment1
    #         alignment2 = string2[j - 1] + alignment2
    #         j -= 1
    
    result = {
        'cost': opt[-1][-1],
        'alignments': [alignment1, alignment2]
    }

    return result


def try_get_argv(index, defualt):
    try:
        return sys.argv[index]
    except:
        return defualt

def main():
    input_file = try_get_argv(1, 'SampleTestCases/input3.txt')
    output_file = try_get_argv(2, 'test/output.txt')
    start_time = time.time()

    strings = construct_strings(input_file)
    solution = solve_alignment(strings[0], strings[1])

    time_used = (time.time() - start_time) * 1000
    memory_used = process_memory()

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        f.write('{}\n{}\n{}\n{}\n{}'.format(solution['cost'], solution['alignments'][0], solution['alignments'][1], time_used, memory_used))


if __name__ == "__main__":
    main()