import random


def roll_dice():

    roll = []

    for _ in range(2):
        roll.append(random.randint(1, 12))

    return roll


class Ameaça:
    def __init__(self, nome, controle=0, agravante=0, atenuante=0):
        self.nome = nome
        self.controle_stadard = controle
        self.controle_superior = self.controle_stadard + 4
        self.agravante_stadard = agravante
        self.agravante_superior = self.agravante_stadard + 4
        self.atenuante_stadard = atenuante
        self.atenuante_superior = self.atenuante_stadard + 4

        self.incapacitado = False
        self.efeitos_marcados = set()  # Para rastrear efeitos sofridos

    def aplicar_efeito(self, intensidade):        

        # print(f"{self.nome} sofreu {intensidade}")

        if intensidade == "Parcial":
            if "Atordoado" in self.efeitos_marcados:
                self.aplicar_efeito("Moderado")
            else:
                self.efeitos_marcados.add("Atordoado")
                print(f"{self.nome} está Atordoado")  

        elif intensidade == "Moderado":
            self.limpa_parcial()
            efeitos_moderados = ["Desajeitado", "Lento", "Fraco", "Vulnerável"]
            for efeito in efeitos_moderados:
                if efeito not in self.efeitos_marcados:
                    self.efeitos_marcados.add(efeito)
                    self.aplicar_consequencia(efeito)
                    break
            if all(e in self.efeitos_marcados for e in efeitos_moderados):
                self.aplicar_efeito("Intenso")

        elif intensidade == "Intenso":
            self.limpa_parcial()
            efeitos_intensos = ["Mutilado", "Estraçalhado"]
            for efeito in efeitos_intensos:
                if efeito not in self.efeitos_marcados:
                    self.efeitos_marcados.add(efeito)
                    if efeito == "Estraçalhado":
                        self.incapacitado = True
                        print(f"{self.nome} está incapacitado!")
                    break

    def aplicar_consequencia(self, efeito):
        if efeito == "Lento":
            # self.controle = self.controle - 1
            print(f"{self.nome} está {efeito}")
        elif efeito == "Desajeitado":
            print(f"{self.nome} está {efeito}")
            pass
        elif efeito == "Fraco":
            # self.agravante = self.agravante - 1
            print(f"{self.nome} está {efeito}")
        elif efeito == "Vulnerável":
            print(f"{self.nome} está {efeito}")
            # self.atenuante = self.atenuante - 1

    def limpa_parcial(self):

        if "Atordoado" in self.efeitos_marcados:             
            self.efeitos_marcados.remove("Atordoado")

    def __str__(self):

        stats = (f"Personagem {self.nome}: "
                 f"Controle={self.controle_stadard}, "
                 f"Agravante={self.agravante_stadard}, "
                 f"Atenuante={self.atenuante_stadard}, "
                 f"Controle={self.controle_superior}, "
                 f"Agravante={self.agravante_superior}, "
                 f"Atenuante={self.atenuante_superior}, "
                 f"Incapacitado={self.incapacitado}")

        return stats


class Personagem:
    def __init__(self, nome, controle=0, agravante=0, atenuante=0):
        self.nome = nome
        self.controle = controle
        self.agravante = agravante
        self.atenuante = atenuante
        self.incapacitado = False
        self.efeitos_marcados = set()  # Para rastrear efeitos sofridos

    def aplicar_efeito(self, intensidade):        

        if self.incapacitado:
            print(f"{self.nome} já está incapacitado!")
            return

        # print(f"{self.nome} sofreu {intensidade}")

        if intensidade == "Parcial":
            if "Atordoado" in self.efeitos_marcados:
                self.aplicar_efeito("Moderado")
            else:
                self.efeitos_marcados.add("Atordoado")
                print(f"{self.nome} está Atordoado")        
        
        elif intensidade == "Moderado":
            self.limpa_parcial()

            efeitos_moderados = ["Desajeitado", "Lento", "Fraco", "Vulnerável"]
            for efeito in efeitos_moderados:
                if efeito not in self.efeitos_marcados:
                    self.efeitos_marcados.add(efeito)
                    self.aplicar_consequencia(efeito)
                    break
            if all(e in self.efeitos_marcados for e in efeitos_moderados):
                self.aplicar_efeito("Intenso")

        elif intensidade == "Intenso":
            self.limpa_parcial()

            efeitos_intensos = ["Mutilado", "Estraçalhado"]
            for efeito in efeitos_intensos:
                if efeito not in self.efeitos_marcados:
                    self.efeitos_marcados.add(efeito)
                    if efeito == "Estraçalhado":
                        self.incapacitado = True
                        print(f"{self.nome} está incapacitado!")
                    break

    def aplicar_consequencia(self, efeito):
        if efeito == "Lento":
            # self.controle = self.controle - 1
            print(f"{self.nome} está {efeito}")
        elif efeito == "Desajeitado":
            print(f"{self.nome} está {efeito}")
            pass
        elif efeito == "Fraco":
            # self.agravante = self.agravante - 1
            print(f"{self.nome} está {efeito}")
        elif efeito == "Vulnerável":
            print(f"{self.nome} está {efeito}")
            # self.atenuante = self.atenuante - 1

    def limpa_parcial(self):

        if "Atordoado" in self.efeitos_marcados:             
            self.efeitos_marcados.remove("Atordoado")

    def __str__(self):

        stats = (f"Personagem {self.nome}: "
                 f"Controle={self.controle}, "
                 f"Agravante={self.agravante}, "
                 f"Atenuante={self.atenuante}, "
                 f"Incapacitado={self.incapacitado}")

        return stats


def evaluate_limit(operation, dice, fighter, treat):

    match operation:

        case "controle":
            first_return = 3
            second_return = 2
            third_return = 1

            modifier = fighter.controle
            stadard = treat.controle_stadard
            superior = treat.controle_superior

            roll = dice[0] + modifier

        case "agravante":
            first_return = 3
            second_return = 2
            third_return = 1

            modifier = fighter.agravante
            stadard = treat.agravante_stadard
            superior = treat.agravante_superior

            roll = dice[1] + modifier

        case "atenuante":
            first_return = 1
            second_return = 2
            third_return = 3

            modifier = fighter.atenuante
            stadard = treat.atenuante_stadard
            superior = treat.atenuante_superior

            roll = dice[1] + modifier

    #print(f"{operation}, dados: {dice} modificador: {modifier}, total = {roll}")

    if roll >= stadard:

        if roll >= superior:

            #print(f"{operation}, Superior, retonou: {first_return}")

            return first_return

        #print(f"{operation}, Standard, retonou: {second_return}")
        return second_return

    #print(f"{operation}, Inferior, retonou: {third_return}")
    return third_return


def check_turn(combatente, ameaça):

    pool = roll_dice()
    controll = evaluate_limit("controle", pool, combatente, ameaça)

    print(pool)

    if controll >= 2:

        if controll == 2:
            combatente.aplicar_efeito("Parcial")

        potence = evaluate_limit("agravante", pool, combatente, ameaça)

        combatente.limpa_parcial()

        if potence == 3:
            ameaça.aplicar_efeito("Intenso")
        if potence == 2:
            ameaça.aplicar_efeito("Moderado")
        if potence == 1:
            ameaça.aplicar_efeito("Parcial")

    if controll == 1:

        potence = evaluate_limit("atenuante", pool, combatente, ameaça)

        ameaça.limpa_parcial()

        if potence == 3:
            combatente.aplicar_efeito("Intenso")

        if potence == 2:
            combatente.aplicar_efeito("Moderado")

        if potence == 1:
            combatente.aplicar_efeito("Parcial")

    if combatente.incapacitado:
        return [True, ameaça]
    
    if ameaça.incapacitado:
        return [True, combatente]
    
    return [False, None]


def test():

    rounds = 0
    combatente = Personagem("Fighter", 2, 2, 2)
    ameaça = Ameaça("goblin", 7, 7, 7)

    for _ in range(50):
        rounds = rounds + 1
        ended, winner = check_turn(combatente, ameaça)

        if ended:
            print(f"{winner.nome} venceu! rouds: {rounds}")
            print(winner.efeitos_marcados)
            break


test()
