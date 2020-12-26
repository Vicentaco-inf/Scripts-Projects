#!/usr/bin/env python3

"""
PROYECTO DE PRÁCTICAS ALT

Nombre Alumno: Vicente Gras Mas

Nombre Alumno: Dan Anitei

Nombre Alumno: Julen Santiago Agredano

Nombre Alumno: Florea Fabian Iacob

"""

import pickle
import sys
import re
import json
import proyecto_ALT as Proj
from time import time

'''
                            Formato de los diccionarios:

            diccpal -------->  key: "palabra" -> value : {key:IdNoticia, value:[posPal]}

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
        elif postlist1[c1] > postlist2[c2]:
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
    for i in range(tamnot):

        if i > 0 and i not in postlist:
            postlistnot.append(i)

    return postlistnot


def queryaNOT(posting,tamnot):
    p = 0
    while p < len(posting)-1:
        if posting[p] == "NOT":
            if posting[p+1] is not '(':
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


def resolverParentesis(posting):

    openP = 0
    closeP = 0
    #encuentra el ultimo '('
    for i in range(len(posting)):
        if type(posting[i]) is not list and posting[i] == '(':
            openP = i
    #encuentra el ')' de cierre
    closeP = openP
    while closeP < len(posting):
        if type(posting[closeP]) is not list and posting[closeP] == ')':
            break
        closeP += 1
    #resuelve los terminos dentro de los parentesis
    res = resolveQuery(posting[openP+1:closeP])
    #reemplaza el parentesis por su resultado
    posting[openP:closeP+1] = res

    return posting

def resolverComillas(cadena,dicc):
    pos1 = 0
    pos2 = 0
    res = []
    aux = dicc.get(cadena[0],{})
    aux = sorted(aux.keys())

    if len(cadena) == 1:
        return aux
    for i in range(len(cadena)):
        if not i == len(cadena) - 1:
            sig = dicc.get(cadena[i+1],{})
            sig = sorted(sig.keys())
            aux = AND(aux,sig)
            diccionario1 = dicc.get(cadena[i],'')
            diccionario2 = dicc.get(cadena[i+1],'')
            for j in range(len(aux)):
                pos1 = 0
                pos2 = 0
                lista1 = sorted(diccionario1.get(aux[j]))
                lista2 = sorted(diccionario2.get(aux[j]))
                while pos1 < len(lista1) and pos2 < len(lista2):
                    if lista1[pos1] + 1 == lista2[pos2]:
                        res.append(aux[j])
                        pos1 = pos1 + 1
                        pos2 = pos2 + 1
                    else:
                        if lista1[pos1] < lista2[pos2]:
                            pos1 = pos1 + 1
                        else:
                            pos2 = pos2 + 1
                if pos1 == len(lista1):
                    pos1 = pos1 - 1
                if pos2 == len(lista2):
                    pos2 = pos2 - 1
                while pos1 < len(lista1) - 1:
                    if lista1[pos1] + 1 == lista2[pos2]:
                        res.append(aux[j])
                    pos1 = pos1 + 1
                while pos2 < len(lista2) - 1:
                    if lista1[pos1] + 1 == lista2[pos2]:
                        res.append(aux[j])
                    pos2 = pos2 + 1
            aux = res
            res = []
    for a in aux:
        if a not in res:
            res.append(a)
    return res


#parámetro dicc contiene el diccionario en cual se quiere buscar la query
def getQuery(query,dicc):
#recorremos la consulta
    cond_logica = ['AND','OR','NOT','(',')']
    posting = []
    q = 0
    dictionary = dicc
    diccT = ""
    while q < len(query):
        dicc = dictionary
        diccT = ''
        #convertimos la consulta en una lista donde apareceran los indices de las noticias donde aparece la palabra q y
        #los elementos booleanos se quedaran como tal. (ejemplo [hola AND adios] -> [[1,2,3], AND, [2,6])
        if query[q] not in cond_logica:

            if query[q].find(":") > 0:
                posPunto = query[q].find(":")
                diccT = query[q][0:posPunto]
                if diccT == 'article': dicc = diccpal
                query[q] = query[q][posPunto+1:]

            
            query[q] = query[q].lower()

            pos = query[q].find("%")
            if pos > 0:             
                dist = query[q][pos+1:]
                if int(dist) < 9:
                    list_leven = Proj.ram_poda_l_noact(trie, query[q][:pos], int(dist))
                else:
                    _, list_leven = Proj.levensthein_trie(trie, query[q][:pos], int(dist))
                #print (list_leven);
                listaPal = []
                for i in list_leven:
                    #print(i)
                    #print("\n")
                    listaNot = dicc.get(i,{})
                    arts = sorted(listaNot.keys())
                    listaPal = OR(arts,listaPal)
                posting = posting + [listaPal]
                #posting = OR(posting,arts)
            else:
                pos = query[q].find("@")
                if pos > 0:
                    dist = query[q][pos+1:]
                    if int(dist) < 9:
                        list_damerau = Proj.ram_poda_d_noact(trie, query[q][:pos], int(dist))
                    else:
                        _, list_damerau = Proj.damerau_trie(trie, query[q][:pos], int(dist))
                    

                    listaPal = []
                    for i in list_damerau:
                        #print(i[0])
                        listaNot = dicc.get(i,{})
                        arts = sorted(listaNot.keys())
                        listaPal = OR(arts,listaPal)
                    posting = posting + [listaPal]
                else:
                    listaNot = dicc.get(query[q],{})
                    arts = sorted(listaNot.keys())
                    #guarda en arts todas las noticias en cuales aparece el término q
                    posting = posting + [arts]

            #print(query[q])
        else:
            posting = posting + [query[q]]
        q = q + 1
    #print(posting)
    return posting

#noticiasDelQuery(posting[0],diccnot,querySinTratar,diccpal)
#diccnot -------->  key: "IdNoticia"-> value : [path,docId,posicion de la noticia dentro de docId]

def noticiasDelQuery(lista,dicnot,query,dicc):
    #mostrar = dicnot.get(lista[0])

    #En todos los casos se mostrará el nombre de los ficheros que contienen las noticias y
    #se informará al usuario del número total de noticias recuperadas como último
    #resultado mostrado.

    #se mostrara fecha titular keywords y article de una o 2 noticias
    if len(lista) < 3:

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
            print("Nombre del archivo de la noticia: " + NombreArchivo[-1] + "\n")
            print("--------------------------------------------------------------\n")

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
            buscarArt = articulo.lower().split()
            for p in range(len(buscarArt)):
                if len(buscarArt[p]) > 1:
                    buscarArt[p]=clean_text(buscarArt[p]).strip()
            articulo = articulo.split()
            #recorremos query donde se encuentran las palabras para hacer el snippet de cada noticia
            posMin = len(articulo)
            posMax = 0
            q = 0
            # recorrer los terminos del query
            while q < len(query):
                #salta si es un AND, OR
                if query[q] not in ["AND","OR","(",")"]:
                    #salta una posición extra para no incluir en el snippet el termino despues de NOT
                    if query[q] == "NOT":
                        q += 1
                    else:
                        existeTermino = diccpal.get(query[q],{})
                        if len(existeTermino) > 0 and l in existeTermino:
                            pos = buscarArt.index(query[q])
                            if pos < posMin:
                                posMin = pos
                            if pos > posMax:
                                posMax = pos

                q += 1

            if posMin > 3:
                if posMax < len(articulo)-3:
                    print("Snippet de '"," ".join(query),"': ", " ".join(articulo[posMin-3:posMax+3]), "\n")
                else:
                    print("Snippet de '"," ".join(query),"': "," ".join(articulo[posMin-3:posMax]), "\n")
            else:
                if posMax < len(articulo)-3:
                    print("Snippet de '"," ".join(query),"': "," ".join(articulo[posMin:posMax+3]), "\n")
                else:
                    print("Snippet de '"," ".join(query),"': "," ".join(articulo[posMin:posMax]), "\n")



            print("keywords: " + article.get("keywords") + "\n")
            #spliteamos la ruta por "/" y cogemos el ultimo elemento el cual es el archivo
            NombreArchivo = mostrar[0].split("/")
            print("Nombre del archivo de la noticia: " + NombreArchivo[len(NombreArchivo)-1] + "\n")
            print("--------------------------------------------------------------\n")

    #se mostrara fecha titulo y keywords en una sola linea de las 10 primeras noticias
    else:
        cnt = 0
        for l in lista:
            if cnt == 10:
                break

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
    print("Numero de noticias recuperadas: %d\n" % len(lista))


if __name__ == "__main__":
    t0 = time()
    if len(sys.argv)  < 2:
        syntax()

    tupli = load_object(sys.argv[1])

    diccpal = tupli[0]
    diccnot = tupli[1]
    tamnot = tupli[2]
    tamdoc = tupli[3]

    trie = Proj.usar_trie("TrieNoticias.txt")

    if len(sys.argv) < 3:
        while True:

            inp = input('Introduzca una frase:\n')
            if len(inp) == 0:
                print("Cerrando el programa.")
                sys.exit(0)
            else:
                queryOriginal = inp
                inp = inp.replace('(','( ')
                inp = inp.replace(')', ' )').split()

                query = inp

                inp = getQuery(inp,diccpal)
                inp = queryaNOT(inp,tamnot)
                while '(' in inp:
                    inp = resolverParentesis(inp)
                    inp = queryaNOT(inp,tamnot)

                inp = resolveQuery(inp)

                if len(inp[0]) > 0:
                    noticiasDelQuery(inp[0],diccnot,query,diccpal)
                else:
                    print("Numero de noticias recuperadas para la consulta '%s' : 0" % queryOriginal)


    else:
        queryOriginal = sys.argv[2]
        query = queryOriginal.replace('(','( ')
        query = query.replace(')', ' )').split()
        querySinTratar = query

        posting = getQuery(query,diccpal)
        posting = queryaNOT(posting,tamnot)
        while '(' in posting:
            posting = resolverParentesis(posting)
            posting = queryaNOT(posting,tamnot)

        posting = resolveQuery(posting)
        #le pasamos las noticias q cumplen el query, diccnot, diccpal, y la query para hacer los snippets

        if len(posting[0]) > 0:
        #if len(posting) > 0:
            noticiasDelQuery(posting[0],diccnot,querySinTratar,diccpal)
        else:
            print("Numero de noticias recuperadas para la consulta '%s' : 0" % queryOriginal)
    t1 = time()
    print(t1-t0)

