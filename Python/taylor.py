import numpy


def taylor_trigonometric(alpha, term):
    alpha = numpy.fmod(alpha, 2 * numpy.pi)
    s = term

    for i in range(2 if term == 1 else 3, 18, 2):
        term = -term * alpha * alpha / (i * (i - 1))
        s += term

    return s


def sin(alpha):
    return taylor_trigonometric(alpha, alpha)


def cos(alpha):
    return taylor_trigonometric(alpha, 1)


def tan(alpha):
    return sin(alpha) / cos(alpha)
