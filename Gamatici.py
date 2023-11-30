import random

class Grammar:
    Vn: list
    Vt: list
    S: str
    P: list
    cuvinte_generate: set

    def __init__(self, Vn: list, Vt: list, P: list):
        self.Vn = Vn
        self.Vt = Vt
        self.S = 'S'
        self.P = P
        self.cuvinte_generate = set()
        
    def inlocuire_lambda(self):
        for i in range(len(self.P)):
            temporary_tuple: tuple = self.P[i]
            if temporary_tuple[1] == "lambda":
                temporary_list = list(temporary_tuple)
                temporary_list[1] = ""
                self.P[i] = tuple(temporary_list)
                

    def citire():
        numar_elemente_Vn: int = int(input("Cate elemente are Vn? "))
        Vn_temporar: list = [input(f"Introduceti elementul numarul {i} din Vn: ") for i in range(numar_elemente_Vn)]
    
        numar_elemente_Vt: int = int(input("Cate elemente are Vt? "))
        Vt_temporar: list = [input(f"Introduceti elementul numarul {i} din Vt: ") for i in range(numar_elemente_Vt)]

        numar_productii: int = int(input("Cate productii vor fi? "))
        P_temporar = []
        for i in range(numar_productii):
            user_input = input("Introduceti pereche de tip cheie->valoare: ")
            key,value = user_input.split("->")
            P_temporar.append[(key, value)]
            
        for i in range(len(P_temporar)):
            temporary_tuple: tuple = P_temporar[i]
            if temporary_tuple[1] == "lambda":
                temporary_list = list(temporary_tuple)
                temporary_list[1] = ""
                P_temporar[i] = tuple(temporary_list)

        gramatica: Grammar = Grammar(Vn_temporar, Vt_temporar, P_temporar)

        return gramatica

    def citire_din_fisier(calea):
        f = open(calea, "r")
        Vn_string:str = f.readline()
        Vn_string = Vn_string.replace("\n","")
        Vn_temporar: list = Vn_string.split()
        Vt_string:str = f.readline()
        Vt_string = Vt_string.replace("\n","")
        Vt_temporar: list = Vt_string.split()
        numar_productii = int(f.readline())
        P_temporar = []
        for i in range(numar_productii):
            file_input:str = f.readline()
            file_input = file_input.replace("\n","")
            key,value = file_input.split("->")
            P_temporar.append((key, value))
            
        for i in range(len(P_temporar)):
            temporary_tuple: tuple = P_temporar[i]
            if temporary_tuple[1] == "lambda":
                temporary_list = list(temporary_tuple)
                temporary_list[1] = ""
                P_temporar[i] = tuple(temporary_list)
                
        gramatica: Grammar = Grammar(Vn_temporar, Vt_temporar, P_temporar)
        return gramatica


    def verificare(self):
        i:str
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
                if litera not in self.Vn and litera not in self.Vt:
                    return False
        
        return True
    
    def is_regular(self):
        for productie in self.P:
            if len(productie[0]) != 1 or productie[0].isupper() == False:
                return False
            if len(productie[1])>2 or len(productie[1])<1:
                return False
            
            if len(productie[1])==1:
                if productie[1].islower()==False:
                    return False
            if len(productie[1])==2:
                if productie[1][0].islower == False or productie[1][1].isupper() == False:
                    return False
                
        return True
            
        print()
        
    def generare(self):
        cuvant: str = self.S
        print(f"{cuvant} -> ", end = '')
        ok: bool = True
        while ok == True:
            optiuni = []
            optiune: tuple
            for optiune in self.P:
                if optiune[0] in cuvant or optiune[0] == cuvant:
                    optiuni.append(optiune)
            inlocuire:tuple = random.choice(optiuni)
            cuvant = cuvant.replace(inlocuire[0], inlocuire[1], 1)
            print(cuvant, end = "")
            ok = False
            for i in self.P:
                if i[0] in cuvant:
                    ok = True
            if ok == True:
                print(" -> ", end = "")
            if ok == False:
                self.cuvinte_generate.add(cuvant)
                
    def automat():
        print()
                
    def afisare(self):
        print(f"multimea neterminalelor: {self.Vn}")
        print(f"multimea terminalelor: {self.Vt}")
        print(f"simbolul de start: {self.S}")
        print("Productii:")
        for i in self.P:
            print(f"{i[0]} -> {i[1]}")
            
class FiniteAutomaton:
    a:str

def main():
    gramatica2: Grammar = Grammar(["S","B","C"],["a","b","c"],[("S", "aS"),
                                                       ("S", "aA"),
                                                       ("S", "aA"),
                                                       ("A", "b"),
                                                       ("A", "lambda")])
    #gramatica2.inlocuire_lambda()
    
    gramatica: Grammar = Grammar.citire_din_fisier("C:\\OTHER\\temporar.txt")

    gramatica.afisare()
    print(gramatica2.is_regular())
    print (gramatica.verificare())
    numar_cuvinte:int = int(input("Introduceti numarul de cuvinte dorite: "))
    for i in range(numar_cuvinte):
        print()
        gramatica.generare()

    print()    
    #print(gramatica.cuvinte_generate)
    print()
    
main()



