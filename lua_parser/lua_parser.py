from __future__ import annotations
from .lua_require import (
    mkBinOpSeq, mkOperand, mkOperator, op, maybe, listMap, appendList)
from .lua_lexer import lexall as lexall
from .lua_construct import *
from lark.lexer import Lexer as Lexer
from lark import Transformer as Transformer
from lark import Lark as Lark
from .fable_sedlex.sedlex import from_ustring as from_ustring

tokenmaps = ["SHARP", "MOD", "AMP", "LPAR", "RPAR", "STAR", "PLUS", "COMMA", "MINUS", "DOT", "DOT2", "ELLIPSE", "DIV", "FLOOR_DIV", "COLON", "LABEL", "SEMICOL", "LT", "LSHIFT", "LE", "ASSIGN", "EQ", "GT", "GE", "RSHIFT", "LB", "RB", "CARET", "AND", "BREAK", "DO", "ELSE", "ELSEIF", "END", "FALSE", "FOR", "FUNCTION", "GOTO", "IF", "IN", "LOCAL", "NIL", "NOT", "OR", "REPEAT", "RETURN", "THEN", "TRUE", "UNTIL", "WHILE", "LBRACE", "VBAR", "RBRACE", "INV", "INVEQ", "NAME", "NESTED_STR", "NUMERAL", "STR_LIT", "UNKNOWN"]

tokenreprs = ["\"#\"", "\"%\"", "\"&\"", "\"(\"", "\")\"", "\"*\"", "\"+\"", "\",\"", "\"-\"", "\".\"", "\"..\"", "\"...\"", "\"/\"", "\"//\"", "\":\"", "\"::\"", "\";\"", "\"<\"", "\"<<\"", "\"<=\"", "\"=\"", "\"==\"", "\">\"", "\">=\"", "\">>\"", "\"[\"", "\"]\"", "\"^\"", "\"and\"", "\"break\"", "\"do\"", "\"else\"", "\"elseif\"", "\"end\"", "\"false\"", "\"for\"", "\"function\"", "\"goto\"", "\"if\"", "\"in\"", "\"local\"", "\"nil\"", "\"not\"", "\"or\"", "\"repeat\"", "\"return\"", "\"then\"", "\"true\"", "\"until\"", "\"while\"", "\"{\"", "\"|\"", "\"}\"", "\"~\"", "\"~=\"", "NAME", "NESTED_STR", "NUMERAL", "STR_LIT", "UNKNOWN"]


def construct_token(token_id, lexeme, line, col, span, offset, file):
    if token_id == -1:
        return token("EOF", "")
    return token(tokenmaps[token_id], lexeme, offset, line, col, None, None, span + offset)


def is_eof(token):
    return token.type == "EOF"


class Sedlex(Lexer):
    def __init__(self, lex_conf):
        pass

    def lex(self, raw_string):
        lexbuf = from_ustring(raw_string)
        return lexall(lexbuf, construct_token, is_eof)


class RBNFTransformer(Transformer):
    def binop(self, children):
        return mkOperator(children[0])

    def field_2(self, children):
        return ElementField(children[0])

    def field_1(self, children):
        return NameField(children[0], children[2])

    def field_0(self, children):
        return IndexField(children[0], children[1], children[4])

    def funcname_2(self, children):
        return VarName(children[0])

    def funcname_1(self, children):
        return MethodName(children[0], children[2])

    def funcname_0(self, children):
        return DotName(children[0], children[2])

    def tableconstructor_1(self, children):
        return TableConstructor(children[0], [])

    def tableconstructor_0(self, children):
        return TableConstructor(children[0], children[1])

    def opt_fieldsep_1(self, children):
        return None

    def opt_fieldsep_0(self, children):
        return (children[0])

    def nempty_list_of_field_1(self, children):
        return appendList(children[0], children[2])

    def nempty_list_of_field_0(self, children):
        return [children[0]]

    def parlist_1(self, children):
        return params(children[0], children[1])

    def parlist_0(self, children):
        return params([], (children[0]))

    def nempty_list_of_name_sep_by_comma_1(self, children):
        return appendList(children[0], children[2])

    def nempty_list_of_name_sep_by_comma_0(self, children):
        return [children[0]]

    def varargs_1(self, children):
        return None

    def varargs_0(self, children):
        return (children[1])

    def functiondef_0(self, children):
        return FuncDef(children[0], False, children[1], children[3], children[5])

    def opt_parlist_1(self, children):
        return None

    def opt_parlist_0(self, children):
        return (children[0])

    def opt_funcname_1(self, children):
        return None

    def opt_funcname_0(self, children):
        return (children[0])

    def args_2(self, children):
        return StringArg(children[0])

    def args_1(self, children):
        return TableArgs(children[0])

    def args_0(self, children):
        return PositionalArgs(children[0], children[1])

    def list_of_exp_sep_by_comma_0(self, children):
        return children[0]

    def allow_empty_list_of_exp_sep_by_comma_1(self, children):
        return children[0]

    def allow_empty_list_of_exp_sep_by_comma_0(self, children):
        return []

    def nempty_list_of_exp_sep_by_comma_1(self, children):
        return appendList(children[0], children[2])

    def nempty_list_of_exp_sep_by_comma_0(self, children):
        return [children[0]]

    def atom_8(self, children):
        return TableExpr(children[0])

    def atom_7(self, children):
        return children[0]

    def atom_6(self, children):
        return Ellipse(children[0])

    def atom_5(self, children):
        return String(children[0])

    def atom_4(self, children):
        return String(children[0])

    def atom_3(self, children):
        return Num(children[0])

    def atom_2(self, children):
        return Bool(children[0], True)

    def atom_1(self, children):
        return Bool(children[0], False)

    def atom_0(self, children):
        return Nil(children[0])

    def prefixexp_6(self, children):
        return children[0]

    def prefixexp_5(self, children):
        return Attr(children[0], children[2])

    def prefixexp_4(self, children):
        return Index(children[0], children[2])

    def prefixexp_3(self, children):
        return CallMethod(children[0], children[2], children[3])

    def prefixexp_2(self, children):
        return CallFunc(children[0], children[1])

    def prefixexp_1(self, children):
        return NestedExp(children[0], children[1])

    def prefixexp_0(self, children):
        return Var(children[0])

    def exponent_1(self, children):
        return children[0]

    def exponent_0(self, children):
        return Exponent(children[0], children[2])

    def unaryexp_4(self, children):
        return children[0]

    def unaryexp_3(self, children):
        return Not(children[0], children[1])

    def unaryexp_2(self, children):
        return Inv(children[0], children[1])

    def unaryexp_1(self, children):
        return Neg(children[0], children[1])

    def unaryexp_0(self, children):
        return Len(children[0], children[1])

    def binoperand_0(self, children):
        return mkOperand(children[0])

    def binseq_1(self, children):
        return [children[0]]

    def binseq_0(self, children):
        return appendList(appendList(children[0], children[1]), children[2])

    def binexp_0(self, children):
        return mkBinOpSeq(children[0], Bin, UnsolvedBin)

    def exp_0(self, children):
        return children[0]

    def else_block_0(self, children):
        return if_else(children[0], children[1])

    def elseif_0(self, children):
        return if_elseif(children[0], children[1], children[3])

    def range_tail_1(self, children):
        return None

    def range_tail_0(self, children):
        return (children[1])

    def range_0(self, children):
        return range(children[0], children[2], children[3])

    def opt_assign_rhs_1(self, children):
        return None

    def opt_assign_rhs_0(self, children):
        return (children[1])

    def stat_13(self, children):
        return Assignment(True, listMap(children[1], Var), children[2])

    def stat_12(self, children):
        return ExprStmt(FuncDef(children[0], True, (children[2]), children[4], children[6]))

    def stat_11(self, children):
        return ForInStmt(children[0], children[1], children[3], children[5])

    def stat_10(self, children):
        return ForRangeStmt(children[0], children[1], children[3], children[5])

    def stat_9(self, children):
        return IfStmt(children[0], children[1], children[3], children[4], children[5])

    def stat_8(self, children):
        return RepeatStmt(children[0], children[1], children[3])

    def stat_7(self, children):
        return WhileStmt(children[0], children[1], children[3])

    def stat_6(self, children):
        return DoStmt(children[0], children[1])

    def stat_5(self, children):
        return GotoStmt(children[0], children[1])

    def stat_4(self, children):
        return BreakStmt(children[0])

    def stat_3(self, children):
        return LabelStmt(children[1])

    def stat_2(self, children):
        return ExprStmt(children[0])

    def stat_1(self, children):
        return Assignment(False, children[0], (children[2]))

    def stat_0(self, children):
        return EmptyStmt(children[0])

    def opt_else_1(self, children):
        return None

    def opt_else_0(self, children):
        return (children[0])

    def list_of_elif_0(self, children):
        return children[0]

    def allow_empty_o_nempty_list_of_elif_p__1(self, children):
        return children[0]

    def allow_empty_o_nempty_list_of_elif_p__0(self, children):
        return []

    def nempty_list_of_elif_1(self, children):
        return appendList(children[0], children[1])

    def nempty_list_of_elif_0(self, children):
        return [children[0]]

    def retstat_0(self, children):
        return ReturnStmt(children[0], children[1])

    def opt_semicol_1(self, children):
        return None

    def opt_semicol_0(self, children):
        return (children[0])

    def block_0(self, children):
        return block(children[0], children[1])

    def opt_retstat_1(self, children):
        return None

    def opt_retstat_0(self, children):
        return (children[0])

    def list_of_stat_0(self, children):
        return children[0]

    def allow_empty_list_of_stat_1(self, children):
        return children[0]

    def allow_empty_list_of_stat_0(self, children):
        return []

    def nempty_list_of_stat_1(self, children):
        return appendList(children[0], children[1])

    def nempty_list_of_stat_0(self, children):
        return [children[0]]

    def start(self, children):
        return children[0]

    pass


with (__import__('pathlib').Path(__file__).parent / 'lua.lark').open(encoding='utf8') as grammar_file:
    grammar = grammar_file.read()

parser = Lark(grammar, start='start', parser='lalr', lexer=Sedlex,
              transformer=RBNFTransformer(), keep_all_tokens=True)
