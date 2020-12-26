#!/usr/bin/env python3

import sys
import numpy as np
import json
import re
import pickle
from time import time

clean_re = re.compile('\W+')
def clean_text(text):
    return clean_re.sub(' ',text)

def save_object(object,file_name):
    with open(file_name, 'wb') as fh:
        pickle.dump(object, fh)

def syntax():
    print ("\n%s file_to_index \n" % sys.argv[0])
    sys.exit()


def levensthein_cad(cadena1, cadena2):
    if cadena1 == cadena2:
        return 0
    M = np.zeros(dtype=np.int8, shape=(len(cadena1)+1,len(cadena2)+1))
    coste = 0
    for i in range(len(cadena1)+1):
        M[i,0] = i

    for j in range(len(cadena2)+1):
        M[0,j] = j

    for j in range(1, len(cadena2)+1):
        for i in range(1, len(cadena1)+1):
            if cadena1[i-1] == cadena2[j-1]:
                coste = 0
            else:
                coste = 1
            M[i,j] = min(M[i-1,j-1] + coste, M[i,j-1] + 1, M[i-1,j] + 1)

    return M[-1,-1]

def leven_damerau(cadena1, cadena2):
    if cadena1 == cadena2:
        return 0
    M = np.zeros(dtype=np.int8, shape=(len(cadena1)+1,len(cadena2)+1))
    coste = 0
    for i in range(len(cadena1)+1):
        M[i,0] = i

    for j in range(len(cadena2)+1):
        M[0,j] = j

    for j in range(1, len(cadena2)+1):
        for i in range(1, len(cadena1)+1):
            if cadena1[i-1] == cadena2[j-1]:
                coste = 0
            else:
                coste = 1
            M[i,j] = min(M[i-1,j-1] + coste, M[i,j-1] + 1, M[i-1,j] + 1)
            if i > 1 and j > 1 and cadena1[i-1] == cadena2[j-2] and cadena1[i-2] == cadena2[j-1]:
                    M[i,j] = min(M[i,j], M[i-2, j-2] + coste)

    return M[-1,-1]


def levensthein_trie(cadena, tolerancia):

    M = np.zeros(dtype=np.int8, shape=(len(cadena), len(trie)))

    for i in range(len(cadena)):
        M[i,0] = i

    for nodo in range(len(trie)):
        M[0,nodo] = trie[nodo][3]

    for letra in range(len(cadena)):
        for nodo in range(len(trie)):
            #M[letra,nodo] = min()
            pass
    return M


def pal_distancia_menor_igual(cadena1, dictionary, distancia, metodo):
    d = 0
    dict_distancias = {}
    dict_res = {}

    for pal in dictionary.keys():
        if metodo == "levensthein":
            d = levensthein_cad(cadena1,pal)
        else:
            d = leven_damerau(cadena1,pal)
        list_d = dict_distancias.get(d,[])
        list_d.append(str(d) + ":" + pal)
        dict_distancias[d] = list_d

    for i in range(distancia+1):
        list_res = []
        for j in range(i+1):
            aux = dict_distancias.get(j, [])
            list_res = list_res + aux
        d_aux = dict_res.get(cadena1,{})
        d_aux[i] = list_res
        dict_res[cadena1] = d_aux

    return dict_res


def make_trie_diccionario(pal):
    global trie, num_nodo

    nodo_actual = 0

    if len(trie) == 0:
        trie[0] = [[nodo_actual, pal[0], num_nodo, False]]
        num_nodo += 1

    final = False

    for j in range(len(pal)):
        depth_trie = trie.get(j,[])


        if len(depth_trie) > 0:
            for i in range(len(depth_trie)):
                final = j == len(pal) -1

                if depth_trie[i][1] == pal[j]:
                    if depth_trie[i][0] == nodo_actual:    # existe transiccion [nodo_actual, pal[j], _]

                        if not depth_trie[i][3]:
                            depth_trie[i][3] = final
                        nodo_actual = depth_trie[i][2]
                        break

            else:                       # crea nueva rama con transiccion [nodo_actual, pal[j], _]

                depth_trie.append([depth_trie[i][0], pal[j], num_nodo, final])
                nodo_actual = num_nodo
                num_nodo += 1

        else:                       # crea nueva rama con transiccion [nodo_actual, pal[j], _]
            depth_trie.append([nodo_actual, pal[j], num_nodo, final])
            nodo_actual = num_nodo
            num_nodo += 1

        trie[j] = depth_trie


def make_trie(pal):
    global trie, nodo_actual
    nodo_padre = 0

    final = False

    for j in range(len(pal)):
        final = j == len(pal) - 1
        for nodo in trie:
            # nodo: 0 -> nodo padre, 1 -> letra, 2 -> nodo_actual, 3 -> profundidad, 4 -> F/NF
            if nodo[1] == pal[j] and nodo[3] == j+1 and nodo_padre == nodo[0]:    # si mismo simbolo, misma profundidad y mismo padre
                if nodo[4] == False:
                    nodo[4] = final
                nodo_padre = nodo[2]
                break

        else:
            trie.append([nodo_padre, pal[j], nodo_actual, j+1, final])
            nodo_padre = nodo_actual
            nodo_actual += 1



if __name__ == "__main__":

    makeTrie = False
    get_trie = False #True

    if len(sys.argv) < 2:
        syntax()
    elif len(sys.argv) < 4 and "-t" in sys.argv:
        makeTrie = True
        get_trie = False

    dictionary = {}
    res = {}
    trie = [[0,'', 0, 0, False]]    # nodo raiz
    nodo_actual = 1

    fich = open(sys.argv[1], "r")
    text = fich.read()
    text = clean_text(text)
    text = text.lower().split()


    if makeTrie:
        t0 = time()
        for pal in range(len(text)):
            dictionary[text[pal]] = text[pal]
            make_trie(text[pal])
        t1 = time()
        print(t1-t0)

        fich_trie = open('trie.txt', 'w')
        json.dump(trie, fich_trie)

    if get_trie:
        fich_trie = open('trie.txt', 'r')
        trie = json.load(fich_trie)

    #for pal in ["cara","caro", "caros", "codo"]:
    for pal in ["ab", "ob"]:
       make_trie(pal)

    print(trie)
    M = levensthein_trie("casos", len("casos"))
    print(M)




    #res = pal_distancia_menor_igual("consitucion", dictionary, 5, "d")

    #for key, value in sorted(res.items()):
    #    for k, v in sorted(value.items()):
    #        print(key," " + str(k) + " " + str(len(v)), v)
    #        pass


    #for word, value in sorted(res.items()):
    #   print(dictionary[word])




