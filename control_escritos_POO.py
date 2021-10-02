from clases.py import *
escrito1 = Escrito(9996762, "123456/21", "FERVETTO", "12/06/2021", "PRUEBA", "Katz")
expediente1 = Expediente("1/21", "fervetto c/ sql", "fervetto")
pase1 = Pase(1, "fervetto", "alfonzo", "30/7/21", "PASE A MESA", "PRUEBA")
print(escrito1)
Escrito.objects.insert(escrito1)
Expediente.objects.insert(expediente1)
Pase.objects.insert(pase1)