check colors deviation on light theme
Add count compare to dif (count in)
Add count classify (pbta)
Maybe change the general sintaxe?

c3d6,5,6
s3d6|1,2|3,4|5,6


update Translations (done)
change banner color (done)
change icon (done)
update to Gnome 48 (done)
cath over 100 dices, 1000 faces error (done)
check tags (done)
add tip to do reroll previous roll button (done)

Preciso de uma função do pyparsing que receba uma string e faça o parse considerando os seguintes elementos:

numero: numero 1-999
dados: formato xdy, onde x é um numero 1-99, seguido do literal 'd', y é um numero 1-999 ou pelo literal 'f'. Se x estiver ausente é considerado 1. 
funções: formato a:b, onde a é string com até dois caracteres, seguido do literal ':', b é um numero 1-99, um literal '<' ou '>' seguido de um numero 1-99, ou um numero 1-99 seguido do literal '..', seguido de numero 1-99.
operadores: literais '+', '-' e '|'

Segue abaixo exemplos de entradas e saidas da função. Evite utilizar funções externas alem das do pyparsing se possivel, de preferencia a lambda caso necessario. Não adicione comentarios ao codigo. 

"d10" -> [[1, 'd', 10]]
"3df" -> [[3, 'd', 'f']]
"4d6 | h:2  - 1" -> [[[4, 'd', 6],['h',[3, '..', 5]]], '-', 1]
"5d6+1|h:3..5", -> [[[5, 'd', 6], '+', 1]['h',[3, '..', 5]]]
"5d6+1d4|h:3..5|c:>4" -> [[[5, 'd', 6], '+', [1, 'd', 4]], ['h',[3, '..', 5]], ['c',['>', 4]]]
"4d6 | h:2 - 5d10 |c:>4" -> [[[4, 'd', 6], ['h', [2]], '-', [[5, 'd', 10], ['c', [4]]]

