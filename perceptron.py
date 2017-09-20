import vector_operations as vops

from math import tanh
import random
import sys

__num_inputs = 0
__ground_fn_type = ''


def perceptron(x, w, err, theta):
    classification = vops.dot(x, w)
    if classification >= theta and err != 0:  # positive classification
        w = vops.sub(x, w)
        theta = theta + 1
    elif classification < theta and err != 0:  # negative classification
        w = vops.add(x, w)
        theta = theta - 1

    return w, theta


def winnow(x, w, err, theta, alpha=2):
    classification = vops.dot(x, w)
    if classification >= theta and err != 0:  # positive classification
        w = list(alpha ** -i * j for i, j in zip(x, w))
    elif classification < theta and err != 0:  # negative classification
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

    global __ground_fn_type
    if fn_name == 'NBF':
        __ground_fn_type = 'NBF'
    elif fn_name == 'TF':
        __ground_fn_type = 'TF'
    else:
        raise Exception('File not parseable')

    parsed = [line.split() for line in lines]

    return [e for sub in parsed for e in sub]  # Flatten list


def generate_ground_function(ground_file_name):
    ground = parse_ground_file(ground_file_name)
    if ground[0] == 'NBF':
        func = build_nbf(ground[1:])
        return lambda x: int(eval(func))
    elif ground[0] == 'TF':
        func = build_tf(ground[1:])
        return lambda x: int(eval(func))
    else:
        raise


def build_nbf(params):  # Build string to eval as function
    if len(params) < 3:
        raise

    num = int(params[0])
    negation = ''
    if num < 0:
        negation = 'not '
        num *= -1
    num -= 1
    max_num = num
    func = ' '.join([negation + 'x[' + str(num) + ']'])

    iterable = iter(params[1:])
    for param in iterable:
        operation = param
        num = int(next(iterable))
        negation = ''
        if num < 0:
            negation = 'not '
            num *= -1
        num -= 1
        if num > max_num:
            max_num = num
        func = ' '.join(['(' + func, operation.lower(), negation + 'x[' + str(num) + '])'])

    global __num_inputs
    __num_inputs = max_num + 1
    print 'num_inputs: ' + str(__num_inputs)
    print 'NBF function: ' + func
    return func


def build_tf(params):
    func = ''

    for i, p in enumerate(params[1:]):
        func += p + '*x[' + str(i) + ']'

    func += '>=' + params[0]

    global __num_inputs
    __num_inputs = len(params) - 1

    return func


def generate_training_data(ground_fn, dist, num_train):
    if dist == 'bool' or __ground_fn_type == 'NBF':
        random_func = 'random.randint(0, 1)'  # better way to do this?
    elif dist == 'sphere':
        random_func = 'random.random()'
    else:
        raise

    training_data = []
    for n in range(0, num_train):
        inputs = [eval(random_func) for m in range(0, __num_inputs)]
        if dist == 'sphere' and __ground_fn_type != 'NBF':
            inputs = vops.normalize(inputs)

        training_data.append((inputs, ground_fn(inputs)))

    return training_data


def train_perceptron(activation, training_alg, training_data):
    w = [random.random() for n in range(0, __num_inputs)]
    theta = 0.1

    for x, y in training_data:
        result = vops.dot(x, w)
        err = abs(y - activation(result, theta))
        new_w, new_theta = training_alg(x, w, err, theta)

        copy_x = []
        for field in x:
            copy_x.append(str(field))

        if w != new_w:
            w = new_w
            theta = new_theta
            print ','.join(copy_x) + ':' + str(y) + ':update'
        else:
            print ','.join(copy_x) + ':' + str(y) + ':no update'

        # print 'error:' + str(err)
        # print 'theta:' + str(theta)

    return w, theta


def test_perceptron(activation, epsilon, testing_data, w, theta):
    errors = []
    for x, y_actual in testing_data:
        result = vops.dot(x, w)
        y_prediction = activation(result, theta)
        err = abs(y_actual - y_prediction)
        errors.append(err)

        print str(x) + ':' + str(y_prediction) + ':' + str(y_actual) + ':' + str(err)
    # print(sum(errors))
    # print(len(errors))
    avg_error = float(sum(errors)) / len(errors)
    print 'Average error:' + str(avg_error)
    print 'Epsilon:' + str(epsilon)

    if avg_error <= epsilon:
        print 'TRAINING SUCCEEDED'
    else:
        print 'TRAINING FAILED'


def main(num_runs=1):
    num_args = len(sys.argv)
    if num_args != 8:
        print 'INCORRECT PARAMETERS'
        print sys.argv
        return

    activation = get_activation_function(sys.argv[1])
    training_alg = get_update_function(sys.argv[2])
    ground_file_name = sys.argv[3]
    distribution = sys.argv[4]
    num_train = int(sys.argv[5])
    num_test = int(sys.argv[6])
    epsilon = float(sys.argv[7])

    for n in range(0, num_runs):
        func = generate_ground_function(ground_file_name)
        # if _ground_fn_type == 'NBF':
        #     print generate_training_data(func, 'bool', 10)
        # else:
        #     print generate_training_data(func, distribution, 10)

        training_data = generate_training_data(func, distribution, num_train)
        results = train_perceptron(activation, training_alg, training_data)
        weights = results[0]
        theta = results[1]

        testing_data = generate_training_data(func, distribution, num_test)
        test_perceptron(activation, epsilon, testing_data, weights, theta)

if __name__ == "__main__":
    main()

