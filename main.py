from lua_parser.lua_parser import parser
from pprint import pprint
src = open("test.lua").read()
pprint(parser.parse(src))
