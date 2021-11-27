import re

##función que separa una caratula completa en numero (1) y caratula(2)
def divide_caratula(caratula_completa, n):
    regex= r"^(.+-1-C)...(.+)"
    result=re.search (regex, caratula_completa)
    try:
        return str(result[n])
    except:
        pass

#función que recibe como parametro un número de expediente en cualquier formato, con carácteres invalidos
# y retorna un número de expediente valido (elimina los caracteres invalidos)
def numero_valido(expte):
    regex= r"([\d]+).*([\d]{2})"
    result= re.search (regex, expte)
    return str(result[1]+"/"+result[2])

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

print (divide_caratula("410/2012-1-C - RAMIREZ IRMA ESTER,  BARRETO ENZO NALDO  C/ MUNICIPALIDAD DE RESISTENCIA Y/O EMPRESA DEL PILAR SRL S/ DAÑOS Y PERJUICIOS Y DAÑO MORAL POR ACC. DE TRANSITO", 2))
