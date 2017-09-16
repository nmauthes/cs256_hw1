import re

from math import tanh

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

def perceptron(x, w, err, theta):
    if err > 0:
        w = sub(x, w)
        theta = theta + 1
    elif err < 0:
        w = add(x, w)
        theta = theta - 1

    return w, theta

def winnow(x, w, err, theta = 0, alpha=2):
    if err > 0:
        w = list(alpha ** -i * j for i, j in zip(x, w))
    elif err < 0:
        w = list(alpha ** i * j for i, j in zip(x, w))

    return w, theta

def parse_ground(filename):
    print 'TODO'

def generate_training_data():
    print 'TODO'

''' Vector ops '''
def add(v1, v2):
    return list(x + y for x, y in zip(v1, v2))

def sub(v1, v2):
    return list(x - y for x, y in zip(v1, v2))

def dot(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

def run(args):
    print 'TODO'