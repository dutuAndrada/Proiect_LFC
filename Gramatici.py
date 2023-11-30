import random

class Grammar:
    def __init__(self, Vn: list, Vt: list, P: list):
        self.Vn: list = Vn
        self.Vt: list = Vt
        self.P: list = P
        self.S: str = 'S'
        self.generated_words: set = set()

    def citire(self):
        self.Vn: list = []
        self.Vt: list = []
        self.P: list = []
        numar_neterminale = int(input("Numarul de neterminale: "))
        for i in range(numar_neterminale):
            self.Vn.append(input("Neterminal: "))
        numar_terminale = int(input("Numarul de terminale: "))
        for i in range(numar_terminale):
            self.Vt.append(input("Terminal: "))
        numar_productii = int(input("Numarul de productii: "))
        for i in range(numar_productii):
            user_input = input("Introduceti pereche de tip cheie->valoare: ")
            key, value = user_input.split("->")
            self.P.append((key, value))

        self.generated_words: set = set()

    def citire_fisier(self, file_name: str):
        self.Vn: list = []
        self.Vt: list = []
        self.P: list = []
        f = open(file_name, "r")
        Vn_string: str = f.readline()
        Vn_string = Vn_string.replace("\n", "")
        self.Vn = Vn_string.split(" ")
        Vt_string: str = f.readline()
        Vt_string = Vt_string.replace("\n", "")
        self.Vt = Vt_string.split(" ")
        numar_productii = int(f.readline())
        for i in range(numar_productii):
            file_input = f.readline()
            file_input = file_input.replace("\n", "")
            key, value = file_input.split("->")
            self.P.append((key, value))

    def verificare(self):
        i: str
        for neterminal in self.Vn:
            #neterminal sa fie litera mare
            if neterminal.islower() == True:
                return False
            #neterminal sa nu fie si terminal
            if neterminal in self.Vt:
                return False

        for terminal in self.Vt:
            #terminal sa nu fie si neterminal
            if terminal in self.Vn:
                return False

        #simbolul de start sa fie neterminal
        if self.S not in self.Vn:
            return False

        ok = False
        for productie in self.P:
            ok2 = True
            #partea stanga a productiei sa aiba macar un neterminal
            for neterminal in self.Vn:
                if neterminal in productie[0]:
                    ok2 = True
            if ok2 == False:
                return False
            #partea stanga a productiei sa fie neterminalul de start
            if self.S == productie[0]:
                ok = True
        if ok == False:
            return False

        for productie in self.P:
            for litera in productie[0]:
                #fiecare litera din productie sa se afle in Vn sau Vt
                if litera not in self.Vn and litera not in self.Vt:
                    return False
            for litera in productie[1]:
                if litera not in self.Vn and litera not in self.Vt and productie[1] != 'lambda':
                    return False

        return True

    def is_regular(self):
        for productie in self.P:
            if len(productie[0]) != 1 or productie[0].isupper() == False:
                return False
            if len(productie[1]) > 2 or len(productie[1]) < 1:
                return False

            if len(productie[1]) == 1:
                if productie[1].islower() == False:
                    return False
            if len(productie[1]) == 2:
                if productie[1][0].islower == False or productie[1][1].isupper() == False:
                    return False

        return True


    def generare(self):
        cuvant: str = self.S
        print(f"{cuvant} -> ", end='')
        ok: bool = True
        while ok == True:
            optiuni_de_inlocuire = []
            optiune: tuple
            for optiune in self.P:
                if optiune[0] in cuvant or optiune[0] == cuvant:
                    optiuni_de_inlocuire.append(optiune)
            inlocuire_aleasa: tuple = random.choice(optiuni_de_inlocuire)
            if inlocuire_aleasa[1] == "lambda":
                cuvant = cuvant.replace(inlocuire_aleasa[0], '', 1)
            else:
                cuvant = cuvant.replace(inlocuire_aleasa[0], inlocuire_aleasa[1], 1)
            print(cuvant, end="")
            ok = False
            for i in self.P:
                if i[0] in cuvant:
                    ok = True
            if ok == True:
                print(" -> ", end="")
            if ok == False:
                self.generated_words.add(cuvant)
        print()

    def afisare(self):
        print("Neterminale: ", self.Vn)
        print("Terminale: ", self.Vt)
        print("Productii: ", self.P)
        print("Start: ", self.S)

class FiniteAutomaton:
    def __init__(self, Q: list, E: list, q0: str, F: list, delta: list):
        self.Q: list = Q
        self.E: list = E
        self.q0: str = q0
        self.F: list = F
        self.delta: list = delta

    def citire(self):


def main():
    grammar = Grammar([], [], [])
    grammar.citire_fisier('gram.txt')
    print(grammar.verificare())
    grammar.generare()
    grammar.afisare()

main()