import os
import psutil


input_path = 'datapoints'
output_path = 'output'

for i in range(1, 16):
    input_file = '{}/in{}.txt'.format(input_path, i)

    os.system("python basic_3.py {} {}".format(input_file, '{}/basic/data{}.txt'.format(output_path, i)))
    os.system("python efficient_3.py {} {}".format(input_file, '{}/efficient/data{}.txt'.format(output_path, i)))
