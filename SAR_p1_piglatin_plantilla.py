#!/usr/bin/env python
#! -*- encoding: utf8 -*-

"""
1.- Pig Latin

Nombre Alumno: Vicente Gras Mas

Nombre Alumno: Dan Anitei
"""

import sys
import os



def piglatin_word(word):
    """
    Esta función recibe una palabra en inglés y la traduce a Pig Latin

    :param word: la palabra que se debe pasar a Pig Latin
    :return: la palabra traducida
    """
    vocales = ['a','e','i','o','u','y']
    primeraesmayus = False
    todomayus = False
    coletilla = ""
    aux = ""
    if word[0].isnumeric():
        return word
    
    if word.isupper(): todomayus = True
    if word[0].isupper(): primeraesmayus = True
        
    word = word.lower()
    for i in range(len(word)):
        if not word[i].isalpha():
            coletilla = word[i:]
            word = word[:i]
            break
            
    if word[0] in vocales:
        word = word + 'yay' + coletilla    
        if todomayus: word = word.upper()
        if primeraesmayus:
            word = word[0].upper() + word[1:]
        return word
        
    for i in range(len(word)):
        if word[i] in vocales:
            aux = word[:i]
            word = word[i:] + aux + 'ay' + coletilla
            break
            
    if todomayus: word = word.upper()
    if primeraesmayus:
        word = word[0].upper() + word[1:]
        
    return word
        
        
    


def piglatin_sentence(sentence):
    """
    Esta función recibe una frase en inglés i la traduce a Pig Latin

    :param sentence: la frase que se debe pasar a Pig Latin
    :return: la frase traducida
    """
    words = sentence.split()
    
    for i in range(len(words)):
        words[i] = piglatin_word(words[i])
    sentence = " ".join(words)
    return  sentence

################################################
#############    AMPLIACIÓN    #################
################################################
def piglatin_file(fichero):
    """
    Esta función recibe un fichero con contenido en ingles y lo traduce a Pig Latin

    :param fichero: el fichero que se debe pasar a Pig Latin
    :return: fichero nuevo con la traducción
    """
    f = open(fichero,'r')
    out = fichero[:-4] + '_piglatin.txt'
    if os.path.isfile(out):
        out = input("El fichero '" + out + "' ya existe. Elige otro nombre para el fichero a generar:\n")        
    fout = open(out,'w')
    for line in f:
        fout.write(piglatin_sentence(line))
        fout.write('\n')
    
    print("El fichero" + out + " se ha creado")
    f.close()
    fout.close()
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if len(sys.argv) > 2: 
            print("El programa solo acepta un argumento")
            sys.exit(0)
        argument = sys.argv[1]
        if argument.startswith('-f'):
            if not argument.endswith('.txt'):
                print('El fichero pasado como parámetro tiene que ser del tipo .txt')
            else:
                piglatin_file(argument[3:])
        else:
            print(piglatin_sentence(argument))
    else:
        
        while True:
            
            inp = input('Introduzca una frase:\n')
            if len(inp) == 0:
                print("Cerrando el programa.")
                sys.exit(0)
            else:
                print(piglatin_sentence(inp))                
            
