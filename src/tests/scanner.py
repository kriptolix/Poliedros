import re

def second_split(token):
    
    token = token.strip()
    
    dice_inline_pattern = re.compile(
        r"^(?P<dice>(?:[1-9]\d?)?d(?:f|[1-9]\d{0,2}))"  # dado: opcionalmente 1 ou 2 dígitos antes de d, depois 'd' e 'f' ou um número de 1 a 3 dígitos
        r"(?P<inline>\|[a-z]{2}:[^|]+)"                  # função inline: pipe, duas letras, dois pontos, e qualquer conjunto de caracteres (exceto outro pipe)
        r"(?P<rest>.*)$"                                 # resto da string (se houver)
    )
    m = dice_inline_pattern.match(token)
    if m:
        # Se batermos, mantemos o dado com sua função inline
        first_token = m.group("dice") + m.group("inline")
        rest = m.group("rest")
        result = [first_token]
        if rest:
            # Se há restante (como em "1d4|kh:3|cn:>4"), dividimos os demais pipes separadamente.
            # Note que o primeiro caractere de rest deve ser "|" para representar a próxima função.
            parts = rest.split('|')
            # Exemplo: rest = "|cn:>4" -> split gera ['', 'cn:>4']
            for part in parts:
                part = part.strip()
                if part:
                    result.append("|" + part)
        return result
    else:
        # Se token não corresponder à notação com função inline,
        # realizamos um split simples pelo "|".
        parts = token.split('|')
        result = []
        for i, part in enumerate(parts):
            part = part.strip()
            if i == 0:
                if part:
                    result.append(part)
            else:
                # Reinserimos o pipe no início para indicar que era originalmente o separador.
                result.append("|" + part)
        return result

def tokenize(expression):
    """
    Recebe a string completa e aplica duas camadas de split.
    
    1. Divide com base nos sinais '+' ou '-' (mantendo esses sinais na lista).
    2. Em cada parte não-operador, aplica a função second_split para dividir por '|'
       respeitando a regra de não separar dados|função inline.
    """
    # Primeira camada: separar operadores ('+' ou '-') pela expressão
    tokens_layer1 = re.split(r'(\+|\-)', expression)
    final_tokens = []
    for token in tokens_layer1:
        token = token.strip()
        if token == "":
            continue
        if token in ['+', '-']:
            final_tokens.append(token)
        else:
            subtokens = second_split(token)
            final_tokens.extend(subtokens)
    return final_tokens


def execute_operations(command):  # 6 - 5d6 + 1d4 |kh:3 |cn:>4

    result = ""
    track = ""
    pool = None
    operation = False

    for parameter in command:  # talvez verificar pares?

        if (re.match(pt_dice, parameter)):
            '''roll, log = roll_dice(parameter)
            pool = roll

            if operation:
                total = sum(roll)
                log = log + f" = {total}"
                operation = False
                pool = None'''
            
            print('dice ', parameter)

        if (re.match(pt_integer, parameter)):
            '''total = parameter
            log = parameter'''

            print('number ', parameter)

        if (re.match(pt_operator, parameter)):
            '''total = parameter
            log = f" {parameter} "
            operation = True'''

            print('operator' , parameter)

        if (re.match(pt_ex, parameter)):  # in: dice, out: list
            # total, log = explode(parameter)

            print('ex ', parameter)
        
        if (re.match(pt_mr, parameter)): # # in: dice, out: list[list] 
            # total, log = explode(parameter)

            print('mr ', parameter)

        if (re.match(pt_rr, parameter)): # # in: dice, out: list
            # total, log = explode(parameter)

            print('rr ', parameter)

        if (re.match(pt_kh, parameter) # in: list, out: list
                or re.match(pt_kl, parameter)):

            '''data = total  # eval(total)?

            if pool:
                data = pool

            total, log = keep_subset(parameter, data)'''

            print('kp ', parameter) 

        if (re.match(pt_cn, parameter)):  # in: list, out: integer
            # total, log = count_in(parameter)
            print('cn', parameter) 
                    

        # stratify, entrada deve ser lista
        

        # result = result + total
        # track = track + log

    results = 0 # [True, eval(result), track]

    return results

# Exemplos de teste:
if __name__ == "__main__":
    examples = [
        "5d6+1d4|kh:3|cn:>4",
        "4d6 | kh:2 + 1",
        "d10",
        "2+3d10",
        "5d6+1|kh:5",
        "4d6 | kh:2 + 5d10 |cn:>4"
    ]
    
    for expr in examples:
        print(f"{expr!r} -> {tokenize(expr)}")

