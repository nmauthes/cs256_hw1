import re

from vector_operations import *

from math import tanh
import random
import sys


def perceptron(x, w, err, theta):
    if err > 0:
        w = v_sub(x, w)
        theta = theta + 1
    elif err < 0:
        w = v_add(x, w)
        theta = theta - 1

    return w, theta


def winnow(x, w, err, theta = 1, alpha=2):
    if err > 0:
        w = list(alpha ** -i * j for i, j in zip(x, w))
    elif err < 0:
        w = list(alpha ** i * j for i, j in zip(x, w))

    return w, theta


def get_activation_function(name):
    if name == 'threshold':
        return lambda x, theta: 1 if x > theta else 0
    elif name == 'tanh':
        return lambda x, theta: .5 + .5 * tanh((x - theta) / 2)
    elif name == 'relu':
        return lambda x, theta: max(0, x - theta)
    else:
        raise


def get_update_function(name):
    if name == 'perceptron':
        return perceptron
    elif name == 'winnow':
        return winnow
    else:
        raise

def parse_ground_file(ground_file):
    f = open(ground_file)
    lines = f.readlines()
    f.close()

    fn_name = lines[0].rstrip()

    if fn_name != 'NBF' and fn_name != 'TF':
        raise Exception('File not parseable')

    return [str.split() for str in lines[1:len(lines)]] # Might want to flatten list before passing to fn generator

def generate_ground_function(ground):
    print 'TODO'


def generate_training_data():
    print 'TODO'


def main():
    num_args = len(sys.argv)
    if num_args != 8:
        print 'INCORRECT PARAMETERS'
        print sys.argv
        return
    print sys.argv[1]
    # activation = get_activation_function(sys.argv[0])
    # training_alg = get_update_function(sys.argv[1])


if __name__ == "__main__":
    main()

