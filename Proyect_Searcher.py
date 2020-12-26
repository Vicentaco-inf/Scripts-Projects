#!/usr/bin/env python3

import pickle
import sys
import re
import json

'''
                            Formato de los diccionarios:

            diccpal -------->  key: "palabra" -> value : [[IdNoticia,lugar donde aparece (ejemplo "title"),[posPal]],[mas listas en el mismo formato]....]



            diccnot -------->  key: "IdNoticia"-> value : [path,docId,posicion de la noticia dentro de docId]


'''

clean_re = re.compile('\W+')
def clean_text(text):
    return clean_re.sub(' ',text)

def load_json(filename):
    with open(filename,encoding = "utf-8") as fh:
        obj = json.load(fh)
    return obj

def syntax():
    print ("\n%s doc_palab consulta(opcionalmente) \n" % sys.argv[0])
    sys.exit()

def load_object(file_name):
    with open(file_name, 'rb') as fh:
        obj = pickle.load(fh)
    return obj

def AND(postlist1, postlist2):

    listand = []
    contlist1 = 0
    contlist2 = 0
    
    if len(postlist1) == 0 or len(postlist2) == 0:
        
        return listand
    
    while contlist1 != len(postlist1) and contlist2 != len(postlist2):
        
        if postlist1[contlist1] > postlist2[contlist2]:
            contlist2 = contlist2 + 1
        elif postlist1[contlist1] < postlist2[contlist2]:
            contlist1 = contlist1 + 1
        else:
            listand = listand + [postlist1[contlist1]]
            contlist1 = contlist1 + 1
            contlist2 = contlist2 + 1
    
    return listand


def OR(postlist1, postlist2):

    listor = []
    
    if len(postlist1) == 0 and len(postlist2) != 0:
        return postlist2
    if len(postlist2) == 0 and len(postlist1) != 0:
        return postlist1

    while len(postlist1) != 0 and len(postlist2) != 0:
        
        if postlist1[0] not in listor:
            listor = listor + [postlist1.pop(0)]
        else:
            postlist1.pop(0)

        if postlist2[0] not in listor:
            listor = listor + [postlist2.pop(0)]
        else:
            postlist2.pop(0)
        
    while len(postlist1) != 0:
        if postlist1[0] not in listor:
            listor = listor + [postlist1.pop(0)]
        else:
            postlist1.pop(0)

    while len(postlist2) != 0:
        if postlist2[0] not in listor:
            listor = listor + [postlist2.pop(0)]
        else:postlist2.pop(0)

    return listor


def NOT(postlist, tamnot):
    
    postlistnot = []
    for i in range(tamnot+1):
        
        if i not in postlist:
            
            postlistnot = postlistnot + [i]
        else:
            pass
    return postlistnot
    
def queryaNOT(posting):
    p = 0
    while p < len(posting)-1:
        if posting[p] == "NOT":
            
            posting[p] = NOT(posting[p + 1],tamnot)
            posting.pop(p + 1)
            if p == len(posting) - 1:
                break
        p = p + 1
    #return posting

def resolveQuery(posting):
    
    while len(posting) > 1:
        
        if posting[1] == "AND":
            posting[0] = AND(posting[0],posting[2])
        else:
            posting[0] = OR(posting[0],posting[2])
        posting.pop(2)
        posting.pop(1)
    #return posting

def getQuery(query,diccpal):
#recorremos la consulta
    cond_logica = ['AND','OR','NOT']
    posting = []
    arts = []
    for q in range(len(query)):
        #convertimos la consulta en una lista donde apareceran los indices de las noticias donde aparece la palabra q y 
        #los elementos booleanos se quedaran como tal. (ejemplo [hola AND adios] -> [[1,2,3], AND, [2,6])
        if query[q] not in cond_logica:
            query[q] = query[q].lower()
            lista = diccpal.get(query[q],[])
            for l in lista:
                if l[0] not in arts:
                    arts = arts + [l[0]]
            posting = posting + [arts]
            arts = []
        else:
            posting = posting + [query[q]]
    return posting

def showInfo(lista):
    if len(lista) < 3:
        for l in lista:
            pass
    pass




if __name__ == "__main__":
  
    if len(sys.argv)  < 2:
        syntax()

    tupli = load_object(sys.argv[1])
    
    diccpal = tupli[0]
    diccnot = tupli[1]
    tampal = tupli[2]
    tamnot = tupli[3]

    if len(sys.argv) < 3:
        while True:
            
            inp = input('Introduzca una frase:\n')
            if len(inp) == 0:
                print("Cerrando el programa.")
                sys.exit(0)
            else:

                inp = inp.split()
                inp = getQuery(inp,diccpal)
                queryaNOT(inp)
                resolveQuery(inp)
                print(inp[0])
            
    else:

        query = sys.argv[2]
        query = clean_text(query)
        query = query.split()
        posting = getQuery(query,diccpal)
        queryaNOT(posting)
        resolveQuery(posting)

        print(posting[0])
        