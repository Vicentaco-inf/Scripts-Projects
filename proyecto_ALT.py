#!/usr/bin/env python3

"""
PROYECTO DE PRÁCTICAS ALT

Nombre Alumno: Vicente Gras Mas

Nombre Alumno: Dan Anitei

Nombre Alumno: Julen Santiago Agredano

Nombre Alumno: Florea Fabian Iacob

"""
import sys
import numpy as np
import json
import re
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

def damerau_trie(trie, cadena, tolerancia):
    res = []
    M = np.zeros(dtype=np.int8, shape=(len(cadena)+1, len(trie)))

    for i in range(len(cadena)+1):
        M[i,0] = i

    for nodo in range(len(trie)):
        M[0,nodo] = trie[nodo][3]

    coste = 0

    for letra in range(1, len(cadena)+1):
        for nodo in range(1, len(trie)):
            if trie[nodo][1] == cadena[letra-1]:
                coste = 0
            else:
                coste = 1
            M[letra,nodo] = min(M[letra-1,nodo] + 1, M[letra,trie[nodo][0]] + 1, M[letra-1, trie[nodo][0]] + coste)
            if letra > 1 and nodo > 1 and cadena[letra-1] == trie[trie[nodo][0]][1] and cadena[letra-2] == trie[nodo][1]:
                M[letra,nodo] = min(M[letra,nodo], M[letra-2, trie[trie[nodo][0]][0]] + coste)

            if letra == len(cadena) and trie[nodo][4]:
                distancia = M[letra,nodo]
                if distancia <= tolerancia and 0 <= distancia:
                    #res.append([trie[nodo][5], distancia])
                    res.append(trie[nodo][5])

    return M, res


def levensthein_trie(trie, cadena, tolerancia):
    res = []
    M = np.zeros(dtype=np.int8, shape=(len(cadena)+1, len(trie)))

    for i in range(len(cadena)+1):
        M[i,0] = i

    for nodo in range(len(trie)):
        M[0,nodo] = trie[nodo][3]

    coste = 0
    for letra in range(1, len(cadena)+1):
        for nodo in range(1, len(trie)):
            if trie[nodo][1] == cadena[letra-1]:
                coste = 0
            else:
                coste = 1
            M[letra,nodo] = min(M[letra-1,nodo] + 1, M[letra,trie[nodo][0]] + 1, M[letra-1, trie[nodo][0]] + coste)

            if letra == len(cadena) and trie[nodo][4]:
                distancia = M[letra,nodo]
                if distancia <= tolerancia and 0 <= distancia:
                    #res.append([trie[nodo][5], distancia])
                    res.append(trie[nodo][5])

    return M, res



# estado (i,nodo,dist), donde i, 0≤i≤|α|es la longitud de una subcadena de α,nodo es un nodo del trie τ y dist es la mejor distancia hasta el momento para esa subcadena y nodo
def ram_poda_l(trie, cadena, tolerancia):
    estado_ini = (0, 0, 0)
    listaAct = {estado_ini}
    res = set()
    while len(listaAct) > 0:
        nodoActivo = listaAct.pop()
        i = nodoActivo[0]
        nodo = nodoActivo[1]
        dist = nodoActivo[2]
        if dist <= tolerancia:

            if i < len(cadena):

                for n in trie[nodo][6]:             # para cada hijo, ramifica
                    if trie[n][1] == cadena[i]:
                        listaAct.add((i+1, n, dist)) # avanza el nodo y la longitud de la cadena si los simbolos coinciden
                    else:
                        listaAct.add((i, n, dist + 1))        # inserta el simbolo del nodo y avanza al hijo
                        listaAct.add((i+1, nodo, dist + 1))   # borra el simbolo de la cadena y se queda en el padre
                        listaAct.add((i+1, n, dist + 1))      # cambia el simbolo de la cadena por el del hijo
                else:
                    listaAct.add((i+1, nodo, dist + 1))   # borra el simbolo de la cadena y se queda en el padre

            else:
                for n in trie[nodo][6]:             # para cada hijo, ramifica
                    listaAct.add((i, n, dist + 1))        # inserta el simbolo del nodo y avanza al hijo


            if i == len(cadena) and trie[nodo][4]:
                res.add(trie[nodo][5])       # añade el prefijo del trie

    return res

def ram_poda_l_noact(trie, cadena, tolerancia):
    estado_ini = (0, 0, 0)
    listaAct = {estado_ini}
    listaPop = set()
    res = set()
    while len(listaAct) > 0:
        nodoActivo = listaAct.pop()
        listaPop.add(nodoActivo)
        i = nodoActivo[0]
        nodo = nodoActivo[1]
        dist = nodoActivo[2]

        for d in range(dist+1,tolerancia+1):
            listaPop.add((i,nodo,d))

        if dist <= tolerancia:
            #print(nodoActivo, " ", cadena[:i+1], " ", trie[nodo][5])

            if i < len(cadena):

                for n in trie[nodo][6]:             # para cada hijo, ramifica
                    #d = dicDist.get(trie[n][5], -1) # comprueba si prefijo existe en el diccionario de distancias

                    if trie[n][1] == cadena[i]:
                        if (i+1, n, dist) not in listaPop:
                            listaAct.add((i+1, n, dist)) # avanza el nodo y la longitud de la cadena si los simbolos coinciden
                    else:
                        if (i, n, dist + 1) not in listaPop: listaAct.add((i, n, dist + 1))        # inserta el simbolo del nodo y avanza al hijo
                        if (i+1, nodo, dist + 1) not in listaPop: listaAct.add((i+1, nodo, dist + 1))   # borra el simbolo de la cadena y se queda en el padre
                        if (i+1, n, dist + 1) not in listaPop: listaAct.add((i+1, n, dist + 1))      # cambia el simbolo de la cadena por el del hijo
                else:
                    if (i+1, nodo, dist + 1) not in listaPop: listaAct.add((i+1, nodo, dist + 1))   # borra el simbolo de la cadena y se queda en el padre

            else:
                for n in trie[nodo][6]:             # para cada hijo, ramifica
                    if (i, n, dist + 1) not in listaPop: listaAct.add((i, n, dist + 1))        # inserta el simbolo del nodo y avanza al hijo


            if i == len(cadena) and trie[nodo][4]:
                res.add(trie[nodo][5])       # añade el prefijo del trie

    return res

def ram_poda_d_noact(trie, cadena, tolerancia):
    estado_ini = (0, 0, 0)
    listaAct = {estado_ini}
    listaPop = set()
    res = set()
    while len(listaAct) > 0:
        nodoActivo = listaAct.pop()
        listaPop.add(nodoActivo)
        i = nodoActivo[0]
        nodo = nodoActivo[1]
        dist = nodoActivo[2]

        for d in range(dist+1,tolerancia+1):
            listaPop.add((i,nodo,d))

        if dist <= tolerancia:

            if i < len(cadena):

                for n in trie[nodo][6]:             # para cada hijo, ramifica
                    if trie[n][1] == cadena[i]:
                        if (i+1, n, dist) not in listaPop: listaAct.add((i+1, n, dist)) # avanza el nodo y la longitud de la cadena si los simbolos coinciden
                    else:
                        if (i, n, dist + 1) not in listaPop: listaAct.add((i, n, dist + 1))        # inserta el simbolo del nodo y avanza al hijo
                        if (i+1, nodo, dist + 1) not in listaPop: listaAct.add((i+1, nodo, dist + 1))   # borra el simbolo de la cadena y se queda en el padre
                        if (i+1, n, dist + 1) not in listaPop: listaAct.add((i+1, n, dist + 1))      # cambia el simbolo de la cadena por el del hijo

                    if i < len(cadena)-1 and cadena[i+1] == trie[n][1]:
                        for nh in trie[n][6]:
                            if cadena[i] == trie[nh][1]:
                                if (i+2, nh, dist + 1) not in listaPop: listaAct.add((i+2, nh, dist + 1))


                else:
                    if (i+1, nodo, dist + 1) not in listaPop:  listaAct.add((i+1, nodo, dist + 1))   # borra el simbolo de la cadena y se queda en el padre


            else:
                for n in trie[nodo][6]:             # para cada hijo, ramifica
                    if (i, n, dist + 1) not in listaPop: listaAct.add((i, n, dist + 1))        # inserta el simbolo del nodo y avanza al hijo


            if i == len(cadena) and trie[nodo][4]:
                res.add(trie[nodo][5])       # añade el prefijo del trie

    return res

def ram_poda_d(trie, cadena, tolerancia):
    estado_ini = (0, 0, 0)
    listaAct = {estado_ini}
    res = set()
    while len(listaAct) > 0:
        nodoActivo = listaAct.pop()
        i = nodoActivo[0]
        nodo = nodoActivo[1]
        dist = nodoActivo[2]
        if dist <= tolerancia:

            if i < len(cadena):

                for n in trie[nodo][6]:             # para cada hijo, ramifica
                    if trie[n][1] == cadena[i]:
                        listaAct.add((i+1, n, dist)) # avanza el nodo y la longitud de la cadena si los simbolos coinciden
                    else:
                        listaAct.add((i, n, dist + 1))        # inserta el simbolo del nodo y avanza al hijo
                        listaAct.add((i+1, nodo, dist + 1))   # borra el simbolo de la cadena y se queda en el padre
                        listaAct.add((i+1, n, dist + 1))      # cambia el simbolo de la cadena por el del hijo

                    if i < len(cadena)-1 and cadena[i+1] == trie[n][1]:
                        for nh in trie[n][6]:
                            if cadena[i] == trie[nh][1]:
                                listaAct.add((i+2, nh, dist + 1))


                else:
                    listaAct.add((i+1, nodo, dist + 1))   # borra el simbolo de la cadena y se queda en el padre

            else:
                for n in trie[nodo][6]:             # para cada hijo, ramifica
                    listaAct.add((i, n, dist + 1))        # inserta el simbolo del nodo y avanza al hijo


            if i == len(cadena) and trie[nodo][4]:
                res.add(trie[nodo][5])       # añade el prefijo del trie

    return res


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

def levensthein_trie_break(trie, cadena, tolerancia):
    res = []
    M = np.zeros(dtype=np.int8, shape=(len(cadena)+1, len(trie)))

    for i in range(len(cadena)+1):
        M[i,0] = i

    for nodo in range(len(trie)):
        M[0,nodo] = trie[nodo][3]

    coste = 0
    for letra in range(1, len(cadena)+1):
        Mayor = True
        for nodo in range(1, len(trie)):
            if trie[nodo][1] == cadena[letra-1]:
                coste = 0
            else:
                coste = 1
            M[letra,nodo] = min(M[letra-1,nodo] + 1, M[letra,trie[nodo][0]] + 1, M[letra-1, trie[nodo][0]] + coste)
            if Mayor:
                if M[letra,nodo] <= tolerancia:
                    Mayor = False
            if letra == len(cadena) and trie[nodo][4]:
                distancia = M[letra,nodo]
                if distancia <= tolerancia and 0 <= distancia:
                    #res.append([trie[nodo][5], distancia])
                    res.append(trie[nodo][5])
        if Mayor:
            break

    return M, res


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


def make_trie(pal, trie, nodo_actual):
    nodo_padre = 0
    prefijo = ""

    final = False

    for j in range(len(pal)):
        final = j == len(pal) - 1
        prefijo = pal[:j+1]
        for nodo in trie[nodo_padre][6]:
            # nodo: 0 -> nodo padre, 1 -> letra, 2 -> nodo_actual, 3 -> profundidad, 4 -> F/NF, 5 -> prefijo palabra, 6 -> hijos
            if trie[nodo][1] == pal[j] and trie[nodo][3] == j+1 and nodo_padre == trie[nodo][0]:    # si mismo simbolo, misma profundidad y mismo padre
                if trie[nodo][4] == False:
                    trie[nodo][4] = final
                nodo_padre = trie[nodo][2]
                break

        else:
            trie.append([nodo_padre, pal[j], nodo_actual, j+1, final, prefijo, []])
            if nodo_actual not in trie[nodo_padre][6]:
                trie[nodo_padre][6].append(nodo_actual)
            nodo_padre = nodo_actual
            nodo_actual += 1

    return nodo_actual, trie

#guardado objeto binario
def guardar_trie(trie,nomTrie):
    fich_trie = open(nomTrie, 'w')
    json.dump(trie, fich_trie)

def usar_trie(nomTrie):
    fich_trie = open(nomTrie, 'r')
    obj = json.load(fich_trie)
    return obj
    
def guardar_lista(lista, nomLista):
    fich_lista = open(nomLista, 'w')
    json.dump(lista, fich_lista)

def usar_lista(nomLista):
    fich_lista = open(nomLista, 'r')
    obj = json.load(fich_lista)
    return obj


if __name__ == "__main__":

    makeTrie = False
    get_trie = True # Ponlo a False si quieres depurar con el caso pequeño, a True lo hace con el Trie

    if len(sys.argv) < 2:
        syntax()
    elif len(sys.argv) < 4 and "-t" in sys.argv:
        makeTrie = True
        get_trie = False

    dictionary = {}
    res = {}
    trie = [[0,'', 0, 0, False, '',[]]]    # nodo raiz
    nodo_actual = 1

    fich = open(sys.argv[1], "r")
    text = fich.read()
    text = clean_text(text)
    text = text.lower().split()

    listaPalabras = list(set(text))
    

    if makeTrie:
        t0 = time()
        for pal in range(len(text)):
            dictionary[text[pal]] = text[pal]
            nodo_actual, trie = make_trie(text[pal], trie, nodo_actual)
            print(round(float(pal) / len(text) * 100,2))
        t1 = time()
        print(t1-t0)

        guardar_trie(trie,"Trie.txt")
        guardar_lista(listaPalabras, "Lista.txt")

    if get_trie:
        trie = usar_trie("Trie.txt")
        listaPalabras = usar_lista("Lista.txt")

    for i in range(0,11):
        print("constitución con Tolerancia: " + str(i))
        t0 = time()
        List = ram_poda_l_noact(trie, "constitución", i)
        t1 = time()
        print("Ramificacion_poda con levenshtein con lista de estados poped: ",t1-t0)
        print("Cantidad palabras recuperadas: " + str(len(List))+ "\n")
        #print(List)

        t0 = time()
        List = ram_poda_l(trie, "constitución", i)
        t1 = time()
        print("Ramificacion_poda con levenshtein sin lista de estados poped: ",t1-t0)
        print("Cantidad palabras recuperadas: " + str(len(List))+ "\n")

        t0 = time()
        List = ram_poda_d_noact(trie, "constitución", i)
        t1 = time()
        print("Ramificacion_poda con damerau con lista de estados poped: ",t1-t0)
        print("Cantidad palabras recuperadas: " + str(len(List))+ "\n")
        #print(List)

        t0 = time()
        List = ram_poda_d(trie, "constitución", i)
        t1 = time()
        print("Ramificacion_poda con damerau sin lista de estados poped: ",t1-t0)
        print("Cantidad palabras recuperadas: " + str(len(List))+ "\n")

        t0 = time()
        M, res = levensthein_trie(trie, "constitución", i)
        t1 = time()
        print("Levensthein programacion dinamica: ",t1-t0)
        print("Cantidad palabras recuperadas: " + str(len(res))+ "\n")

        t0 = time()
        M, res = levensthein_trie_break(trie, "constitución", i)
        t1 = time()
        print("Levenshtein trie con break en la gen de la matriz : ",t1-t0)
        print("Cantidad palabras recuperadas: " + str(len(res)) + "\n")

        t0 = time()
        M, res = damerau_trie(trie, "constitución", i)
        t1 = time()
        print("Damerau programacion dinamica: ",t1-t0)
        print("Cantidad palabras recuperadas: " + str(len(res)) + "\n")
        print("-----------------------------------------------------")
    #M, res = levensthein_trie(trie,"casa", 2)
    #print(len(res))
    #print(res)

    #for i in res:
    #    if i not in List:
    #        print(i)


    #res = pal_distancia_menor_igual("jabón", dictionary, 4, "d")

    #for key, value in sorted(res.items()):
    #    for k, v in sorted(value.items()):
    #        print(key," " + str(k) + " " + str(len(v)), v)
    #        pass


    #for word, value in sorted(res.items()):
    #   print(dictionary[word])