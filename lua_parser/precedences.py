"""
This Python module provides a framework to separate the resolution
of operator precedence and associativity from parsing time,
by using a concise algorithm instead of Shunting Yard algorithm.

Such algorithm is authored by Taine Zhao, and has been named "Operator Bubbling".
--------------------------------------------------------------------------------
Copyright (c) 2022, thautwarm(Taine Zhao)

All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.
    * Neither the name of lark-parsers nor the names of its contributors
    may be used to endorse or promote products derived from this software
    without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
from __future__ import annotations
from collections import defaultdict
import typing as t

__all__ = ["Operator", "binop_reduce"]


class Doubly:
    l: Doubly | None
    v: Operator
    r: Doubly | None

    def __init__(self, left, value, right):
        self.l = left
        self.v = value
        self.r = right


class Operator:
    def __init__(self, opname, val):
        self.opname = opname
        self.val = val


def chunk_by(f, seq):
    if not seq:
        return []
    seq = iter(seq)
    chunk = [next(seq)]
    last = f(chunk[0])
    chunks = []
    for each in seq:
        cur = f(each)
        if cur == last:
            chunk.append(each)
        else:
            chunks.append((last, chunk))
            chunk = [each]
        last = cur

    chunks.append((last, chunk))
    return chunks


lua_precedences = {
    "or": 1,
    "and": 2,
    "<": 3,
    ">": 3,
    ">=": 3,
    "<=": 3,
    "~=": 3,
    "~=": 3,
    "==": 3,
    "|": 4,
    "~": 5,
    "&": 6,
    "<<": 7,
    ">>": 7,
    "..": 8,
    "+": 9,
    "-": 9,
    "*": 10,
    "/": 10,
    "//": 10,
    "%": 10,
}

lua_associativities = defaultdict(lambda: False)
lua_associativities[".."] = True



def binop_reduce(
    cons,
    seq: list,
    precedences: dict[str, int] = lua_precedences,
    associativities: dict[str, bool] = lua_associativities,
):
    start = Doubly(None, None, None)
    last = start
    ops: t.List[Doubly] = []
    for each in seq:
        cur = Doubly(last, each, None)
        if isinstance(each, Operator):
            ops.append(cur)

        last.r = cur
        last = cur

    final = Doubly(last, None, None)
    last.r = final

    # precedence
    ops.sort(key=lambda x: precedences[x.v.opname], reverse=True)

    # associativity
    op_chunks = chunk_by(
        lambda x: (precedences[x.v.opname], associativities[x.v.opname]), ops
    )
    ops = []
    for ((_, is_right_asoc), chunk) in op_chunks:
        ops.extend(reversed(chunk) if is_right_asoc else chunk)

    for op in ops:
        op_v = op.v
        op.v = cons(op_v)(op.l.v, op.r.v)
        op.l = op.l.l
        op.r = op.r.r
        op.l.r = op
        op.r.l = op
    return final.l.v

if __name__ == '__main__':
    seq = [1, Operator("+", "+"), 2, Operator("-", "-"), 3]
    print(binop_reduce(lambda x: lambda l, r: f"{x.val}({l}, {r})", seq))
