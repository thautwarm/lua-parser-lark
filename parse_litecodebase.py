from lua_parser.lua_parser import parser
from wisepy2 import wise
from timeit import default_timer as timer

if __name__ == '__main__':
    from pprint import pprint
    src = open("test.lua").read()
    pprint(parser.parse(src))