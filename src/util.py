from gi.repository import Gio

from pyparsing import (
    Word, Literal, Group, Optional, Forward, Suppress, ParserElement, nums,
    oneOf, infixNotation, opAssoc, delimitedList
)


def create_action(action_group, prefix, name, callback,
                  shortcuts=None, parameter=None, target=None):
    """
    Add an action to an action group.

    Args:
        action_group(Gio.SimpleActionGroup): where the actions is added
        prefix(str): prefix used to actions on action group
        name(str): the name of the action
        callback(function): the function to be called when the action is
            activated
        shortcuts(list): an optional list of accelerators
        data(GLib.VariantType): possibles parameters for the action
    """
    action = Gio.SimpleAction.new(name, parameter)
    action.connect("activate", callback)
    action_group.add_action(action)
    detailed_name = f"{prefix}.{name}"

    if (target):
        detailed_name = f"{prefix}.{name}::{target}"

    if shortcuts:
        action_group.set_accels_for_action(detailed_name, shortcuts)


ParserElement.enablePackrat()

# Token para número inteiro
integer = Word(nums)

# Operadores aritméticos
plus = Literal('+')
minus = Literal('-')

# Operador de intervalo e expressão de intervalo (ex.: "3..5")
range_op = Literal("..")
range_expr = Group(integer("start") + range_op + integer("end"))

# Prioriza a alternativa com intervalo para não confundir "1..2" com apenas "1"
number_or_range = range_expr | integer

# Notação de dados: "XdY" (X é opcional, assume "1" se omitido)
dice_notation = Group(
    Optional(integer, default="1")("count") +
    Literal("d") +
    integer("faces")
)

# Declaração recursiva de expressão para permitir aninhamento
expr = Forward()

# Expressões entre parênteses – garantindo que operações externas (como -1) sejam aplicadas após o conteúdo dos parênteses
parenthesized_expr = Group(Suppress("(") + expr + Suppress(")"))

# Um literal inteiro simples (por exemplo, em operações aritméticas)
integer_expr = integer.copy()

# Funções especiais que já havíamos definido:
highest = Group(
    Literal("highest")("command") +
    Optional(number_or_range, default="1")("amount") +
    Literal("in") +
    (parenthesized_expr | dice_notation | integer_expr)("dice")
)

lowest = Group(
    Literal("lowest")("command") +
    Optional(number_or_range, default="1")("amount") +
    Literal("in") +
    (parenthesized_expr | dice_notation | integer_expr)("dice")
)

count = Group(
    Literal("count")("command") +
    delimitedList(number_or_range, delim=",")("values") +
    Literal("in") +
    (parenthesized_expr | dice_notation | integer_expr)("dice")
)

# FUNÇÃO EXPLODE – CORRIGIDA
#
# Aceita:
#  • "explode n in XdY": se os valores n forem informados (podendo ser uma lista, valores separados por vírgula ou um intervalo)
#  • "explode in XdY": se omitido, o valor será definido como o número de faces (Y) do dado.


def default_explode_values(tokens):
    # Se a chave "values" não foi capturada ou está vazia, atribui o número de faces do dado.
    if "values" not in tokens or tokens["values"] == []:
        dice = tokens.dice
        # Tenta obter o valor a partir do campo "faces" (se o operando for a notação de dado)
        if hasattr(dice, "get") and "faces" in dice:
            tokens["values"] = dice["faces"]
        else:
            # Se não houver o campo nomeado, assume que o dado está na forma ['X', 'd', 'Y']
            try:
                tokens["values"] = dice[2]
            except Exception:
                tokens["values"] = ""
    return tokens


explode = Group(
    Literal("explode")("command") +
    Group(Optional(delimitedList(number_or_range, delim=",")))("values") +
    Literal("in") +
    (parenthesized_expr | dice_notation | integer_expr)("dice")
)
explode.setParseAction(default_explode_values)

reroll = Group(
    Literal("reroll")("command") +
    (
        (oneOf("< >")("comparator") + number_or_range("amount")) |
        number_or_range("amount")
    ) +
    Literal("in") +
    (parenthesized_expr | dice_notation | integer_expr)("dice")
)

# O operando estendido aceita expressões entre parênteses, funções ou notações simples
extended_operand = (parenthesized_expr | highest | lowest | count |
                    explode | reroll | dice_notation | integer_expr)

# Define expressões aritméticas com '+' e '-' via infixNotation.
# Assim, em "3d6+3" ou "(explode 4d10)-1", as operações são aplicadas após o fechamento dos parênteses.
arith_expr = infixNotation(extended_operand,
                           [
                               (oneOf('+ -'), 2, opAssoc.LEFT)
                           ])

expr <<= arith_expr

# ---------------------------
# Casos de Teste
# ---------------------------
tests = [
    # Casos para a função explode:
    # Valor informado explicitamente: deve retornar ['explode', '1', 'in', ['4', 'd', '6']]
    "explode 1 in 4d6",
    # Vários valores informados: deve retornar ['explode', ['5','6'], 'in', ['4', 'd', '6']]
    "explode 5,6 in 4d6",
    # Valor informado como intervalo: deve retornar ['explode', ['3', '..', '5'], 'in', ['4', 'd', '10']]
    "explode 3..5 in 4d10",
    # Valor omitido: deve usar o número de faces ("6"), resultando em ['explode', '6', 'in', ['4', 'd', '6']],
    "explode in 4d6",

    # Outros casos já cobertos:
    "5d6",
    "d10",
    "highest 2 in 4d10",
    "highest in 3d8",
    "lowest 3 in 6d12",
    "lowest in 4d10",
    "count 6 in 5d6",
    "count 3,4 in 6d8",
    "count 2..4 in 8d10",
    "reroll < 3 in 4d12",
    "reroll > 4 in 5d10",
    "reroll 3..5 in 4d12",
    "3d6+3",
    "(explode in 4d10)-1",
    "highest 2 in 6d10 + 5",
    "3d6+2-1",
    "(3d6)+5",
    "count 6 in (highest 2 in 5d6)"
]

'''print("Testando gramática com função explode corrigida:")
for test in tests:
    try:
        result = expr.parseString(test, parseAll=True)
        print(f"{test} -> {result.asList()}")
    except Exception as e:
        print(f"Erro ao interpretar '{test}': {e}")'''
