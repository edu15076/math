def extended_euclidian(a: int, b: int) -> tuple:
    x2, y2, x1, y1 = 1, 0, 0, 1
    q, r = divmod(a, b)
    while r:
        x = x2 - x1 * q
        y = y2 - y1 * q
        x2, y2 = x1, y1
        x1, y1 = x, y

    return b, x1, y1

# def find_
