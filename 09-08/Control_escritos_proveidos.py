##!/usr/bin/env python3
import csv
import re
import os
from datetime import datetime
import pandas as pd

os.chdir("C:\\controlDeEscritos")
os.getcwd()

formato1='%d/%m/%Y %H:%M:%S' #formato de fechas1
formato2='%d/%m/%Y'          #formato de fechas2
formato3='%d/%m/%Y %H:%M' #formato de fechas3
proveyentes=["DOWNIE, Laura Catalina", "MORILLA, Maria Jose", 
"BLOCH PEDERSEN, Cristian", "CHILISSI RACIG, Judith", "COLUSSI MATTAR, Fabiola", "Barrios, Fernando Ariel", "CHORVAT, Enrique Eduardo"] #listado de proveyentes
funcionarios=["IBARRA, Jorge Carlos Ariel", "LUGON, Carlos Dardo", "FARIAS, Adrian Fernando Alberto", "BENITEZ, Carola Romina", "TORRESAGASTI, Marcelo Sebastian"] #listado de funcionarios
mesa_de_entradas=["ALFONZO, Mirta", "ERVETTO, Fernando Manuel", "SOLOAGA, Roberto Javier"]  #listado de personal de mesa de entradas
firmado=False # Variable booleana, si esta proveido y firmado es True
pasado=False #Variable booleana, si tiene una salida de letra es True


#función que recibe como parametros un archivo csv y sus headers y retorna una lista de diccionarios donde cada
# fila del csv es un elemento de la lista y cada key identifica las columnas
def importarFiles(file, headers): 
    result=[]
    with open (file, encoding="utf8", errors="ignore") as arch:
        reader=csv.DictReader(arch, fieldnames=headers, delimiter=";")
        for row in reader:
            result.append(row)
    return result

#función que recibe como parametro un número de expediente en cualquier formato, con carácteres invalidos
# y retorna un número de expediente valido
def numero_valido(expte):
    regex= r"([\d]+).*([\d]{2})"
    result= re.search (regex, expte)
    return result[1]+"/"+result[2]

#Función que convierte un número de expediente en formato "NNNN/AA" a formato "NNNN/AAAA-1-C"
def convertir_numero_nvo(expte):
    expte= numero_valido(expte)
    regex= r"^([\d]+)/([\d]{2})"
    año= int(re.sub (regex, r"\2", expte))
    numero= re.sub (regex, r"\1", expte)
    if año <= 60: 
        result = re.sub (regex, r"\1/20\2-1-C", expte)
    else:
        result = re.sub (regex, r"\1/19\2-1-C", expte)
    return result

#Función que recibe como parametros la lista de escritos ingresados, lista de proveidos y lista de salidas de letra
# y devuelve un archivo csv con los escritos controlados
def controlar_escritos(lista_ESCRITOS, lista_PROVEIDOS, lista_PASES):
    lista_controlada=[]
    expte_controlado={}
    with open ("ESCRITOS CONTROLADOS CON FECHA DE PROVEIDOS.csv", "w", newline="", encoding="utf-8") as salida:
        Keys="Nro", "Proveyente", "Fecha de Presentacion", "Fecha Proveido", "Firmado por", "Interviene", "Profesional", "Tipo de Escrito", "Titulo del proveido"
        writer=csv.DictWriter(salida, fieldnames=Keys, delimiter=";")
        writer.writeheader()
        for escrito in lista_ESCRITOS:
            firmado=False
            for proveido in lista_PROVEIDOS:      
                try:
                    if datetime.strptime(escrito["Fecha de Presentacion"], formato2) > datetime.strptime(proveido["Fecha"], formato1) or proveido["Responsable"]=="ALFONZO, Mirta":
                        continue
                except:
                    if datetime.strptime(escrito["Fecha de Presentacion"], formato2) > datetime.strptime(proveido["Fecha"], formato3) or proveido["Responsable"]=="ALFONZO, Mirta":
                        continue
                if proveido["Nro"] == convertir_numero_nvo(escrito["Nro"]) and not firmado:
                    firmado=True
                    expte_controlado["Fecha Proveido"]=proveido["Fecha"]
                    expte_controlado["Interviene"]="PROVEIDO"
                    expte_controlado["Firmado por"]=proveido["Responsable"]
                    expte_controlado["Titulo del proveido"]=proveido["Descripcion Escrito"]                    
                    break
            if not firmado:
                pasado=False
                expte_controlado["Firmado por"]= "SIN FIRMA"
                for pase in lista_PASES:
                    if pase["Envia"] in mesa_de_entradas:
                        continue
                    if pase["Nro"] == convertir_numero_nvo(escrito["Nro"]) and datetime.strptime(escrito["Fecha de Presentacion"], formato2) < datetime.strptime(pase["Fecha"], formato2):
                        pasado= True
                        expte_controlado["Titulo del proveido"]=pase["Observacion"]
                        expte_controlado["Interviene"]=pase["Responsable"]      
                        if (pase["Responsable"] in funcionarios):                      
                            expte_controlado["Fecha Proveido"]="Pasado para firma "+pase["Fecha"]     
                        elif pase["Responsable"] in proveyentes and pase["Envia"] in funcionarios:
                            expte_controlado["Fecha Proveido"]="Corregido el "+ pase["Fecha"]   
                        elif pase["Responsable"]=="ALFONZO, Mirta":
                            expte_controlado["Firmado por"]="ALFONZO, Mirta"
                            expte_controlado["Interviene"]="PROVEIDO (Agregue)"   
                            expte_controlado["Fecha Proveido"]="Pasado para firma "+pase["Fecha"]            
                        break
            if not firmado and not pasado:
                expte_controlado["Fecha Proveido"]="ESCRITO SIN PROVEER"
                expte_controlado["Titulo del proveido"]=""
                expte_controlado["Interviene"]=escrito["Responsable"]
            expte_controlado["Nro"]=convertir_numero_nvo(escrito["Nro"])            
            if escrito["Responsable"] in proveyentes:
                expte_controlado["Proveyente"]=escrito["Responsable"]   
            elif escrito["Responsable"]=="":
                expte_controlado["Proveyente"]="ESCRITO MAL INGRESADO"
            else:
                expte_controlado["Proveyente"]="PARA REASIGNAR"
            expte_controlado["Fecha de Presentacion"]=escrito["Fecha de Presentacion"]
            expte_controlado["Profesional"]=escrito["Profesional"]
            expte_controlado["Tipo de Escrito"]=escrito["Tipo Escrito"]

            writer.writerow(expte_controlado)
            os.system ("cls")
            print("Sistema de Control de Escritos")
            print(lista_ESCRITOS.index(escrito)+1, " escritos procesados de:", len(lista_ESCRITOS))
        return(lista_controlada)

cabeceras_ESCRITOS = ["", "Nro", "Responsable", "Fecha de Presentacion", "Tipo Escrito", "Profesional", "Documento", "Adj1", "Adj2", "Adj3", "Adj4", "Visto INDI", "Contestar"]
cabeceras_PROVEIDOS=["Nro", "Fecha", "Responsable", "Descripcion Escrito"]
cabeceras_SALIDA=["Nro", "Caratula", "Envia", "Responsable", "Fecha", "", "", "Tipo", "Observacion"]

pd.read_excel("grid_dbo_vConsultaProveidosFirmadosTodos.xlsx").to_csv('grid_dbo_vConsultaProveidosFirmadosTodos.csv', encoding="utf-8" ,header=False, index=False, sep=";")

try:
    lista_ESCRITOS= importarFiles("grid_dbo_vConsultaEscritosIndiDiariosSinArchivos.csv", cabeceras_ESCRITOS)
    lista_PROVEIDOS= importarFiles('grid_dbo_vConsultaProveidosFirmadosTodos.csv', cabeceras_PROVEIDOS)
    lista_PASES= importarFiles("grid_dbo_vConsultaSalidasLetrasGrid.csv", cabeceras_SALIDA )
except FileNotFoundError:
    print("Archivo No Encotrado")
except:
    print("Error desconocido")    

try:
    controlar_escritos(lista_ESCRITOS, lista_PROVEIDOS, lista_PASES)
except PermissionError:
    print("Archivo de salida bloqueado")

print("proceso finalizado con exito")
print("Presione una tecla cualquiera para salir")
input()

