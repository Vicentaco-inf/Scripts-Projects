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

dicc = {}

clean_re = re.compile('\W+')
def clean_text(text):
    return clean_re.sub(' ', text)


def tokenizacion(filename):
    
    
    archivo = open(filename,'r')
    er = re.compile(";|!|\.|\?|\n\n")
    arch = er.split(archivo.read())
    for frase in range(len(arch)):
        
        arch[frase] = '$ ' + clean_text(arch[frase]).lower() + ' $'
       
        dicc = indices(arch[frase])
        
    
    return ordenar(dicc)

def ordenar(algo):
    entrada = sorted(algo.items(), key=operator.itemgetter(0))
    
    for i in range(len(entrada)):
        
        entrada[i][1][1] = sorted(entrada[i][1][1].items(), key=operator.itemgetter(1),reverse = True)

    return entrada
    
    

    
def indices(frase):

    cadena = frase.split()
    
    for palabra in range(len(cadena)):

        if palabra == len(cadena) - 1:

            lista = dicc.get(cadena[palabra],[1,{}])
            lista = [lista[0] + 1, lista[1]]
            dicc[cadena[palabra]] = lista
            break

        else:
            sigpal = cadena[palabra + 1]
            lista = dicc.get(cadena[palabra],[0,{}])
            diccint = lista[1]
            diccint[sigpal] = diccint.get(sigpal,0) + 1
            lista = [lista[0] + 1, diccint]
            dicc[cadena[palabra]] = lista
    
    return dicc



def save_object(object,file_name):
    with open(file_name, 'wb') as fh:
        pickle.dump(object, fh)

def syntax():
    print ("\n%s filename.txt newfilename\n" % sys.argv[0])
    sys.exit()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        syntax()
    
    texto = tokenizacion(sys.argv[1])
    print(texto)
    save_object(texto,sys.argv[2])
