def operator(n, times: int, op, identity):
    if not times:
        return identity

    div, mod = divmod(times, 2)
    print(div, n)
    result = operator(op(n, n), div, op, identity)

    return op(result, n) if mod else result


def my_pow(base, exp: int):
    return operator(base, exp, lambda a, b: a * b, 1)
