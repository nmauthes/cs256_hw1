import vector_operations as vops

from math import tanh
import random
import sys

def perceptron(x, w, err, theta):
    if err > 0:
        w = vops.sub(x, w)
        theta = theta + 1
    elif err < 0:
        w = vops.add(x, w)
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

    global _ground_fn_type
    if fn_name == 'NBF':
        _ground_fn_type = 'NBF'
    elif fn_name == 'TF':
        _ground_fn_type = 'TF'
    else:
        raise Exception('File not parseable')

    parsed = [str.split() for str in lines]

    return [e for sub in parsed for e in sub] # Flatten list

def generate_ground_function(ground):
    if ground[0] == 'NBF':
        func = build_NBF(ground[1:])
        return lambda x: eval(func)
    elif ground[0] == 'TF':
        func = build_TF(ground[1:])
        return lambda x: eval(func)
    else:
        raise


def build_NBF(params): # Build string to eval as function
    print 'TODO'

def build_TF(params):
    function = ''

    for i, p in enumerate(params[1:]):
        function += p + '*x[' + str(i) +']'

    function += '>=' + params[0]

    global _num_inputs
    _num_inputs = len(params) - 1

    return function

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
            vops.normalize(inputs) # TODO normalize doesn't seem to be working properly

        training_data.append((inputs, ground_fn(inputs)))

    print training_data



def main():
    func = generate_ground_function(parse_ground_file('ground_test.txt')) # test code
    generate_training_data(func, 'bool', 10)

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

