# Validation Patterns

pt_integer = r'^[1-9][0-9]{0,2}+$'
pt_number = r'[1-9][0-9]{0,2}'
pt_operator = r'^[+\-]+$'
pt_dice = r'^[1-9][0-9]?d(f|[1-9][0-9]{0,2})+$'
pt_dice_prefix = r'[1-9][0-9]?d(?:f|[1-9][0-9]{0,2})'
pt_sufix = r'(?=\|[A-Za-z]{{2}}:|$)'

pt_ge_le = rf"[<>]{pt_number}"
pt_range = rf"{pt_number}\.\.{pt_number}"

pt_ex = rf"^(?:{pt_dice_prefix}\|)ex:(?:{pt_number}|{pt_ge_le}|{pt_range})$"
pt_rr = rf"^(?:{pt_dice_prefix}\|)rr:(?:{pt_number}|{pt_ge_le}|{pt_range})$"
pt_mr = rf"^(?:{pt_dice_prefix}\|)mr:(?:{pt_number}|{pt_ge_le}|{pt_range})$"

pt_ex_b = rf"^ex:(?:{pt_number}|{pt_ge_le}|{pt_range})$"
pt_rr_b = rf"^rr:(?:{pt_number}|{pt_ge_le}|{pt_range})$"
pt_mr_b = rf"^mr:(?:{pt_number}|{pt_ge_le}|{pt_range})$"

pt_cn = rf"^cn:(?:{pt_number}|{pt_ge_le}|{pt_range})$"
pt_st = rf"^st:(?:{pt_number})$"
pt_kh = rf"^kh:(?:{pt_number})$"
pt_kl = rf"^kl:(?:{pt_number})$"