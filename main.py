import timeit
from utils.generate import generate

if __name__ == '__main__':
    print(timeit.timeit('generate()', 'from utils.generate import generate',
                        number=1))
