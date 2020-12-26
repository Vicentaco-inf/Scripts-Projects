#!/usr/bin/env python3

import pickle
import sys
import re
import json
from colorama import Fore

'''
                            Formato de los diccionarios:

            diccpal -------->  key: "palabra" -> value : {key:IdNoticia, value:[posPal]}
            dicctitle -------->  key: "palabra" -> value : {key:IdNoticia, value:[posPal]}
            dicckeywords -------->  key: "palabra" -> value : {key:IdNoticia, value:[posPal]}
            diccsummary -------->  key: "palabra" -> value : {key:IdNoticia, value:[posPal]}


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

    while contlist1 < len(postlist1) and contlist2 < len(postlist2):

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
    c1 = 0
    c2 = 0

    if len(postlist1) == 0 and len(postlist2) != 0:
        return postlist2
    if len(postlist2) == 0 and len(postlist1) != 0:
        return postlist1

    while c1 < len(postlist1) and c2 < len(postlist2):

        if postlist1[c1] < postlist2[c2]:
            listor.append(postlist1[c1])
            c1 += 1
        elif postlist1[c1] > postlist1[c2]:
            listor.append(postlist2[c2])
            c2 += 1
        else:
            listor.append(postlist1[c1])
            c1 += 1
            c2 += 1

    while c1 < len(postlist1):
        listor.append(postlist1[c1])
        c1 += 1

    while c2 < len(postlist2):
        listor.append(postlist2[c2])
        c2 += 1

    return sorted(listor)


def NOT(postlist, tamnot):
    postlistnot = []
    for i in range(tamnot+1):

        if i not in postlist:
            postlistnot.append(i)

    return postlistnot



def queryaNOT(posting,tamnot):
    p = 0
    while p < len(posting)-1:
        if posting[p] == "NOT":

            posting[p] = NOT(posting[p + 1],tamnot)
            posting.pop(p + 1)
        p = p + 1
    return posting



def resolveQuery(posting):

    while len(posting) > 1:

        if posting[1] == "AND":
            posting[0] = AND(posting[0],posting[2])
            posting.pop(2)
            posting.pop(1)

        elif posting[1] == 'OR':
            posting[0] = OR(posting[0],posting[2])
            posting.pop(2)
            posting.pop(1)

        else:
            posting[0] = AND(posting[0],posting[1])
            posting.pop(1)

    return posting


#parámetro dicc contiene el diccionario en cual se quiere buscar la query
def getQuery(query,dicc):
#recorremos la consulta
    cond_logica = ['AND','OR','NOT']
    posting = []

    for q in range(len(query)):
        #convertimos la consulta en una lista donde apareceran los indices de las noticias donde aparece la palabra q y
        #los elementos booleanos se quedaran como tal. (ejemplo [hola AND adios] -> [[1,2,3], AND, [2,6])
        if query[q] not in cond_logica:
            query[q] = query[q].lower()
            listaNot = dicc.get(query[q],{})

            #guarda en arts todas las noticias en cuales aparece el termino q
            arts = sorted(listaNot.keys())

            posting = posting + [arts]

        else:
            posting = posting + [query[q]]
    return posting


#diccnot -------->  key: "IdNoticia"-> value : [path,docId,posicion de la noticia dentro de docId]

def noticiasDelQuery(lista,dicnot,query,dicc):
    mostrar = dicnot.get(lista[0])
    
    #En todos los casos se mostrará el nombre de los ficheros que contienen las noticias y
    #se informará al usuario del número total de noticias recuperadas como último
    #resultado mostrado.

#se mostrara fecha titular keywords y article de una o 2 noticias
    if len(lista) < 3 and len(lista) > 0:
        
        for l in lista:
            #mostrar es [path,docId,posicion de la noticia dentro de docId] de la noticia l de la lista final del resultado del query
            mostrar = dicnot.get(l)
            #cargamos json y accedemos al articulo q se encuentra en la posicion de la noticia dentro del json
            article = load_json(mostrar[0])
            article = article[mostrar[2]]
            print("--------------------------------------------------------------\n")
                #el print siguiente esta por depuracion, en verdad no vale pa na(se repite en los siguientes elif y else)
            print("noticia: " + str(l) + "\n")
            print("fecha: " + article.get("date") + "\n")
            print("titulo: " + article.get("title") + "\n")
            print("keywords: " + article.get("keywords") + "\n")
            print("articulo: " + article.get("article") + "\n")
            #spliteamos la ruta por "/" y cogemos el ultimo elemento el cual es el archivo
            NombreArchivo = mostrar[0].split("/")
            print("Nombre del archivo de la noticia: " + NombreArchivo[len(NombreArchivo)-1] + "\n")
            print("--------------------------------------------------------------\n")
            #este print nose porq no va
        print("Numero de noticias recuperadas: " + len(lista))
        
        #return
    #si hay de 3 a 5 noticias se mostrara fecha titulo snippets y keywords de las noticias en lista
    elif len(lista) < 6:
        
        for l in lista:
            mostrar = dicnot.get(l)
            #path archivo noticia
            article = load_json(mostrar[0])
            #orden de la noticia dentro del archivo article
            article = article[mostrar[2]]
            print("--------------------------------------------------------------\n")
            print("noticia: " + str(l) + "\n")
            print("fecha: " + article.get("date") + "\n")
            print("titulo: " + article.get("title") + "\n")
            # Si no se hace búsqueda por el cuerpo de la noticia se mostrarán las primeras 100 palabras.
            # Esto no esta implementado porq no se lo q es (el comentario de arriba), snippets si q esta implementado

            #---------------------------------------------------------------------------------
            #----------------------------------SNIPPET----------------------------------------

            #Un snippet de un termino es una subcadena del documento que contiene el termino y
            #un contexto por la izquierda y derecha. Prueba diferentes tamaños de contexto.
            #esto habra q hacer testeo en el rango de palabras q se devuelva en cada snippet para q
            #el snippet tenga sentido en un contexto

            #---------------------------------------------------------------------------------
            #---------------------------------------------------------------------------------

            #articulo es el tag article dentro de la noticia especifica q nos devuelve el path mostrar[0]
            articulo = article.get("article")
            articulo = articulo.split()
            #recorremos query donde se encuentran las palabras para hacer el snippet de cada noticia
            for q in query:
                snippets = []
                if q not in ["AND","OR","NOT"]:
                    #diccpal -------->  key: "palabra" -> value : {key:IdNoticia, value:[posPal]}
                    #si posPal es "IS NOT" significa q no esta porq tendra NOT delante en el query por lo tanto no se pueden hacer snippets de ella
                    #ya q no existe
                    posPal = dicc.get(q,"IS NOT")

                    if posPal == "IS NOT":
                        continue

                    #lista de posiciones dentro de la noticia de la palabra
                    posPal = posPal.get(l)
                    
                    for pos in posPal:
                        if pos == 0:
                            snippets = snippets + [articulo[0] + " " + articulo[1] + " " + articulo [2]]

                        elif pos == len(articulo) - 1:
                            posPalSnip = pos
                            snippets = snippets + [articulo[posPalSnip - 2] + " " + articulo[posPalSnip - 1] + " " + articulo [posPalSnip]]

                        else:
                            #OJO, a veces da out of bounds exception y ni idea de porq, si no, funciona bien
                            snippets = snippets + [articulo[pos - 1] + " "  + articulo[pos] + " " + articulo [pos + 1]]

                    #Mostramos snippets de dicha palabra, si hay varias palabras en el query se crearan los snippets sobre el query
                    print("Snippets de la palabra " + "\"" + q + "\"" + " dentro del articulo: " + str(snippets).strip("[]") + "\n")


            print("keywords: " + article.get("keywords") + "\n")
            #spliteamos la ruta por "/" y cogemos el ultimo elemento el cual es el archivo
            NombreArchivo = mostrar[0].split("/")
            print("Nombre del archivo de la noticia: " + NombreArchivo[len(NombreArchivo)-1] + "\n")
            print("--------------------------------------------------------------\n")
        print("Numero de noticias recuperadas: " + len(lista))
        #return

    #se mostrara fecha titulo y keywords en una sola linea de las 10 primeras noticias
    else:
        cnt = 0
        for l in lista:
            if cnt == 10:
                return
            mostrar = dicnot.get(l)
            article = load_json(mostrar[0])
            article = article[mostrar[2]]
            print("--------------------------------------------------------------\n")
            print("noticia: " + str(l) + "," + "fecha: " + article.get("date") + "titulo: " + article.get("title") + "keywords: " + article.get("keywords") + "\n")
            #spliteamos la ruta por "/" y cogemos el ultimo elemento el cual es el archivo
            NombreArchivo = mostrar[0].split("/")
            print("Nombre del archivo de la noticia: " + NombreArchivo[len(NombreArchivo)-1] + "\n")
            print("--------------------------------------------------------------\n")
            cnt = cnt + 1
        print("Numero de noticias recuperadas: " + len(lista))


if __name__ == "__main__":

    if len(sys.argv)  < 2:
        syntax()

    tupli = load_object(sys.argv[1])

    diccpal = tupli[0]
    diccnot = tupli[1]
    tampal = tupli[2]
    tamnot = tupli[3]
    dicctitle = tupli[4]
    dicckeywords = tupli[5]
    diccsummary = tupli[6]


    if len(sys.argv) < 3:
        while True:

            inp = input('Introduzca una frase:\n')
            if len(inp) == 0:
                print("Cerrando el programa.")
                sys.exit(0)
            else:

                inp = inp.split()
                query = inp
                #buscamos en el diccionario de tipo 'article'
                inp = getQuery(inp,diccpal)
                inp = queryaNOT(inp,tamnot)
                inp = resolveQuery(inp)
                print(noticiasDelQuery(inp[0],diccnot,query,diccpal))

    else:
        query = sys.argv[2]
        query = query.split()
        querySinTratar = query
            #buscamos en el diccionario de tipo 'article'
        posting = getQuery(query,diccpal)
        posting = queryaNOT(posting,tamnot)
        posting = resolveQuery(posting)
        #le pasamos las noticias q cumplen el query, diccnot, diccpal, y la query para hacer los snippets
        #al final de toda consulta en shell devuelve un none y ni puta idea porq
        #OJO, esto ahora mismo solo funciona para article, habra q implementar un for en algun lado para 
        #q los otros 3 diccionarios tambien se hagan sus respectivas consultas y sus respectivos snippets
        print(noticiasDelQuery(posting[0],diccnot,querySinTratar,diccpal))
        

