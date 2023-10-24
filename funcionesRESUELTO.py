from xml.dom.minidom import Element
from principal import *
from configuracion import *
import random
#lista abecedario
abecedario=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l','m', 'n','ñ', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
#lee el archivo y carga en la lista diccionario todas las palabras
def lectura(diccionario):
    f = open("lemario.txt")
    datos =f.readlines()
    f.close()
    for elemento in datos:
        if len(elemento)>2 and len(elemento)<9:
            diccionario.append(elemento[:-1])
    return diccionario

#Devuelve una cadena de 7 caracteres sin repetir con 2 o 3 vocales y a lo sumo
# con una consonante dificil (kxyz)
def dame7Letras():
    vocales=["a","e","i","o","u"]
    letrasEnPantalla=""
    i=0
    consonante=["k","x","y","z"]
    while i<3:
            elemento=random.choice(vocales)
            if elemento not in letrasEnPantalla:
                letrasEnPantalla=letrasEnPantalla+elemento
                i=i+1
    letrasEnPantalla=letrasEnPantalla+random.choice(consonante)
    i=0
    while i<4:
        elemento=random.choice(abecedario)
        if elemento not in letrasEnPantalla:
            letrasEnPantalla=letrasEnPantalla+elemento    
            i=i+1
    return letrasEnPantalla

def dameLetra(letrasEnPantalla): #elige una letra de las letras en pantalla
    return random.choice(letrasEnPantalla)

#si es valida la palabra devuelve puntos sino resta.
def procesar(letraPrincipal, letrasEnPantalla, candidata, diccionario):
    if esValida(letraPrincipal,letrasEnPantalla,candidata,diccionario):
        return Puntos(candidata,letraPrincipal, letrasEnPantalla,diccionario)
    else:
        return Puntos(candidata,letraPrincipal, letrasEnPantalla,diccionario)
#busca en el diccionario paralabras correctas y devuelve una lista de estas
def dameAlgunasCorrectas(letraPrincipal, letrasEnPantalla, diccionario):
    lista=[]
    letras=list(letrasEnPantalla)
    for elemento in diccionario:
        if len(elemento) > 2:
            if elemento[0]==letraPrincipal:
                cadena=""
                for letra in elemento:
                    if letra in letras:
                        cadena = cadena + letra
                if cadena == elemento:
                    lista.append(cadena)
    return lista
#chequea que se use la letra principal, solo use letras de la pantalla y
#exista en el diccionario
def esValida( candidata, letraPrincipal, letrasEnPantalla, diccionario):
    lista=dameAlgunasCorrectas(letraPrincipal,letrasEnPantalla,diccionario)
    if candidata!="":
        for elemento in lista:
            if candidata[0]==letraPrincipal:
                if candidata==elemento:
                    return True
#devuelve los puntos
def Puntos(candidata, letraPrincipal, letrasEnPantalla, diccionario):
    if esValida(candidata,letraPrincipal, letrasEnPantalla,diccionario):
        if len(candidata) == 3:
            return 1
        elif len(candidata) == 4:
            return 2
        elif len(candidata) == 5:
            return 5
        elif len(candidata) == 6:
            return 6
        elif len(candidata) == 7:
            return 10
    else:
        return -1