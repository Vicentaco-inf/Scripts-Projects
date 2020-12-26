#!/usr/bin/env python3

"""
5.- Indexer

Nombre Alumno: Vicente Gras Mas

Nombre Alumno: Dan Anitei

"""

import sys
import os
import json
import re
import pickle
import time


diccpal = {}
dicctitle = {}
dicckeywords = {}
diccsummary = {}
diccnot = {}
docId = 1
docNot = 1

'''
                            Formato de los diccionarios:

            diccpal -------->  key: "palabra" -> value : {key:IdNoticia, value:[posPal]}
            dicctitle -------->  key: "palabra" -> value : {key:IdNoticia, value:[posPal]}
            dicckeywords -------->  key: "palabra" -> value : {key:IdNoticia, value:[posPal]}
            diccsummary -------->  key: "palabra" -> value : {key:IdNoticia, value:[posPal]}

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

    #quitamos los simbolos non alfanumericos y ponemos los terminos en minusculas
    text = clean_text(text)
    text = text.lower().split()

    #recorremos texto para indexarlo en el diccionario que le corresponde (article, title, keywords, summary)
    for pal in range(len(text)):

        #el valor de la clave de la palabra sera un diccionario donde guardamos como clave: idNot, y valor: posiciones del termino dentro de la noticia
        valpal = dicc.get(text[pal],{})

        #si no existe aun se hara una lista con la posicion donde aparece la palabra
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

    initime = time
    for dirname, subdirs, files in os.walk(sys.argv[1]):

        for filename in files:
            fullname = os.path.join(dirname, filename)
            artic = load_json(fullname)

            #recorremos la lista de noticias del archivo ya que al hacer load_json se pone una noticia por elemento de lista
            for art in range(len(artic)):

                textArt = artic[art].get("article")
                tokenizar(docNot,textArt,diccpal)

                textTitle = artic[art].get("title")
                tokenizar(docNot,textTitle,dicctitle)

                textKey = artic[art].get("keywords")
                tokenizar(docNot,textKey,dicckeywords)

                textSum = artic[art].get("summary")
                tokenizar(docNot,textSum,diccsummary)

                #textDat = artic[art].get("date")
                #tokenizar(docNot,"date",textDat)

                #diccionario de noticias
                diccnot[docNot] = [fullname,docId,art]
                docNot += 1
                print(docNot)

            #aumentar docId
            docId += 1

    tupli = [diccpal,diccnot,docNot,docId,dicctitle,dicckeywords,diccsummary]
    #print(diccnot)
    save_object(tupli,sys.argv[2])


    #for word, count in sorted(dicctitle.items()):
    #    print(word," ",count)

    #for word, count in sorted(diccnot.items()):
    #    print(word," ",count)





