import re

from math import tanh

def get_update_function(name):
    if name == 'perceptron':
        return perceptron
    elif name == 'winnow':
        return winnow
    else:
        raise

def perceptron(w, x, err, theta):
    if err == 0:
        return
    elif err > 0:
        w = sub(w, x)
        theta = theta + 1
    else:
        w = add(w, x)
        theta = theta - 1

    return w, theta

#def winnow(w, x, err, theta=0, alpha=2):


''' Vector ops '''
def add(v1, v2):
    return list(x + y for x, y in zip(v1, v2))

def sub(v1, v2):
    return list(x - y for x, y in zip(v1, v2))

def dot(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))
