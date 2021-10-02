import sqlite3
from sqlite3.dbapi2 import TimestampFromTicks, register_converter
DB_PATH ='prueba.db'
class EscritosManager(object):
    def __init__ (self, database=None):
        if not database:
            database = ':memory:'
        self.conn = sqlite3.connect(database)  #conecta a una base de datos
        self.cursor =self.conn.cursor()        # crea objeto cursor

    def insert(self, Escrito):
        query = 'INSERT INTO Escritos VALUES ("{}", "{}", "{}","{}", "{}", "{}")'.format(Escrito.id, Escrito.numero, Escrito.responsable, Escrito.fecha_ingreso, Escrito.tipo, Escrito.profesional)
        self.cursor.execute(query)             # Ejecuta una consulta
        self.conn.commit()                     # Confirma los cambios

class ExpedientesManager(object):
    def __init__ (self, database=None):
        if not database:
            database = ':memory:'
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()

    def insert(self, Expediente):
        query = 'INSERT INTO expedientes VALUES ("{}", "{}", "{}")'.format(Expediente.numero, Expediente.caratula, Expediente.proveyente)
        self.cursor.execute(query)
        self.conn.commit()

class Expediente(object):
    objects = ExpedientesManager(DB_PATH)
    def __init__(self, numero, caratula, proveyente):
        self.numero = numero
        self.caratula = caratula
        self.proveyente = proveyente

    def __str__(self):
        return f"{self.numero}, {self.caratula}, {self.proveyente}"

class Escrito(object):
    objects = EscritosManager(DB_PATH)
    def __init__(self, id, numero, responsable, fecha_ingreso, tipo, profesional):
        self.id = id
        self.numero = numero
        self.responsable = responsable
        self.fecha_ingreso = fecha_ingreso
        self.tipo=tipo
        self.profesional = profesional
    def __str__(self):
        return f"{self.id}, {self.numero}, {self.responsable}, {self.fecha_ingreso}, {self.profesional}"

class PasesManager(object):
    def __init__ (self, database=None):
        if not database:
            database = ':memory:'
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()

    def insert(self, Pase):
        query = 'INSERT INTO pases VALUES ("{}", "{}", "{}", "{}", "{}", "{}")'.format(Pase.id, Pase.envia, Pase.recive, Pase.fecha, Pase.tipo, Pase.observacion)

class Pase(object):
    objects = PasesManager(DB_PATH)
    def __init__(self, id, envia, recive, fecha, tipo, observacion):
        self.id = id
        self.envia = envia
        self.recive = recive
        self.fecha = fecha
        self.tipo = tipo
        self.observacion = observacion


escrito1 = Escrito(99999, "123456/21", "FERVETTO", "12/06/2021", "PRUEBA", "Katz")
expediente1 = Expediente("4/21", "fervetto c/ sql", "fervetto")
pase1 = Pase(1, "fervetto", "alfonzo", "30/7/21", "PASE A MESA", "PRUEBA")
print(escrito1)
Escrito.objects.insert(escrito1)
Expediente.objects.insert(expediente1)
Pase.objects.insert(pase1)