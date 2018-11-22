def test():
    try:
        a = 5 / 0
    except ZeroDivisionError:
        raise Exception('This is spatar')

try:
    test()
except:
    print('nah')