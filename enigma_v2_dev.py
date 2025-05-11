# -*- coding: utf-8 -*-

class Rotor:
    """ classe décrivant les rotors et leurs utilisation """
    def __init__(self,filtre="ABCDEFGHIJKLMNOPQRSTUVWXYZ",sortie="ABCDEFGHIJKLMNOPQRSTUVWXYZ",rang=0):
        self.filtre = filtre
        self.sortie = sortie
    def transcript(self,stringin,angle=0):
        """ methode de transcription aller """
        return self.sortie[((self.filtre.find(stringin))+angle)%26]    
    def reverse(self,stringin,angle=0):
        """ methode de transcritpion retour """
        return self.filtre[((self.sortie.find(stringin))+angle)%26]
class Câblage:
    """ classe décrivant les câblages et leur utilisation """
    def __init__(self,sig1="",sig2=""):
        self.sig1 = sig1
        self.sig2 = sig2    
    def cable(self,stringin):
        """ methode de test et de transcription par le cablage (reversible) """
        if stringin == self.sig1:
            return self.sig2
        if stringin == self.sig2:
            return self.sig1
        else:
            return stringin            
def traitement_in(message,stringout=""):
    """ traitement du message d'entrée pour le rendre transcriptible (passage en capitales et retrait de tous les caractères non alphabétiques) """
    message = message.upper()
    for a in message:
        if "ABCDEFGHIJKLMNOPQRSTUVWXYZ".find(a) != -1:
            stringout += a
    return stringout    
def traitement_out(message,stringout=""):
    """ traitement de sortie du message (sequençage en chaines de quatre caractères), inutile d'un point de vue du message, ne fait que reproduire une caractéristique historique """
    return ' '.join([message[i:i+4] for i in range(0, len(message), 4)])
def enigma(message,r1=0,r2=0,r3=0,F1="ABCDEFGHIJKLMNOPQRSTUVWXYZ",S1="EKMFLGDQVZNTOWYHXUSPAIBRCJ",F2="ABCDEFGHIJKLMNOPQRSTUVWXYZ",S2="AJDKSIRUXBLHWTMCQGZNPYFVOE",F3="ABCDEFGHIJKLMNOPQRSTUVWXYZ",S3="ZYXWVUTSRQPONMLKJIHGFEDCBA",FR="ABCDEFGHIJKLMNOPQRSTUVWXYZ",SR="ZYXWVUTSRQPONMLKJIHGFEDCBA",C1a="A",C1b="X",C2a="Y",C2b="J",C3a="Q",C3b="F"):
    """ fonction de traitement d'entrée, transcription, et traitement de sortie """
    messageout = ""
    R1 = Rotor(F1,S1)
    R2 = Rotor(F2,S2)
    R3 = Rotor(F3,S3)
    RF = Rotor(FR,SR)
    C1 = Câblage(C1a,C1b)
    C2 = Câblage(C2a,C2b)
    C3 = Câblage(C3a,C3b)
    message = traitement_in(message)
    for a in message:
        # print("debug info : configuration, r1 = {0}, r2 = {1}, r3 = {2}".format(r1,r2,r3))
        messageout += C1.cable(C2.cable(C3.cable(R1.reverse(R2.reverse(R3.reverse(RF.transcript(R3.transcript(R2.transcript(R1.transcript(C3.cable(C2.cable(C1.cable(a))),r1),r2),r3)),-r3),-r2),-r1))))
        # print("full debug trace : cable 1 = {0}, cable 2 = {1}, cable 3 = {2}, rotor 1 = {3}, rotor 2 = {4}, rotor 3 = {5}, reflecteur = {6}, rotor 3 = {7}000000, rotor 2 = {8}, rotor 1 = {9}, cable 3 = {10}, cable 2 = {11}, cable 1 = {12}".format(C1.cable(traitement_in(a)),C2.cable(C1.cable(traitement_in(a))),C3.cable(C2.cable(C1.cable(traitement_in(a)))),R1.transcript(C3.cable(C2.cable(C1.cable(traitement_in(a)))),r1),R2.transcript(R1.transcript(C3.cable(C2.cable(C1.cable(traitement_in(a)))),r1),r2),R3.transcript(R2.transcript(R1.transcript(C3.cable(C2.cable(C1.cable(traitement_in(a)))),r1),r2),r3),RF.transcript(R3.transcript(R2.transcript(R1.transcript(C3.cable(C2.cable(C1.cable(traitement_in(a)))),r1),r2),r3)),R3.reverse(RF.transcript(R3.transcript(R2.transcript(R1.transcript(C3.cable(C2.cable(C1.cable(traitement_in(a)))),r1),r2),r3)),-r3),R2.reverse(R3.reverse(RF.transcript(R3.transcript(R2.transcript(R1.transcript(C3.cable(C2.cable(C1.cable(traitement_in(a)))),r1),r2),r3)),-r3),-r2),R1.reverse(R2.reverse(R3.reverse(RF.transcript(R3.transcript(R2.transcript(R1.transcript(C3.cable(C2.cable(C1.cable(traitement_in(a)))),r1),r2),r3)),-r3),-r2),-r1),C3.cable(R1.reverse(R2.reverse(R3.reverse(RF.transcript(R3.transcript(R2.transcript(R1.transcript(C3.cable(C2.cable(C1.cable(traitement_in(a)))),r1),r2),r3)),-r3),-r2),-r1)),C2.cable(C3.cable(R1.reverse(R2.reverse(R3.reverse(RF.transcript(R3.transcript(R2.transcript(R1.transcript(C3.cable(C2.cable(C1.cable(traitement_in(a)))),r1),r2),r3)),-r3),-r2),-r1))),C1.cable(C2.cable(C3.cable(R1.reverse(R2.reverse(R3.reverse(RF.transcript(R3.transcript(R2.transcript(R1.transcript(C3.cable(C2.cable(C1.cable(traitement_in(a)))),r1),r2),r3)),-r3),-r2),-r1))))))
        r1 += 1
        if r1 % 26 == 0:
            r2 += 1
            if r2 % 26 == 0:
                r3 += 1
    return traitement_out(messageout)    
def interface_utilisateur(check=True):
    """ fonction d'interface utilisateur """
    print("Bienvenue dans enigma_v2\n")    
    while check == True:
        print("voulez vous paramettrer les rotors ? (O/N) ")
        question = str(input())        
        if question == "O":
            print("index rotor 1 ?")
            iR1 = str(input)
            print("sortie rotor 1 ?")
            sR1 = str(input)
            print("index rotor 2 ?")
            iR2 = str(input)
            print("sortie rotor 2 ?")
            sR2 = str(input)
            print("index rotor 3 ?")
            iR3 = str(input)
            print("sortie rotor 3 ?")
            sR3 = str(input)
            print("index reflecteur ?")
            iRF = str(input)
            print("sortie reflecteur ?")
            sRF = str(input)            
        else:
            iRF = iR3 = iR2 = iR1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            sR1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
            sR2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
            sR3 = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
            sRF = "ZYXWVUTSRQPONMLKJIHGFEDCBA"
        print("debug",iR1,sR1,iR2,sR2,iR3,sR3,iRF,sRF,"\n")
        print("voulez vous paramettrer les cablages ?")
        question = str(input())
        if question == "O":
            print("Câble 1 port A ?")
            c1a = str(input)
            print("Câble 1 port B ?")
            c1b = str(input)
            print("Câble 2 port A ?")
            c2a = str(input)
            print("Câble 2 port B ?")
            c2b = str(input)
            print("Câble 3 port A ?")
            c3a = str(input)
            print("Câble 3 port B ?")
            c3b = str(input)            
        else:
            c1a = "A"
            c1b = "X"
            c2a = "Y"
            c2b = "J"
            c3a = "Q"
            c3b = "F"
        print("debug",c1a,c1b,c2a,c2b,c3a,c3b,"\n")
        print("Voulez vous paramettrer les crans de départ des rotors ?")
        question = str(input())
        if question == "O":
            print("Cran du rotor 1 ?")
            cr1 = str(input)
            print("Cran du rotor 2 ?")
            cr2 = str(input)
            print("Cran du rotor 3 ?")
            cr3 = str(input)
        else :
            cr1 = cr2 = cr3 = 0
        print("debug", cr1, cr2, cr3, "\n")
        print("Entrez votre message\n")
        message = str(input())
        print("lancez la transcription\n")
        input()
        print(enigma(message,cr1,cr2,cr3,iR1,sR1,iR2,sR2,iR3,sR3,iRF,sRF,c1a,c1b,c2a,c2b,c3a,c3b))
        check = False
        print("Transcription terminée !")
        input()
interface_utilisateur()

#       Données supplémentaires : 
#       Rotors d'origine connus:
# I:     EKMFLGDQVZNTOWYHXUSPAIBRCJ
# II:    AJDKSIRUXBLHWTMCQGZNPYFVOE
# III:   BDFHJLCPRTXVZNYEIWGAKMUSQO
# IV:    ESOVPZJAYQUIRHXLNFTGKDCMWB
# V:     VZBRGITYUPSDNHLXAWMJQOFECK
# VI:    JPGVOUMFYQBENHZRDKASXLICTW
# VII:   NZJHGRCXMYSWBOUFAIVLPEKQDT
# VIII:  FKQHTLXOCBJSPDZRAMEWNIUYGV
 
#       Reflecteurs d'origine connus :
# beta:  LEYJVCNIXWPBQMDRTAKZGFUHOS
# Gamma: FSOKANUERHMBTIYCWLQPZXVGJD
# A:     EJMZALYXVBWFCRQUONTSPIKHGD
# B:     YRUHQSLDPXNGOKMIEBFZCWVJAT
# C:     FVPJIAOYEDRZXWGCTKUQSBNMHL
# B fin: ENKQAUYWJICOPBLMDXZVFTHRGS
# C fin: RDOBJNTKVEHMLFCWZAXGYIPSUQ
# ETW:   ABCDEFGHIJKLMNOPQRSTUVWXYZ

#       Les filtes et sorties peuvent être modifiés tant qu'ils comportent chacun une seule occurence de chaque lettre.


223A5187B5C