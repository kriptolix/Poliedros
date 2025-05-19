from pyparsing import (
    Word, Literal, Group, Optional, Suppress, alphas, CaselessLiteral,
    oneOf, ZeroOrMore, nums, OneOrMore, Regex, delimitedList
)



def parse_expression(sequence):

    number = Word("123456789", nums, min=1, max=3).setParseAction(
        lambda t: int(t[0])
    )

    plus = (Literal("+"))
    minus = (Literal("-"))
    pipe = Suppress(Literal("|"))
    seperator = Suppress(Literal(":"))    

    range_expression = Group(number + Literal("..") + number)

    number_or_range = range_expression | number

    dice_notation = Group(
        Optional(number, default="1")("count") +
        Literal("d") +
        (number | Literal("f"))("faces")
    )

    multiroll = Group(
        (Literal("multiroll") | Literal("mr"))("command") +
        Group(number_or_range)("amount")
    )

    keep = Group(
        (Literal("highest") | Literal("kh") | 
         Literal("lowest") | Literal("kl"))("command") +
        seperator("separator") +
        Group(Optional(delimitedList(number_or_range, delim=","), default="1"))(
            "amount")
    )   

    count = Group(
        (Literal("count") | Literal("cn") |
         Literal("check") | Literal("ch"))("command") +
        seperator("separator") +
        (
            Group(oneOf("< >")("comparator") + number_or_range("amount")) |
            Group(delimitedList(number_or_range, delim=",")("values")) |
            number_or_range("amount")
        )
    )

    explode = Group(
        (Literal("explode") | Literal("ex"))("command") +
        Group(Optional(delimitedList(number_or_range, delim=",")))("values")
    )

    reroll = Group(
        (Literal("reroll") | Literal("rr"))("command") +
        (
            Group(oneOf("< >")("comparator") + number_or_range("amount")) |
            Group(delimitedList(number_or_range, delim=",")("values")) |
            number_or_range("amount")
        )
    )

    dice_operand = (
        dice_notation + OneOrMore(oneOf("+ -") + (dice_notation | number)))

    extended_operand = (
        keep | count | dice_operand |
        explode | reroll | multiroll | dice_notation | number
    )

    expression = extended_operand + \
        ZeroOrMore((plus | minus | pipe) + extended_operand)

    try:
        result = expression.parseString(sequence, parseAll=True)
        return result.asList()
    except Exception as e:
        print(f"Erro ao interpretar '{sequence}': {e}")
