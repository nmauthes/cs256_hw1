from math import sqrt

# Vector ops


def v_add(v1, v2):
    return [x + y for x, y in zip(v1, v2)]


def v_sub(v1, v2):
    return [x - y for x, y in zip(v1, v2)]


def dot(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))


def scalar_mult(v1, c):
    return [c * x for x in v1]


def mag(v1):
    return sqrt(sum(x**2 for x in v1))


def normalize(v1):
    return [x / mag(v1) for x in v1]