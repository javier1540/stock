import sqlite3


class Base:
    def __init__(self):
        self.conexion = sqlite3.connect("stock.db")
        self.cursor = self.conexion.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS talles(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        talle TEXT
                        )""")



        self.cursor.execute("""CREATE TABLE IF NOT EXISTS STOCK (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    institucion VARCHAR (100),
                    Tipo VARCHAR (100),
                    Talle_id INTEGER,
                    cantidad INTEGER,
                    Precio INTEGER,
                    FOREIGN KEY (Talle_id) REFERENCES talles(id)
                    )""")


    def modificar_dato(self,inst=None,tipo=None,talle=None,cant=0,precio=0,agregar=False,quitar=False):
        self.inst = inst
        self.tipo = tipo
        self.talle = self.cursor.execute("SELECT id FROM talles WHERE talle = '{}'".format(talle)).fetchone()
        self.talle = self.talle[0]
        self.cantidad = int(cant)
        self.precio = precio
        agregar = agregar
        quitar = quitar

        self.cursor.execute("""SELECT id FROM STOCK WHERE institucion='{}'AND tipo='{}' AND talle_id='{}'""".format(self.inst,self.tipo,self.talle))
        seleccion = self.cursor.fetchone()

        if seleccion != None: # si se encuentra el id seleccionado entonces se actualiza la info
            print("se actualiza la info")
            # sumar cantidad
            if agregar:
                print("se suma")
                id = seleccion[0]
                self.cursor.execute("""UPDATE STOCK SET cantidad = cantidad + '{}',precio = '{}' WHERE id = '{}'""".format(self.cantidad,self.precio,id))
                self.conexion.commit()
            elif quitar:
                print("se resta")
                id = seleccion[0]
                cantidad = self.cursor.execute("""SELECT cantidad FROM STOCK WHERE id='{}'""".format(id)).fetchone()
                cantidad_a_restar = self.cantidad
                operacion = max(0,(cantidad[0]-cantidad_a_restar))
                self.cursor.execute("""UPDATE STOCK SET cantidad ='{}' WHERE id = '{}'""".format(operacion,id))
                self.conexion.commit()
        else: # Si no encuentra el id seleccionado se crea uno
            print("se crea la info ")
            self.cursor.execute("""INSERT INTO STOCK VALUES(null,'{}','{}','{}',{},{})""".format(self.inst,self.tipo,self.talle,self.cantidad,self.precio))
            self.conexion.commit()

    def eliminar_dato(self,institucion,tipo,talle):
        self.cursor.execute("""DELETE FROM STOCK WHERE institucion = '{}' AND Tipo = '{}' AND Talle_id = (SELECT id FROM talles WHERE talle = '{}')""".format(institucion,tipo,talle))
        self.conexion.commit()


    def ver_talles_de(self,producto,institucion):
        if len(institucion) != 0:
            registros = self.cursor.execute("""SELECT STOCK.Tipo,talles.talle FROM STOCK JOIN talles ON STOCK.Talle_id = talles.id 
                                                WHERE institucion = '{}' AND Tipo = '{}' ORDER BY talles.id ASC""".format(institucion,producto)).fetchall()
            lista = []
            for valores in registros:
                if valores[1] not in lista:
                    lista.append(valores[1])
            return lista
        else:
            registros = self.cursor.execute("""SELECT STOCK.Tipo,talles.talle FROM STOCK JOIN talles ON STOCK.Talle_id = talles.id 
                                    WHERE Tipo = '{}' ORDER BY talles.id ASC""".format(producto)).fetchall()
            lista = []
            for valores in registros:
                if valores[1] not in lista:
                    lista.append(valores[1])
            return lista
    def ver_talles(self):
        self.cursor.execute("SELECT talle FROM talles ORDER BY id ASC")
        registros = self.cursor.fetchall()
        lista = []
        for registro in registros:
            lista.append(registro[0])
        return lista
    def agregar(self,talle):
        try:
            self.cursor.execute("""INSERT INTO Talles VALUES (null,'{}')""".format(talle))
            self.conexion.commit()
        except:
            print("ya se inserto el talle ")

    def actualizar(self,nombre_viejo,nombre_nuevo):
        self.cursor.execute("""UPDATE Talles SET talle = '{}' WHERE talle = '{}' """.format(nombre_nuevo,nombre_viejo))
        self.conexion.commit()

    def eliminar(self,id):
        self.cursor.execute(""" DELETE FROM Talles WHERE id = '{}' """.format(id))
        self.conexion.commit()

    def ver_id(self,nombre):
        self.cursor.execute(""" SELECT id FROM Talles WHERE talle = '{}' """.format(nombre))
        registro = self.cursor.fetchone()
        return registro[0]
    def ver(self):
        self.cursor.execute("""SELECT * FROM Talles ORDER BY id ASC""")
        registros = []
        for valor in self.cursor.fetchall():
            registros.append(valor[1])
        return registros


    def ver_instituciones(self):
        self.cursor.execute("SELECT institucion FROM STOCK ORDER BY institucion ASC")
        registros = self.cursor.fetchall()
        lista = []
        for registro in registros:
            if not registro[0] in lista:
                lista.append(registro[0])
        return lista

    def ver_tipos(self):
        registros = self.cursor.execute("""SELECT Tipo FROM STOCK """).fetchall()
        lista = []
        for registro in registros:
            if registro[0] not in lista:
                lista.append(registro[0])
        return lista
    def ver_tipos_de(self,institucion):
        self.cursor.execute("SELECT Tipo FROM STOCK WHERE institucion='{}' ORDER BY Tipo ASC".format(institucion))
        registros = self.cursor.fetchall()
        lista = []
        for registro in registros :
            if not registro[0] in lista:
                lista.append(registro[0])
        return lista

    def ver_articulos(self,institucion,tipo):
        self.cursor.execute("""SELECT STOCK.id,STOCK.institucion,STOCK.Tipo,talles.talle,STOCK.cantidad,STOCK.Precio 
                            FROM STOCK  INNER JOIN talles ON STOCK.Talle_id = talles.id WHERE institucion = '{}' AND tipo = '{}'
                            ORDER BY STOCK.talle_id ASC""".format(institucion,tipo))
        registros = self.cursor.fetchall()
        return registros

    def actualizar_precio(self,producto,talle,precio,institucion):
        if len(institucion) != 0:
            self.cursor.execute("""UPDATE STOCK SET Precio = {} WHERE institucion = '{}' Tipo = '{}' AND Talle_id = (SELECT id FROM talles WHERE talle = '{}')""".format(institucion,precio, producto, talle))
            self.conexion.commit()
        else:
            self.cursor.execute("""UPDATE STOCK SET Precio = {} WHERE Tipo = '{}' AND Talle_id = (SELECT id FROM talles WHERE talle = '{}')""".format(precio,producto,talle))
            self.conexion.commit()
    def ver_precio_de(self,producto,talle):
        registros = self.cursor.execute("""SELECT Precio FROM STOCK WHERE Tipo = '{}' AND Talle_id = (SELECT id FROM talles WHERE talle = '{}')""".format(producto,talle)).fetchall()
        precios = []
        for registro in registros:
            if registro[0] not in precios:
                precios.append(registro[0])
        return precios
#*****************************************
# Cantidades:
class Cantidades_de:
    def __init__(self):
        pass

b = Base()
print(b.ver_precio_de("Chomba","XS"))
