##!/usr/bin/env python3
import csv
import re
import os
from datetime import datetime
formato1='%d/%m/%Y %H:%M' #formato de fechas1
formato2='%d/%m/%Y'          #formato de fechas2
proveyentes=["DOWNIE, Laura Catalina", "IBARRA, Jorge Carlos Ariel", "MORILLA, Maria Jose", 
"BLOCH PEDERSEN, Cristian", "CHILISSI RACIG, Judith", "COLUSSI MATTAR, Fabiola", "Barrios, Fernando Ariel"] #listado de proveyentes
funcionarios=["LUGON, Carlos Dardo", "FARIAS, Adrian Fernando Alberto", "BENITEZ, Carola Romina", "TORRESAGASTI, Marcelo Sebastian"] #listado de funcionarios
mesa_de_entradas=["ALFONZO, Mirta", "CHORVAT, Enrique Eduardo", "ERVETTO, Fernando Manuel", "SOLOAGA, Roberto Javier"] #listado de personal de mesa de entradas
firmado=False # Variable booleana, si esta proveido y firmado es True
pasado=False #Variable booleana, si tiene una salida de letra es True
proveidos_controlados=[]

#función que recibe como parametros un archivo csv y sus headers y retorna una lista de diccionarios donde cada
# fila del csv es un elemento de la lista y cada key identifica las columnas
def importarFiles(file, headers): 
    result=[]
    with open (file) as arch:
        reader=csv.DictReader(arch, fieldnames=headers, delimiter=";")
        for row in reader:
            result.append(row)
    return result

def contarEscritos(lista_ESCRITOS, lista_controlada):
    expediente_contado={}
    with open ("Cantidad de escritos por expediente.csv", "w", newline="") as salida:
        keys="Nro", "Caratula", "Proveyente", "Cantidad Escritos", "Cantidad Proveidos"
        writer=csv.DictWriter(salida, fieldnames=keys, delimiter=";")
        writer.writeheader()
        for expediente in lista_controlada:
            expediente_contado["Cantidad Escritos"]=0
            for escrito in lista_ESCRITOS:
                if expediente["Nro"] == escrito["Nro"]:
                    expediente_contado["Cantidad Escritos"]= expediente_contado["Cantidad Escritos"] + 1
            expediente_contado["Nro"]=expediente["Nro"]
            expediente_contado["Caratula"] = expediente["Caratula"]
            expediente_contado["Proveyente"] = expediente["Proveyente"]
            expediente_contado["Cantidad Proveidos"] = 11
            writer.writerow(expediente_contado)



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
    with open ("Cantidad de proveidos en ejecuciones.csv", "w", newline="") as salida:
        Keys="Nro", "Caratula", "Proveyente", "Cantidad Proveidos"
        writer=csv.DictWriter(salida, fieldnames=Keys, delimiter=";")
        writer.writeheader()
        antiguo = datetime.strptime("01/01/3021", formato2) 
        nuevo = datetime.strptime("01/01/1021", formato2) 
        for escrito in lista_ESCRITOS:
            expte_controlado["Cantidad Proveidos"]=0 
            encontrado = False
            for proveido in lista_PROVEIDOS:   
                if datetime.strptime(escrito["Fecha de Presentacion"], formato2) > datetime.strptime(proveido["Fecha"], formato1) or proveido["Responsable"]=="ALFONZO, Mirta":
                    continue
                if proveido["Nro"] == convertir_numero_nvo(escrito["Nro"]):
                    expte_controlado["Cantidad Proveidos"]=expte_controlado["Cantidad Proveidos"]+1
                    if antiguo > datetime.strptime(proveido["Fecha"], formato1):
                        antiguo =  datetime.strptime(proveido["Fecha"], formato1)
                    elif nuevo < datetime.strptime(proveido["Fecha"], formato1):
                        nuevo = datetime.strptime(proveido["Fecha"], formato1)
            for pase in lista_PASES:
                if convertir_numero_nvo(escrito["Nro"]) == pase["Nro"]:
                    expte_controlado["Nro"]=pase["Nro"]  
                    expte_controlado["Caratula"]= pase["Caratula"]
                    expte_controlado["Proveyente"]=escrito["Responsable"]                                    
                    break
            if "EJECUCION" in expte_controlado["Caratula"] and pase["Nro"] not in proveidos_controlados:
                writer.writerow(expte_controlado)
                proveidos_controlados.append(pase["Nro"])
            os.system ("cls")
            print("Sistema cuenta proveidos")
            print(f'{lista_ESCRITOS.index(escrito)+1} escritos procesados de:{len(lista_ESCRITOS)}')
        return(lista_controlada, antiguo, nuevo)

cabeceras_ESCRITOS = ["", "Nro", "Responsable", "Fecha de Presentacion", "Tipo Escrito", "Profesional", "Documento", "Adj1", "Adj2", "Adj3", "Adj4", "Visto INDI", "Contestar"]
cabeceras_PROVEIDOS=["Nro", "Fecha", "Responsable", "Descripcion Escrito"]
cabeceras_SALIDA=["Nro", "Caratula", "Envia", "Responsable", "Fecha", "", "", "Tipo", "Observacion"]
lista_ESCRITOS= importarFiles("grid_dbo_vConsultaEscritosIndiDiarios.csv", cabeceras_ESCRITOS)
lista_PROVEIDOS= importarFiles("grid_dbo_vConsultaProveidosFirmadosTodos.csv", cabeceras_PROVEIDOS)
lista_PASES= importarFiles("grid_dbo_vConsultaSalidasLetrasGrid.csv", cabeceras_SALIDA )

lista_ctrl, antiguo, nuevo =controlar_escritos(lista_ESCRITOS, lista_PROVEIDOS, lista_PASES)
print(f'entre {antiguo} y {nuevo}')
print("proceso finalizado con exito")
print("Presione una tecla cualquiera para continuar")
input()


cabeceras_ESCRITOS_CONTADOS = ["Nro", "Caratula", "Proveyente", "Cantidad de Escritos", "Cantidad Proveidos"]
lista_ESCRITOS_CONTADOS = importarFiles("Cantidad de proveidos en ejecuciones.csv", cabeceras_ESCRITOS_CONTADOS)
Lista_salida = contarEscritos(lista_ESCRITOS, lista_ESCRITOS_CONTADOS)

print("Presione una tecla cualquiera para salir")

input()
