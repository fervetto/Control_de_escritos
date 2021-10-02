import csv
import re
import collections
import openpyxl

def importarFiles(file):
    result=[]
    wb=openpyxl.load_workbook(file)
    ws =wb.get_sheet_by_name("Worksheet")
    
    result= collections.defaultdict(dict)
    for row in ws.iter_rows():
      result[row[0].value].append(row[1].value)
    return result
    

def numero_valido(expte):
    regex= r"([\d]+).*([\d]{2})"
    result= re.search (regex, expte)
    return result[1]+"/"+result[2]

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


def controlar_escritos(lista_IURE, lista_INDI):
    lista_controlada=[]
    expte_controlado={}
    cont=0
    with open ("lista_salida.csv", "w") as salida:
        Keys="Nro", "Proveyente","Tipo de Escrito", "Profesional", "Fecha de Presentacion"
        writer=csv.DictWriter(salida, fieldnames=Keys)
        writer.writeheader()
        for expte in lista_IURE:
            for escrito in lista_INDI:      
                if expte["NÂº Expediente"] == convertir_numero_nvo(escrito["Exp"]):
                    expte_controlado["Nro"]=expte["NÂº Expediente"]
                    if expte["Responsable"]=="DOWNIE, Laura Catalina":
                        expte_controlado["Proveyente"]="LD"
                    elif expte["Responsable"]=="IBARRA, Jorge Carlos Ariel":
                        expte_controlado["Proveyente"]="AR"
                    elif expte["Responsable"]=="MORILLA, Maria Jose":
                        expte_controlado["Proveyente"]="MJ"
                    elif expte["Responsable"]=="BLOCH PEDERSEN, Cristian":
                        expte_controlado["Proveyente"]="CBP"
                    elif expte["Responsable"]=="CHILISSI RACIG, Judith":
                        expte_controlado["Proveyente"]="JCR"
                    elif expte["Responsable"]=="COLUSSI MATTAR, Fabiola":
                        expte_controlado["Proveyente"]="FCM"              
                    elif expte["Responsable"]=="Barrios, Fernando Ariel":
                        expte_controlado["Proveyente"]="FAB"                   
                    else:
                        expte_controlado["Proveyente"]="REASIGNAR"
                    #print(lista_controlada)
                    expte_controlado["Tipo de Escrito"]=expte["Tipo Escrito"]
                    expte_controlado["Profesional"]=expte["Profesional"]
                    expte_controlado["Fecha de Presentacion"]=escrito["Fecha Presentacion"]
                    writer.writerow(expte_controlado)
                    lista_INDI.remove(escrito)
                    break
                    #lista_controlada.append(expte_controlado)
                    #print(expte["Nro"], "|", escrito["Nro"])
        for escrito in lista_INDI:
            expte_controlado["Nro"]=convertir_numero_nvo(escrito["Exp"])
            expte_controlado["Proveyente"]="NO INGRESADO!"
            expte_controlado["Profesional"]=escrito["Documento"]
            writer.writerow(expte_controlado)


        return(lista_controlada)

lista_IURE= importarFiles("grid_dbo_vConsultaEscritosIndiDiarios.xlsx")
lista_INDI= importarFiles("grid_dbo_LDPROF_Escritos_5.xls")

lista_ctrl=controlar_escritos(lista_IURE, lista_INDI)
print("proceso finalizado con exito")
