from pyparsing import (
    Word, Literal, Group, Optional, Forward, Suppress, ParserElement, nums,
    oneOf, ZeroOrMore, delimitedList
)


def command_parser(command):

    ParserElement.enablePackrat()

    integer = Word(nums)

    positive = Word("123456789", "0123456789", min=1, max=3)
    plus = Literal('+')
    minus = Literal('-')

    range_op = Literal("..")
    range_expr = integer("start") + range_op + integer("end")

    number_or_range = range_expr | integer

    dice_notation = Group(
        Optional(integer, default="1")("count") +
        Literal("d") +
        (positive | Literal("f"))("faces")
    )

    expr = Forward()

    parenthesized_expr = (Suppress("(") + expr + Suppress(")"))

    integer_expr = integer.copy()

    multiroll = Group(
        Literal("multiroll")("command") +
        Group(number_or_range)("amount") +
        dice_notation("dice")
    )

    highest = Group(
        (Literal("highest") | Literal("h"))("command") +
        Group(Optional(delimitedList(number_or_range, delim=","), default="1"))("amount") +
        Suppress("in") +
        (parenthesized_expr | dice_notation | integer_expr)("dice")
    )

    lowest = Group(
        Literal("lowest")("command") +
        Group(Optional(delimitedList(number_or_range, delim=","), default="1"))("amount") +
        Suppress("in") +
        (parenthesized_expr | dice_notation | integer_expr)("dice")
    )

    count = Group(
        Literal("count")("command") +
        (
            Group(oneOf("< >")("comparator") + number_or_range("amount")) |
            Group(delimitedList(number_or_range, delim=",")("values")) |
            number_or_range("amount")
        ) +
        Suppress("in") +
        (parenthesized_expr | dice_notation | integer_expr)("dice")
    )

    explode = Group(
        Literal("explode")("command") +
        Group(Optional(delimitedList(number_or_range, delim=",")))("values") +
        Suppress("in") +
        (parenthesized_expr | dice_notation | integer_expr)("dice")
    )

    reroll = Group(
        Literal("reroll")("command") +
        (
            Group(oneOf("< >")("comparator") + number_or_range("amount")) |
            Group(delimitedList(number_or_range, delim=",")("values")) |
            number_or_range("amount")
        ) +
        Suppress("in") +
        (parenthesized_expr | dice_notation | integer_expr)("dice")
    )

    extended_operand = (
        parenthesized_expr | highest | lowest | count |
        explode | reroll | multiroll | dice_notation | integer_expr
    )

    expr <<= extended_operand + ZeroOrMore((plus | minus) + extended_operand)

    try:
        result = expr.parseString(command, parseAll=True)
        return result
    except Exception as e:
        print(f"Erro ao interpretar '{command}': {e}")
