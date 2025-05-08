from pyparsing import (
    Word, Literal, Group, Optional, Forward, Suppress, ParserElement, nums,
    oneOf, infixNotation, opAssoc, delimitedList
)


def run_postorder(expr):
    """
    Faz uma travessia pós-ordem (postorder) da estrutura em árvore.
    Apenas nós que são listas são retornados.
    """
    nos = []
    if isinstance(expr, list):
        for item in expr:
            nos.extend(run_postorder(item))
            print(item)
        nos.append(expr)
    return nos


def command_parser(command):

    ParserElement.enablePackrat()

    integer = Word(nums)
    positive = Word("123456789", nums)
    plus = Literal('+')
    minus = Literal('-')

    # Operador de intervalo e expressão de intervalo (ex.: "3..5")
    range_op = Literal("..")
    range_expr = integer("start") + range_op + integer("end")

    # Prioriza a alternativa com intervalo para não confundir "1..2" com apenas "1"
    number_or_range = range_expr | integer

    # Notação de dados: "XdY" (X é opcional, assume "1" se omitido)
    dice_notation = Group(
        Optional(integer, default="1")("count") +
        Suppress("d") +
        (integer | (Literal("f"))) ("faces") 
    )

    # Declaração recursiva de expressão para permitir aninhamento
    expr = Forward()

    # Expressões entre parênteses – garantindo que operações externas (como -1) sejam aplicadas após o conteúdo dos parênteses
    parenthesized_expr = Group(Suppress("(") + expr + Suppress(")"))

    # Um literal inteiro simples (por exemplo, em operações aritméticas)
    integer_expr = integer.copy()

    roll = (
        (Optional(Literal("roll"), default="roll"))("command") +
        (dice_notation)("dice")
    )

    highest = (
        Literal("highest")("command") +
        Group(Optional(delimitedList(number_or_range, delim=","), default="1"))("amount") +
        Suppress("in") +
        (parenthesized_expr | dice_notation | integer_expr)("dice")
    )

    lowest = (
        Literal("lowest")("command") +
        Group(Optional(delimitedList(number_or_range, delim=","), default="1"))("amount") +
        Suppress("in") +
        (parenthesized_expr | dice_notation | integer_expr)("dice")
    )

    count = (
        Literal("count")("command") +
        (
            Group((oneOf("< >")("comparator") + number_or_range("amount"))) |
            Group(delimitedList(number_or_range, delim=",")("values")) |
            number_or_range("amount")
        ) +
        Suppress("in") +
        (parenthesized_expr | dice_notation | integer_expr)("dice")
    )

    explode = (
        Literal("explode")("command") +
        Group(Optional(delimitedList(number_or_range, delim=",")))("values") +
        Suppress("in") +
        (parenthesized_expr | dice_notation | integer_expr)("dice")
    )

    reroll = (
        Literal("reroll")("command") +
        (
            (oneOf("< >")("comparator") + number_or_range("amount")) |
            number_or_range("amount")
        ) +
        Suppress("in") +
        (parenthesized_expr | dice_notation | integer_expr)("dice")
    )

    # O operando estendido aceita expressões entre parênteses, funções ou notações simples
    extended_operand = (parenthesized_expr | highest | lowest | count |
                        explode | roll | reroll | dice_notation | integer_expr)

    # Define expressões aritméticas com '+' e '-' via infixNotation.
    # Assim, em "3d6+3" ou "(explode 4d10)-1", as operações são aplicadas após o fechamento dos parênteses.
    arith_expr = infixNotation(extended_operand,
                               [
                                   (oneOf('+ -'), 2, opAssoc.LEFT)
                               ])

    expr <<= arith_expr

    try:
        result = expr.parseString(command, parseAll=True)
        return result
    except Exception as e:
        print(f"Erro ao interpretar '{command}': {e}")
