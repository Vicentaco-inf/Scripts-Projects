#!/usr/bin/env python3

"""
PROYECTO DE PRÁCTICAS ALT

Nombre Alumno: Vicente Gras Mas

Nombre Alumno: Dan Anitei

Nombre Alumno: Julen Santiago Agredano

Nombre Alumno: Florea Fabian Iacob

"""

import sys
import os
import json
import re
import pickle
import proyecto_ALT as Proj

diccpal = {}
diccnot = {}
docId = 1
docNot = 1

'''
                            Formato de los diccionarios:

            diccpal ---------->  key: "palabra" -> value : {key:IdNoticia, value:[posPal]}

            diccnot -------->  key: "IdNoticia"-> value : [path,docId,posicion de la noticia dentro de docId]


'''


#se ha añadido un segundo parametro al metodo open para que no parta las palabras cuando se encuentre una letra acentuada o una ñ
def load_json(filename):
    with open(filename,encoding = "utf-8") as fh:
        obj = json.load(fh)
    return obj


def syntax():
    print ("\n%s doc_directory doc_indexer \n" % sys.argv[0])
    sys.exit()

clean_re = re.compile('\W+')
def clean_text(text):
    return clean_re.sub(' ',text)

#se le pasa el id de la noticia, el text a procesar y el tipo de diccionario donde guardar los terminos (article, title, keywords, summary)
def tokenizar(idNot,text,dicc):
    global trie, nodo_actual
    #quitamos los simbolos non alfanumericos y ponemos los terminos en minusculas

    text = clean_text(text)
    text = text.lower().split()

    #recorremos texto para indexarlo en el diccionario que le corresponde (article, title, keywords, summary)
    for pal in range(len(text)):
        nodo_actual, trie = Proj.make_trie(text[pal],trie,nodo_actual)

        #el valor de la clave de la palabra será un diccionario donde guardamos como clave: idNot, y valor: posiciones del termino dentro de la noticia
        valpal = dicc.get(text[pal],{})

        #si no existe todavia se hara una lista con la posicion donde aparece la palabra
        posiciones = valpal.get(idNot,[])
        if len(posiciones) == 0:
            valpal[idNot]=[pal]
            dicc[text[pal]] = valpal

        #si existe, se añade la posición a la lista
        else:
            posiciones.append(pal)
            valpal[idNot]=posiciones
            dicc[text[pal]] = valpal

#guardado objeto binario
def save_object(object,file_name):
    with open(file_name, 'wb') as fh:
        pickle.dump(object, fh)


if __name__ == "__main__":

    if len(sys.argv) < 3:
        syntax()

    trie = [[0,'', 0, 0, False, '',[]]]    # nodo raiz
    nodo_actual = 1

    for dirname, subdirs, files in os.walk(sys.argv[1]):

        for filename in files:
            fullname = os.path.join(dirname, filename)
            artic = load_json(fullname)

            print(fullname)

            #recorremos la lista de noticias del archivo ya que al hacer load_json se pone una noticia por elemento de lista
            for art in range(len(artic)):


                textArt = artic[art].get("article")
                tokenizar(docNot,textArt,diccpal)

                #diccionario de noticias
                diccnot[docNot] = [fullname,docId,art]
                docNot += 1


            #aumentar docId
            docId += 1


    tupli = [diccpal,diccnot,docNot,docId]
    save_object(tupli,sys.argv[2])

    Proj.guardar_trie(trie, "TrieNoticias.txt")
    #print(trie)

    #for word, count in sorted(dicctitle.items()):
    #    print(word," ",count)

    #for word, count in sorted(diccnot.items()):
    #    print(word," ",count)

    #for word, count in sorted(diccdate.items()):
    #    print(word," ",count)




