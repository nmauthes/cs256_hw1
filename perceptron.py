import vector_operations as vops

from math import tanh
import random
import sys
import re


def perceptron(x, w, err, theta):
    if err > 0:
        w = vops.sub(x, w)
        theta = theta + 1
    elif err < 0:
        w = vops.add(x, w)
        theta = theta - 1

    return w, theta


def winnow(x, w, err, theta, alpha=2):
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
    print(fn_name)

    global _ground_fn_type
    if fn_name == 'NBF':
        _ground_fn_type = 'NBF'
    elif fn_name == 'TF':
        _ground_fn_type = 'TF'
    else:
        raise Exception('File not parseable')

    parsed = [line.split() for line in lines]

    return [e for sub in parsed for e in sub] # Flatten list


def generate_ground_function(ground_file_name):
    ground = parse_ground_file(ground_file_name)
    print(ground[0])
    if ground[0] == 'NBF':
        func = build_nbf(ground[1:])
        return lambda x: eval(func)
    elif ground[0] == 'TF':
        func = build_tf(ground[1:])
        return lambda x: int(eval(func))
    else:
        raise


def build_nbf(params):  # Build string to eval as function
    func = '(x[' + params[0] + '] ' + params[1].lower() + ' x[' + params[2] + '])'
    print func
    iterable = iter(params[3:])
    for param in iterable:
        operation = param
        num = int(next(iterable))
        negation = ''
        if num < 0:
            negation = 'not'
            num *= -1
        func = ' '.join(['(' + func, negation, operation.lower(), 'x[' + str(num) + '])'])

    print func
    return func


def build_tf(params):
    func = ''

    for i, p in enumerate(params[1:]):
        func += p + '*x[' + str(i) +']'

    func += '>=' + params[0]

    global _num_inputs
    _num_inputs = len(params) - 1

    return func


def generate_training_data(ground_fn, dist, num_train):
    if dist == 'bool' or _ground_fn_type == 'NBF':
        random_func = 'random.randint(0, 1)' # better way to do this?
    elif dist == 'sphere':
        random_func = 'random.random()'
    else:
        raise

    training_data = []
    for n in range(0, num_train):
        inputs = [eval(random_func) for m in range(0, _num_inputs)]

        if dist == 'sphere':
            inputs = vops.normalize(inputs)

        training_data.append((inputs, ground_fn(inputs)))

    print training_data
    return training_data

def train_perceptron(activation, training_alg, training_data):
    w = [random.random() for n in range(0, _num_inputs)]
    theta = 0.1

    for x, y in training_data:
        result = vops.dot(x, w)
        err = y - activation(result, theta)
        new_w, new_theta = training_alg(x, w, err, theta)

        if w != new_w:
            w = new_w
            theta = new_theta
            print str(x) + ':' + str(y) +':Update'
        else:
            print str(x) + ':' + str(y) +':No Update'

def test_perceptron():
    pass


def main():
    num_args = len(sys.argv)
    if num_args != 8:
        print 'INCORRECT PARAMETERS'
        print sys.argv
        return

    activation = get_activation_function(sys.argv[1])
    training_alg = get_update_function(sys.argv[2])
    ground_file_name = sys.argv[3]
    distribution = sys.argv[4]
    num_train = sys.argv[5]
    num_test = sys.argv[6]
    epsilon = sys.argv[7]

    func = generate_ground_function(ground_file_name)
    training_data = generate_training_data(func, 'bool', 1000)
    train_perceptron(activation, training_alg, training_data)

if __name__ == "__main__":
    main()

