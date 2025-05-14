from pyparsing import (
    Word, Literal, Group, Optional, Suppress, alphas,
    oneOf, ZeroOrMore 
)


def parse_expression(command):

    func_id = Word(alphas, min=1, max=2)

    func_number = Word("123456789", "0123456789", min=1, max=3).setParseAction(
        lambda tokens: int(tokens[0]))

    dice_expr = Group(
        Optional(func_number, default="1")("count") +
        Literal("d") +
        (func_number | Literal("f"))("faces")
    )

    plus = Literal("+")
    minus = Literal("-")
    pipe = Suppress("|")

    op = plus | minus | pipe

    comparator = oneOf("> <")
    comp_expr = Group(comparator + func_number)

    range_expr = Group(func_number + Literal("..") + func_number)

    func_param = range_expr | comp_expr | func_number

    func_expr = Group(func_id + Suppress(":") + func_param)

    operand = dice_expr | func_expr | func_number

    expression = operand + ZeroOrMore(op + operand)

    try:
        result = expression.parseString(command)
        return result
    except Exception as e:
        print(f"Erro ao interpretar '{command}': {e}")