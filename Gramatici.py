﻿import random
from stat import FILE_ATTRIBUTE_NOT_CONTENT_INDEXED

class Grammar:
    def __init__(self, Vn: list, Vt: list, P: list):
        self.Vn: list = Vn
        self.Vt: list = Vt
        self.P: list = P
        self.S: str = 'S'
        self.generated_words: set = set()

    def ReadGrammar(self):
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

    def ReadGrammarFile(self, file_name: str):
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

    def VerifyGrammar(self):
        i: str
        for neterminal in self.Vn:
            if neterminal.islower() == True:
                return False
            if neterminal in self.Vt:
                return False

        for terminal in self.Vt:
            if terminal in self.Vn:
                return False

        if self.S not in self.Vn:
            return False

        ok = False
        for productie in self.P:
            ok2 = True
            for neterminal in self.Vn:
                if neterminal in productie[0]:
                    ok2 = True
            if ok2 == False:
                return False
            if self.S == productie[0]:
                ok = True
        if ok == False:
            return False

        for productie in self.P:
            for litera in productie[0]:
                if litera not in self.Vn and litera not in self.Vt:
                    return False
            for litera in productie[1]:
                if litera not in self.Vn and litera not in self.Vt and productie[1] != 'lambda':
                    return False

        return True

    def IsRegular(self):
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


    def GenerateWord(self):
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

    def TransformAutomata(self):
        automata: FiniteAutomaton = FiniteAutomaton([], [], '', [], [])
        if self.IsRegular() == False:
            print("Gramatica nu este corecta")
            return automata
        else:
            automata.Q = self.Vn
            automata.E = self.Vt
            automata.q0 = self.S
            for productie in self.P:
                if len(productie[1]) == 2:
                    automata.delta.append((productie[0], productie[1][0], productie[1][1]))
                else:
                    stare_finala:str = chr(ord(automata.Q[len(automata.Q) - 1]) + 1)
                    automata.delta.append((productie[0], productie[1], stare_finala))
                    automata.Q.append(stare_finala)
                    automata.F.append(stare_finala)
            return automata


    def PrintGrammar(self):
        print("Neterminale: ", self.Vn)
        print("Terminale: ", self.Vt)
        print("Productii: ", self.P)
        print("Start: ", self.S)

class FiniteAutomaton:
    def __init__(self, Q: list[str], E: list[str], q0: str, F: list[str], delta: list[tuple[str]]):
        self.Q: list[str] = Q
        self.E: list[str] = E
        self.q0: str = q0
        self.F: list[str] = F
        self.delta: list[tuple[str]] = delta

    def ReadAutomaton(self):
        self.Q: list[str] = []
        self.E: list[str] = []
        self.F: list[str] = []
        self.delta: list[tuple[str]] = []
        numar_stari = int(input("Numarul de stari: "))
        for i in range(numar_stari):
            self.Q.append(input("Stare: "))
        numar_litere = int(input("Numarul de litere: "))
        for i in range(numar_litere):
            self.E.append(input("Litera: "))
        self.q0 = input("Starea initiala: ")
        numar_stari_finale = int(input("Numarul de stari finale: "))
        for i in range(numar_stari_finale):
            self.F.append(input("Stare finala: "))
        numar_tranzitii = int(input("Numarul de tranzitii: "))
        for i in range(numar_tranzitii):
            user_input = input("Introduceti tranzitia: ")
            stare1, aux = user_input.split(",")
            litera, stare2 = aux.split("->")
            self.delta.append((stare1, litera, stare2))

    def ReadAutomatonFile(self, file_name: str):
        self.Q: list[str] = []
        self.E: list[str] = []
        self.F: list[str] = []
        self.delta: list[tuple[str]] = []
        f = open(file_name, "r")
        Q_string: str = f.readline()
        Q_string = Q_string.replace("\n", "")
        self.Q = Q_string.split(" ")
        E_string: str = f.readline()
        E_string = E_string.replace("\n", "")
        self.E = E_string.split(" ")
        self.q0 = f.readline()
        self.q0 = self.q0.replace("\n", "")
        F_string: str = f.readline()
        F_string = F_string.replace("\n", "")
        self.F = F_string.split(" ")
        numar_tranzitii = int(f.readline())
        for i in range(numar_tranzitii):
            file_input = f.readline()
            file_input = file_input.replace("\n", "")
            stare1, aux = file_input.split(",")
            litera, stare2 = aux.split("->")
            self.delta.append((stare1, litera, stare2))

    def verifyAutomaton(self):
        if self.q0 not in self.Q:
            return False
        for state in self.F:
            if state not in self.Q:
                return False
        for transition in self.delta:
            if transition[0] not in self.Q:
                return False
            if transition[1] not in self.E:
                return False
            if len(transition) > 2:
                for finalState in range (2, len(transition)):
                    if transition[finalState] not in self.Q:
                        return False
        return True
    def checkWord(self, word):
        currentState = self.q0
        for letter in word:
            foundTransition = False
            for transition in self.delta:
                if transition[0] == currentState and transition[1] == letter:
                    currentState = transition[2]
                    foundTransition = True
                    break
            if not foundTransition:
                return False  
        return currentState in self.F
    
    def IsDeterministic(self):
        existingTransitions: list = []
        for transition in self.delta:
            aux: tuple = (transition[0],transition[1])
            if aux in existingTransitions:
                return False
            existingTransitions.append(aux)
        return True

    
    def printAutomaton(self):
        print(self.Q)
        print(self.E)
        print(self.q0)
        print(self.F)
        print(self.delta)

def main():
    grammar = Grammar([], [], [])
    grammar.ReadGrammarFile('gram.txt')

    if not grammar.VerifyGrammar() or not grammar.IsRegular():
        print("Gramatica nu este corecta sau nu este regulata.")
        return

    print("Gramatica este corecta si regulata.")

    while True:
        print("\nMeniu:")
        print("a. Afișarea gramaticii G")
        print("b. Generare a n cuvinte în gramatica G")
        print("c. Obținere automat echivalent cu G")
        print("d. Verificare dacă un cuvânt este acceptat de automat")
        print("e. Generare și verificare cuvânt în G")
        print("x. Ieșire")

        optiune = input("Alegeți o opțiune: ")

        if optiune == 'a':
            grammar.PrintGrammar()

        elif optiune == 'b':
            numar_cuvinte = int(input("Introduceți numărul de cuvinte: "))
            for i in range(numar_cuvinte):
                grammar.GenerateWord()

        elif optiune == 'c':
            automaton = grammar.TransformAutomata()
            automaton.printAutomaton()

        elif optiune == 'd':
            word = input("Introduceți cuvântul de verificat: ")
            automaton = grammar.TransformAutomata()
            if automaton.verifyAutomaton():
                if automaton.IsDeterministic():
                    if automaton.checkWord(word):
                        print(f"Cuvântul '{word}' este acceptat de automat.")
                    else:
                        print(f"Cuvântul '{word}' nu este acceptat de automat.")
                else:
                    print("Automatul nu este determinist.")
            else:
                print("Automatul nu este valid.")

        elif optiune == 'e':
            generated_word = grammar.GenerateWord()
            word = input("Introduceți cuvântul de verificat: ")
            automaton = grammar.TransformAutomata()
            if automaton.verifyAutomaton():
                if automaton.IsDeterministic():
                    if automaton.checkWord(word):
                        print(f"Cuvântul '{word}' este acceptat de automat.")
                    else:
                        print(f"Cuvântul '{word}' nu este acceptat de automat.")
                else:
                    print("Automatul nu este determinist.")
            else:
                print("Automatul nu este valid.")

        elif optiune == 'x':
            break

        else:
            print("Opțiune invalidă. Reîncercați.")

    
  
main()