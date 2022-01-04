# An out-of-box Lua parser written in Lark

Such parser handles a relaxed version of Lua 5.3 grammar.

This is a Python-Lark implementation of Lua 5.3 parser. It has the following features:

1. the grammar is compatible to LALR(1)/LR(1)/ALL(*)
2. the generated parser creates declarative and typed Python dataclasses instead of error-prone CSTs -- that's why we call it "out-of-box".


[Fable.Sedlex](https://github.com/thautwarm/Fable.Sedlex), which is an F\# port of OCaml sedlex project and transpiled into Python, is used in this parser to achieve high-quality lexer that avoids unnecessary collisions of lexical rules.

## Motivation

This project serves as a control group of comparisons against Typed BNF. We tend to show the conciseness, declarativity, simplicity, and other advantages of TypedBNF.

## Limitations

It supports full lua 5.3 syntax except

1. assignment left-hand side can take arbitrary expressions, which is invalid in real lua syntax. This can be checked after parsing.

2. support for nested literal strings is limited: only `[[...]]`, `[[=]]`, `[=[...]=]` are correctly supported.

3. comments support only `-- ...` form, i.e., line comments.

