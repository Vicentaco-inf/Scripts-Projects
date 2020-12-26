#!/usr/bin/env python
#! -*- encoding: utf8 -*-

from operator import itemgetter
import re
import sys

clean_re = re.compile('\W+')
def clean_text(text):
    return clean_re.sub(' ', text)

def sort_dic(d):
    for key, value in sorted(d.items(), key=itemgetter(1), reverse=True):
        yield key, value

def text_statistics(filename, to_lower=True, remove_stopwords=True):
   
    NumLin = 0 #COMPLETED
    NumPal = 0 #COMPLETED
    NumSSWords = 0 #Numero de palabras sin stop words #COMPLETED
    NumChar = 0 #COMPLETED
    letraDic = {}
    letraUnic = {}
    Vocabulario = {}
    palabrasTxt = {} 

    StopWords = open('stopwords_en.txt','r')
    sWords = StopWords.read().split()
    FileIn = open(filename,'r')

    for i in FileIn:
        FraseI = clean_text(i).split()
        
        NumLin += 1
        NumPal += len(FraseI) #Coge una frase, le quita lo que no es alfanumerico, lo convierte en un array (split) y mide su longitud
        for pal in FraseI:

            if to_lower: #Si segundo parametro es pasar a minusculas
                pal = pal.lower()

            if not remove_stopwords:
               
                NumChar += len(pal)
                palabrasTxt[pal] = palabrasTxt.get(pal,0) + 1 #Vocabulario y frecuencia de las palabras con StopWords
                Vocabulario.setdefault(pal,1)
                
                for char in pal:
                    letraDic[char] = letraDic.get(char,0) + 1 #Cuantas veces aparece una letra
                    letraUnic.setdefault(char,1) 
            else:

                if pal not in sWords:
                    NumSSWords += 1
                    NumChar += len(pal)
                    palabrasTxt[pal] = palabrasTxt.get(pal,0) + 1 #Vocabulario y frecuencia de las palabras sin StopWords
                    Vocabulario.setdefault(pal,1)

                    for char in pal:
                        letraDic[char] = letraDic.get(char,0) + 1 #Cuantas veces aparece una letra
                        letraUnic.setdefault(char,1) 

            

    print("Numero de lineas:",NumLin)    #Numero de lineas            
    print("Numero de palabras: ",NumPal) #Numero de palabras
    if remove_stopwords:
        print("Numero de palabras sin StopWords: ",NumSSWords) #Numero de palabras sin stop words
    print("Numero de palabras que hay en el vocabulario:",len(Vocabulario)) #Numero pal en el vocab
    print("Numero de letras: ",NumChar) #Numero de letras
    print("Numero de letras unicas que se emplean",len(letraUnic)) #Numero de letras diferentes
    

    print ("Palabras por orden alfabetico:")
    for word, count in sorted(palabrasTxt.items()):
        print("\t%s   \t%d" % (word, count))

    print ("Palabras por frecuencia:")
    for word, count in sort_dic(palabrasTxt):
        print("\t%s   \t%d" % (word, count))

    print ("Letras por orden alfabetico:")
    for word, count in sorted(letraUnic.items()):
        print("\t%s   \t%d" % (word, count))
    
    print ("letras por frecuencia:")
    for word, count in sort_dic(letraDic):
        print("\t%s   \t%d" % (word, count))
    
    

    

    
    
       
     


def syntax():
    print ("\n%s filename.txt [to_lower?[remove_stopwords?]\n" % sys.argv[0])
    sys.exit()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        syntax()
    name = sys.argv[1]
    lower = False
    stop = False
    if len(sys.argv) > 2:
        lower = (sys.argv[2] in ('1', 'True', 'yes'))
        if len(sys.argv) > 3:
            stop = (sys.argv[3] in ('1', 'True', 'yes'))
    text_statistics(name, to_lower=lower, remove_stopwords=stop)

