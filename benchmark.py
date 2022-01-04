from lua_parser.lua_parser import parser
from wisepy2 import wise
from timeit import default_timer as timer

if __name__ == '__main__':
    from pprint import pprint
    src = open("test.lua").read()
    pprint(parser.parse(src))

def main(filename: str, outfile: str, number: int = 1):
    src = open(filename).read()
    start = timer()
    stats = []
    for _ in range(number):
        parser.parse(src)
        stats.append(1000 * (timer() - start)) # unit: ms
        start = timer()
    with open(outfile, 'w', encoding='utf8') as f:
        f.write(','.join(map(str, stats)))