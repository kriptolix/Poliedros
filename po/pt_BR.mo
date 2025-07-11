��    #      4  /   L        �   	  �    {  �  #  C  �   g  �   W	  �  0
  f  �  �   N     5     E     Q     _     m     �     �     �     �     �      �                    (     9  	   E  �   O     �               #     ;     G     V    i  �   �  �  �  �  E  .  �  �     �     �  �  u  �  �   ,     !     3     A     P     b     {     �  #   �     �     �  )   �               *     ?     O  	   `  �   j     6     K  5   Q     �     �     �     �                                                     #                                                                     
             	      "   !             <b>Additions/Subtractions:</b> "+" and "-" operators.
                    
<b>Ex.:</b> 1d6 + 3, roll 1 6-sided die and add the number 3.
<b>Ex.:</b> 2d8 - 1d4, roll 2 8-sided dice and subtract the result of rolling 1 4-sided die.
                     <b>Count in:</b> operator "|cn:parameters".
                    
<b>Ex.:</b> 6d10|cn:6,8,10; roll 4 10-sided dice and count how many 6s,8s and 10s occur.
<b>Ex.:</b> 4d4|cn:4; roll 4 4-sided dice and count how many 4s occur.
<b>Ex.:</b> 6d20|cn:>15; roll 6 20-sided dice and count how many results greater than 15 occur.
<b>Ex.:</b> 3d100|cn:80..90; roll 3 100-sided dice and count how many results between 80 and 90 occur occur.
                     <b>Exploding dice:</b> operator "|ex:parameters".
                    
<b>Ex.:</b> 6d6|ex:6, roll 6 6-sided dice and, if any of them result in a 6, roll that die again, add to the result and so on.
<b>Ex.:</b> 5d10|ex:>8, roll 5 10-sided dice and, if any of the results is greater than 8, roll that die again, add to the result and so on.                    
                     <b>Functions parameters:</b>

<b>Ex.:</b> >15: greater than number(inclusive).
<b>Ex.:</b> 6,8,10: relation of arbitrary numbers.
<b>Ex.:</b> 4: a single number.
<b>Ex.:</b> &lt;10: lower than number (inclusive).
<b>Ex.:</b> 80..90: interval between numbers (inclusive).
                     <b>Keeping higher:</b> operator "|kh:number".
                    
<b>Ex.:</b> 3d6|kh:2, roll 3 6-sided dice and keep the 2 highest.
<b>Ex.:</b> 2d20|kh:1, roll 2 20-sided dice and keep the highest.                    
                     <b>Keeping lower:</b> operator "|kl:number".
                    
<b>Ex.:</b> 4d10|kl:2, roll 4 10-sided dice and keep the 2 lowest.
<b>Ex.:</b> 3d6|kl:1, roll 3 6-sided dice and keep the lowest.
                     <b>Nested functions:</b> You can use the result of one function as an input for another function.
                    
<b>Ex.:</b> 6d6|ex:6|cn:6, roll 6 6-sided dice and, if any of them result in a 6, roll that die again, add to the result and so on.Then, count how many 6s occur.
<b>Ex.:</b> 5d10|kh:1|cn:>8, roll 5 10-sided dice and keep the highest, then, check if the result is greater than 8.                    
                     <b>Reroll dice:</b> operator "|rr:parameters".
                    
<b>Ex.:</b> 6d6|rr:6, roll 6 6-sided dice and, if any of them result in a 6, reroll that die and keep the new result.
<b>Ex.:</b> 5d10|rr:>8, roll 5 10-sided dice and, if any of the results is greater than 8, reroll that die and keep the new result.                    
                     <b>Rolling dice:</b> operator "d".

<b>Ex.:</b> 3d6, roll 3 6-sided dice.
<b>Ex.:</b> 2df, roll 2 fudge dice (-1, 0 and 1 possible results).
<b>Ex.:</b> It is possible to roll arbitrary dice like 1d7 or, 3d19.
                     About Poliedros Basic Mode. Clear Command Clear results Collapsed sidebar. Command Mode Command Mode. Command mode usage instructions Command usage instructions Diego C Sampaio GTK;Die;Dice;Roll;Random;Number; Go Back Minus Number No sidebar. Nothing Here Yet Plus Number Poliedros Poliedros is a multi-type dice roller. Basic mode allows you to make quick rolls using just the mouse, while Command mode allows for more complex rolls and combinations. Redo this roll Roll Roll multi-type dice. Roll some dice to begin Switch Mode Toggle History translator_credits Project-Id-Version: 
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2025-06-23 17:02-0300
Last-Translator: Diego C. Sampaio <kriptolix@gmail.com>
Language-Team: 
Language: pt_BR
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Generator: Poedit 3.6
 <b>Adições/Subtrações :</b> operadores "+" e "-".
                    
<b>Ex.:</b> 1d6 + 3, rola 1 dado de 6 faces e adiciona 3.
<b>Ex.:</b> 2d8 - 1d4, rola 2 dados de 8 faces e subtrai o resultado da rolagem de 1 dado de 4 faces.
                     <b>Contar:</b> operador "|cn:parâmetros".
                    
<b>Ex.:</b> 6d10|cn:6,8,10; rola 4 dados de 10 lados e conte quantos 6,8 e 10 saem.
<b>Ex.:</b> 4d4|cn:4; rola 4 dados de 4 faces e conte quantos 4 saem.
<b>Ex.:</b> 6d20|cn:>15; rola 6 dados de 20 faces e conte quantos resultados maiores que 15 saíram.
<b>Ex.:</b> 3d100|cn:80..90; rola 3 dados de 100 lados e conte quantos resultados entre 80 e 90 saíram.
                     <b>Explodindo dados:</b> operador "|ex:parâmetros". 
                   
<b>Ex.:</b> 6d6|ex:6, rola 6 dados de 6 faces e, se algum resultar num 6, rola esse dado novamente, adiciona o resultado e assim por diante.
<b>Ex.:</b> 5d10|ex:>8, rola 5 dados de 10 faces e, se algum dos resultados for maior que 8, rola esse dado novamente, adiciona o resultado e assim por diante.                    
                     <b>Parâmetros de função:</b>.

<b>Ex.:</b> >15: maior que um numero (inclusivo).
<b>Ex.:</b> 6,8,10: relação arbitraria de números.
<b>Ex.:</b> 4: um numero único.
<b>Ex.:</b> &lt;10: menor que um numero (inclusivo).
<b>Ex.:</b> 80..90: intervalo entre números (inclusive).
                     <b>Mantendo os maiores:</b> operador "|kh:number".
                    
<b>Ex.:</b> 3d6|kh:2, rola 3 dados de 6 faces e mantêm os 2 maiores.
<b>Ex.:</b> 2d20|kh:1, rola 2 dados de 20 faces mantêm o maior.                    
                     <b>Mantendo os menores:</b> operador "|kl:number".
                    
<b>Ex.:</b> 4d10|kl:2, rola 4 dados de 10 faces e mantêm os 2 menores.
<b>Ex.:</b> 3d6|kl:1, rola 3 dados de 6 faces e mantêm o menor.
                     <b>Funções aninhadas:</b> Você pode usar o resultado de uma função como entrada para outra função. 
                    
<b>Ex.:</b> 6d6|ex:6|cn:6, rola 6 dados de 6 faces e, se algum deles resultar num 6, role esse dado novamente e assim por diante.Então, conte quantos 6 saíram.
<b>Ex.:</b> 5d10|kh:1|cn:>8, rola 5 dados de 10 faces e mantenha o maior, então, verifica se o resultado é maior que 8.                   
                     <b>Rerolar dados:</b> operador "e". 
                    
<b>Ex.:</b> 6d6|rr:6, rola 6 dados de 6 faces e, se algum resultar num 6, rola esse dado novamente e fica com o novo resultado.
<b>Ex.:</b> 5d10|rr:>8, rola 5 dados de 10 faces e, se algum dos resultados for maior que 8, rola esse dado novamente e fica com o novo resultado.                    
                     <b>Rolando dados:</b> operador "d".

<b>Ex.:</b> 3d6, rola 3 dados de 6 lados.
<b>Ex.:</b> 2df, rola 2 dados fudge (-1, 0 e 1 como possíveis resultados).
<b>Ex.:</b> É possível rolar dados arbitrários como 1d7 ou, 3d19.
                     Sobre o Poliedros Modo Básico. Limpar Comando Limpar Resultados Barra leteral colapsada. Modo Comando Modo Comando. Instruções de uso do modo comando Instruções de uso do comando Diego C Sampaio GTK;Dado;Dados;Rolagem;Aleatório;Numero; Voltar Subtrair Numero Sem a barra lateral. Nada Aqui Ainda Adicionar Numero Poliedros Poliedros é um rolador de múltiplos tipos de dados. O modo Básico permite realizar rolagens rápidas utilizando apenas o mouse, enquanto o modo Comando permite rolagens e combinações mais complexas. Refazer essa rolagem Rolar Poliedros é um rolador de múltiplos tipos de dados. Role alguns dados para começar Alternar Modo Exibir/Ocultar Histórico Diego C. Sampaio 