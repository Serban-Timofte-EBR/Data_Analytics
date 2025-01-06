def functie1(*args):
    print(type(args))
    for p in args:
        print(type(p), p)


def functie2(**kwargs):
    print(type(kwargs))
    for k in kwargs.keys():
        print(k, kwargs[k], sep="=")


functie1(2, 7, [1, 2, 3, 4])
functie2(a=10, b=90, c=[1, 2, 3, 4])
