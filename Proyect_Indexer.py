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
from datetime import datetime

diccpal = {}
diccnot = {}
docId = 1
docNot = 1

'''
                            Formato de los diccionarios:

            diccpal -------->  key: "palabra" -> value : [[IdNoticia,lugar donde aparece (ejemplo "title"),[posPal]],[mas listas en el mismo formato]....]



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

#se le pasa el id de la noticia(faltara observar si las id de las noticias son unicas) el lugar donde aparece(si es date, article etc) y el text a procesar
def tokenizar(idNot,lugar,text):
    global diccpal
    
    #usamos este if para q no se haga un split de la fecha ya que esta en formato dd-mm-yyyy
    if lugar is not "date":
        text = clean_text(text)
        text = text.lower().split()

    #recorremos texto para indexarlo en diccpal (diccionario de palabras)
    for pal in range(len(text)):
        
        #el valor de la clave de la palabra sera una lista o una lista vacia si no existe aun
        valpal = diccpal.get(text[pal],[])
        
        #si no existe aun se hara una lista con tres elementos, id noticia, el lugar donde aparece(si es date, article etc), y la posicion donde aparece la palabra
        if len(valpal) == 0:
            valpal = [[idNot,lugar,[pal]]]
            diccpal[text[pal]] = valpal

        else:
            #se recorre la lista con las listas con el formato [id noticia, lugar donde aparece, posicion de la palabra]
            for lista in range(len(valpal)):
                #si id noticia es igual a this.id noticia y lugar donde aparece es igual a this.lugar donde aparece, se pone su posicion en el tercer elemento
                #la cual es una lista con la posicion de la palabra en el texto y se sale del bucle for
                if valpal[lista][0] == idNot and valpal[lista][1] == lugar:
                    valpal[lista][2].append(pal)
                    diccpal[text[pal]] = valpal
                    break
            #si recorremos el bucle for entero y no salta el break, significa que es una aparicion en un lugar nuevo o en una noticia nueva y se añade al valor 
            #de la clave de la palabra ya que es una lista de listas de aparicion
            else:
                listaux = [idNot,lugar,[pal]]
                valpal = valpal + [listaux]
                diccpal[text[pal]] = valpal
    #for word, count in sorted(diccpal.items()):

        #print(word," ",count)
#guardado objeto binarioç


def save_object(object,file_name):
    with open(file_name, 'wb') as fh:
        pickle.dump(object, fh)

if __name__ == "__main__":
    
    

    if len(sys.argv) < 3:
        syntax()    
    
    #if not os.path.exists(idir):
    #    os.mkdir(idir)

    initime = datetime.now()
    for dirname, subdirs, files in os.walk(sys.argv[1]):
        
        for filename in files:
            fullname = os.path.join(dirname, filename)
            artic = load_json(fullname)
            
            #recorremos la lista de noticias del archivo ya que al hacer load_json se pone una noticia por elemento de lista
            for art in range(len(artic)):
                
                textArt = artic[art].get("article")
                tokenizar(docNot,"article",textArt)

                textTitle = artic[art].get("title")
                tokenizar(docNot,"title",textTitle)

                textKey = artic[art].get("keywords")
                tokenizar(docNot,"keywords",textKey)

                textSum = artic[art].get("summary")
                tokenizar(docNot,"summary",textSum)

                textDat = artic[art].get("date")
                tokenizar(docNot,"date",textDat)

                #diccionario de noticias
                diccnot[docNot] = [fullname,docId,art]
                docNot = docNot + 1
                print(docNot)
            

            #aumentar docId
            docId += 1
    fintime = datetime.now()
    print(fintime - initime)
    tupli = [diccpal,diccnot,docNot,docId]
    #print(diccnot)
    save_object(tupli,sys.argv[2])

    #for word, count in sorted(diccnot.items()):

    #    print(word," ",count)





