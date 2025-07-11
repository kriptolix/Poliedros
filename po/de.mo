��    #      4  /   L        �   	  �    {  �  #  C  �   g  �   W	  �  0
  f  �  �   N     5     E     Q     _     m     �     �     �     �     �      �                    (     9  	   E  �   O     �               #     ;     G     V    i  '  �  �  �  �  �  '  r  (  �    �    �  �  �  '  �     �     �     �     �     �          #     1     M     i  L   y     �  
   �     �     �  	      	      �         �      !  "   !  +   A!     m!     |!  &   �!                                                     #                                                                     
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
PO-Revision-Date: 2025-06-23 22:18+0200
Last-Translator: Philipp Kiemle <l10n@prly.mozmail.com>
Language-Team: 
Language: de
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Generator: Poedit 3.6
 <b>Addition/Subtraktion:</b> Befehle »+« und »-«.
                    
<b>Befehle:</b> 1d6 + 3, würfelt 1 6-seitigen Würfel und addiert die Zahl 3.
<b>Befehle:</b> 2d8 - 1d4, würfelt 2 8-seitige Würfel und subtrahiert das Ergebnis des Wurfs von 1 4-seitigem Würfel.
                     <b>Würfel zählen:</b> Befehl »|cn:parameter«.
                    
<b>Beispiel:</b> 6d10|cn:6,8,10, würfelt 4 10-seitige Würfel und zählt alle 6er, 8er und 10er vorkommen.
<b>Beispiel:</b> 4d4|cn:4, würfelt 4 4-seitige Würfel und zählt alle 4er.
<b>Beispiel:</b> 6d20|cn:>15, würfelt 6 20-seitige Würfel und zählt alle Würfel über 15.
<b>Beispiel:</b> 3d100|cn:80..90, würfelt 3 100-seitige Würfel und zählt alle Ergebnisse zwischen 80 und 90.
                     <b>Explodierende Würfel:</b> Befehl »|ex:parameter«.
                    
<b>Beispiel:</b> 6d6|ex:6, würfelt 6 6-seitige Würfel und jeden Würfel, der eine 6 zeigt, erneut. Dies passiert wieder, wenn erneut eine 6 gewürfelt wird – unendlich lang.
<b>Beispiel:</b> 5d10|ex:>8, würfelt 5 10-seitige Würfel und jeden Würfel, der eine 10 zeigt, erneut. Wenn das neue Ergebnis auch 10 ist, wird der Würfel aber nicht erneut geworfen.                    
                     <b>Funktionsparameter:</b>
<b>Beispiel:</b> >15: Größer als Zahl (inklusiv).
<b>Beispiel:</b> 6,8,10: Eine Reihe an Zahlen.
<b>Beispiel:</b> 4: Eine einfache Zahl.
<b>Beispiel:</b> &lt;10: Niedriger als Zahl (inklusiv).
<b>Beispiel:</b> 80..90: Zahlenintervall (inklusiv).
                     <b>Höhere behalten:</b> Befehl »|kh:zahl«.
                    
<b>Beispiel:</b> 3d6|kh:2, würfelt 3 6-seitige Würfel und behält die 2 höchsten Ergebnisse.
<b>Beispiel:</b> 2d20|kh:1, würfelt 2 20-seitige Würfel und behält das höchste Ergebnis.                    
                     <b>Niedrigere behalten:</b> Befehl »|kl:zahl«.
                    
<b>Beispiel:</b> 4d10|kl:2, würfelt 4 10-seitige Würfel und behält die 2 niedrigsten Ergebnisse.
<b>Beispiel:</b> 3d6|kl:1, würfelt 3 6-seitige Würfel und behält das niedrigste Ergebnis.
                     <b>Verschachtelte Funktionen:</b> Sie können das Ergebnis einer Funktion als Eingabe für eine andere Funktion verwenden.
                    
<b>Beispiel:</b> 6d6|ex:6|cn:6, würfelt 6 6-seitige Würfel und jeden Würfel, der eine 6 zeigt, erneut - so lange, bis keine 6 mehr gewürfelt wird. Dann wird die Anzahl 6er gezählt.
<b>Beispiel:</b> 5d10|kh:1|cn:>8, würfelt 5 10-seitige Würfel und behält den höchsten. Dann wird überprüft, ob dieser Wurf höher als 8 ist.                    
                     <b>Erneut würfeln:</b> Befehl »|rr:parameter«.
                    
<b>Beispiel:</b> 6d6|rr:6, würfelt 6 6-seitige Würfel. Jeder Würfel, der eine 6 zeigt, wird erneut gewürfelt und das neue Ergebnis wird behalten.
<b>Beispiel:</b> 5d10|rr:>8, würfelt 5 10-seitige Würfel. Jeder Würfel, der eine 8 oder höher zeigt, wird erneut gewürfelt und das neue Ergebnis wird behalten.                    
                     <b>Würfel würfeln:</b> Befehl »d«.

<b>Beispiel:</b> 3d6, würfelt 3 6-seitige Würfel.
<b>Beispiel:</b> 2df, würfelt 2 Fudge-Würfel (-1, 0 und +1 sind mögliche Ergebnisse).
<b>Beispiel:</b> Es ist möglich, unkonventionelle Würfel zu würfeln, z. B. 1d7 oder 3d19.
                     Info zu Poliedros Einfacher Modus. Befehl leeren Ergebnisse leeren Eingeklappte Seitenleiste. Befehlsmodus Befehlsmodus. Verwendung des Befehlsmodus Verwendung des Befehlsmodus Diego C Sampaio GTK;Die;Dice;Roll;Random;Number;Würfel;würfeln;Wurf;Zufall;zufällig;Zahl; Zurückgehen Minus Zahl Keine Seitenleiste. Hier ist noch nichts Plus Zahl Poliedros Poliedros simuliert das Würfeln verschiedener Würfel. Der einfache Modus ermöglicht es, schnelle Würfe mit der Maus durchzuführen - der Befehlsmodus hingegen ist gut geeignet für kompliziertere Würfe und Kombinationen. Diesen Wurf wiederholen Würfeln Würfeln Sie verschiedene Würfel. Würfeln Sie einige Würfel, um zu beginnen Modus wechseln Chronik umschalten Philipp Kiemle <l10n@prly.mozmail.com> 