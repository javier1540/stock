import sqlite3


class Base:
    def __init__(self):
        self.conexion = sqlite3.connect("stock.db")
        self.cursor = self.conexion.cursor()
        try:
            self.cursor.execute("""CREATE TABLE STOCK (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            institucion VARCHAR (100),
            Tipo VARCHAR (100),
            Talle VARCHAR (10),
            cantidad INTEGER,
            Precio FLOAT
            )""")
        except sqlite3.OperationalError:
            print("tabla creada")

    def agregar_dato(self,id=0,inst=None,talle=None,precio=None):
        self.id = id
        self.inst = inst
        self.talle = talle
        self.precio = precio

        self.cursor.execute("SELECT * FROM STOCK WHERE id={}".format(self.id))
        seleccion = self.cursor.fetchone()
        if seleccion == None:
            pass
        else:
            return seleccion[1]

    def ver_instituciones(self):
        self.cursor.execute("SELECT institucion FROM STOCK")
        registros = self.cursor.fetchall()
        conjunto = set()
        for registro in registros:
            conjunto.add(registro[0])
        return conjunto

    def ver_tipos_de(self,institucion):
        self.cursor.execute("SELECT Tipo FROM STOCK WHERE institucion='{}'".format(institucion))
        registros = self.cursor.fetchall()
        conjunto = set()
        for registro in registros:
            conjunto.add(registro[0])
        return conjunto

    def ver_articulos(self,institucion,tipo):
        self.cursor.execute("SELECT * FROM STOCK WHERE institucion='{}' AND Tipo='{}'".format(institucion,tipo))
        registros = self.cursor.fetchall()
        return registros

b = Base()
print(b.ver_articulos("Tecnico","chomba"))
