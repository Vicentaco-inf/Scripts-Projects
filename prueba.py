#!/usr/bin/env python
#! -*- encoding: utf8 -*-
import random
num = 11
frase = ''
cnt = 0 
while cnt != 50:

    cnt = cnt + 1
    rand = random.randint(1,num - 1)
    print(rand)

"""for item in range(len(relacionados)):
                    
                    
    aver = relacionados[item]
    if aver[0] == SigPal:

        tupli = (SigPal,aver[1] + 1)
        aux.append(tupli)
                        

    else:
                        
        aux.append(aver)

relacionados = aux
print(aux)"""
"""aux = []
    cadena = frase.split()
        
    for palabra in range(len(cadena)):

        Pal = cadena[palabra]

        dicc[Pal] = dicc.get(Pal,(0,[]))

        

        if palabra == len(cadena)-1:

            dicc[Pal] = (dicc.get(Pal)[0] + 1,dicc.get(Pal)[1])
            break

        else:
            
            SigPal = cadena[palabra + 1]
            
            if len(dicc.get(Pal)[1]) == 0:

                dicc[Pal] = (dicc.get(Pal)[0] + 1,[(SigPal,1)])

            else:
                
                relacionados = dicc.get(Pal)[1]
                
                aux =[]
                yaexistia = False
                for item in range(len(relacionados)):
                    
                    
                    aver = relacionados[item]
                    if aver[0] == SigPal:

                        yaexistia = True
                        tupli = (SigPal,aver[1] + 1)
                        aux.append(tupli)
                        

                    else:
                        
                        aux.append(aver)
                    
                if yaexistia == False:

                    aux.append((SigPal,1))
                    
                
                dicc[Pal] = (dicc.get(Pal)[0] + 1,aux)

            
            
        
            
    return(dicc)"""