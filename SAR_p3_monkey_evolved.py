#!/usr/bin/env python
#! -*- encoding: utf8 -*-

"""
3.- Monkey indexer

Nombre Alumno: Vicente Gras Mas

Nombre Alumno: Dan Anitei

"""


import operator
import re
import sys
import pickle
import random

def generador(sometxt):
    
    primerapal = sometxt[0][0]
    cont = sometxt[0][1][1]
    firstnum = sometxt[0][1][0]
    frase = primerapal
    numb = 0
    numFrases = 10
    pal = 0

    while numFrases != 1:
        if len(frase.split()) == 1:
            rand = random.randint(0,firstnum - 1)

        else:
            rand = random.randint(0,sometxt[pal][1][0] - 1)

        for pal in range(len(cont)):
            palsig = cont[pal][1]
            rand = rand - palsig
            if rand <= 0 :
                palsig = cont[pal][0]
                frase = frase + ' ' + palsig
                break
        if palsig == "$" or (len(frase.split()) == 25):
            numFrases = numFrases - 1
            randtext = frase + "\n"
            print(frase)
            primerapal = sometxt[0][0]
            cont = sometxt[0][1][1]
            frase = primerapal
            
        else:
            for pal in range(len(sometxt)):

                if sometxt[pal][0] == palsig:
                    cont = sometxt[pal][1][1]

       

    print(randtext)

    



def save_object(object,file_name):
    with open(file_name, 'wb') as fh:
        pickle.dump(object, fh)
        
def load_object(file_name):
    with open(file_name, 'rb') as fh:
        obj = pickle.load(fh)
    return obj

def syntax():
    print ("\n%s filename.txt \n" % sys.argv[0])
    sys.exit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        syntax()
    
    texto = load_object(sys.argv[1])
    generador(texto)