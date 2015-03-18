#!/usr/bin/python
# -*- coding: utf-8 -*-
####################################################################################
# File Name  : lineas_mayores.py
# Author     : David Bojart
# Date       : 20150305
# Update     : Thu 05 Mar 2015 05:19:27 PM CET
# Explanation: Busca en todos los ficheros de un directorio, las lineas que
#              contegan a partir del caracter que se le indique si tiene un maximo
#              de caracteres indicado en la variable "longuitud"
# Update by  :
####################################################################################
import os

## Variables
ruta = "/tu/ruta"
lista = os.listdir(ruta) # realiza un listado de la ruta
longitud = 64 # numero maximo de caracteres.
##

for fichero in lista:
  infile = open(ruta+fichero, 'r')
  contador = 0
  for line in infile:
      cadena = (line[47:]) # caracter en el que empieza a contar.
      contador = contador+1
      if len(cadena) >= longitud:
        print ("En "+ fichero +" la linea "+ str(contador) +" es mayor de 64")
        print("Contiene: "+ str(len(cadena)) + " caracteres\n")
  infile.close()
