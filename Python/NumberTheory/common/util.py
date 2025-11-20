def cfor(start, stop: callable, step: callable = lambda i: 1):
    i = start
    while stop(i):
        yield i
        i = step(i)
