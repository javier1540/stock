import sqlite3

class Crear_base:
    def __init__(self):
        self.conexion = sqlite3.connect("base_lobo_uniformes.db")
        self.cursor = self.conexion.cursor()

        self.conexion.execute("""CREATE TABLE IF NOT EXISTS Instituciones(
                                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                                nombre  TEXT UNIQUE
        )""")

        self.conexion.execute("""CREATE TABLE IF NOT EXISTS Talles (
                                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                                nombre  TEXT UNIQUE NOT NULL
        )""")

        self.conexion.execute("""CREATE TABLE IF NOT EXISTS Productos(
                                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                                nombre      TEXT
                                
        )""")
        #### ARTICULOS ####
        self.conexion.execute("""CREATE TABLE IF NOT EXISTS Articulos(
                                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                                institucion_id  INTEGER NOT NULL,
                                producto_id     INTEGER NOT NULL,
                                precio          INTEGER,
                                
                                FOREIGN KEY (institucion_id) REFERENCES Instituciones(id) ON DELETE CASCADE ON UPDATE CASCADE,
                                FOREIGN KEY (producto_id) REFERENCES Productos(id) ON DELETE CASCADE ON UPDATE CASCADE
        )""")
        ### STOCK ####
        self.conexion.execute("""CREATE TABLE IF NOT EXISTS STOCK (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    institucion VARCHAR (100),
                    Tipo VARCHAR (100),
                    Talle_id INTEGER,
                    cantidad INTEGER,
                    Precio FLOAT,
                    FOREIGN KEY (Talle_id) REFERENCES talles(id)
                    )""")
        self.conexion.commit()


class Instituciones:
    def __init__(self):
        self.conexion = sqlite3.connect("base_lobo_uniformes.db")
        self.cursor = self.conexion.cursor()

    def agregar(self,institucion):
        try:
            self.conexion.execute("""INSERT INTO Instituciones VALUES (null,'{}')""".format(institucion))
            self.conexion.commit()
        except:
            print("ya se agrego")

    def ver(self):
        self.cursor.execute("""SELECT * FROM Instituciones ORDER BY nombre ASC""")
        registros = self.cursor.fetchall()
        lista = []
        for registro in registros:
            lista.append(registro)
        return lista

    def actualizar(self,nombre,nuevo_nombre):
        id = self.cursor.execute("""SELECT id FROM Instituciones WHERE nombre = '{}'""".format(nombre)).fetchone()
        self.cursor.execute("""UPDATE Instituciones SET nombre = '{}' WHERE id = '{}'""".format(nuevo_nombre,id[0]))
        self.conexion.commit()

    def borrar(self,nombre):
        id = self.cursor.execute("""SELECT id FROM Instituciones WHERE nombre = '{}'""".format(nombre)).fetchone()
        self.cursor.execute("""DELETE FROM Instituciones WHERE id = '{}'""".format(id[0]))
        self.conexion.commit()

class Talles(Crear_base):
    def __init__(self):
        super().__init__()

    def agregar(self,talle):
        try:
            self.cursor.execute("""INSERT INTO Talles VALUES (null,'{}')""".format(talle))
            self.conexion.commit()
        except:
            print("ya se inserto el talle ")

    def actualizar(self,nombre_viejo,nombre_nuevo):
        self.cursor.execute("""UPDATE Talles SET nombre = '{}' WHERE nombre = '{}' """.format(nombre_nuevo,nombre_viejo))
        self.conexion.commit()

    def eliminar(self,id):
        self.cursor.execute(""" DELETE FROM Talles WHERE id = '{}' """.format(id))
        self.conexion.commit()

    def ver_id(self,nombre):
        self.cursor.execute(""" SELECT id FROM Talles WHERE nombre = '{}' """.format(nombre))
        registro = self.cursor.fetchone()
        return registro[0]
    def ver(self):
        self.cursor.execute("""SELECT * FROM Talles ORDER BY id ASC""")
        registros = []
        for valor in self.cursor.fetchall():
            registros.append(valor[1])
        return registros

class Productos(Crear_base):

    def __init__(self):
        super().__init__()

    def agregar(self,nombre):
        self.cursor.execute("""INSERT INTO Productos VALUES (null,'{}')""".format(nombre))
        self.conexion.commit()
    def actualizar(self,nombre_viejo,nombre_nuevo):
        self.cursor.execute("""UPDATE Productos SET nombre = '{}' WHERE nombre = '{}'""".format(nombre_nuevo,nombre_viejo))
        self.conexion.commit()
    def eliminar(self,producto):
        self.cursor.execute("""DELETE FROM Productos WHERE nombre = '{}'""".format(producto))
        self.conexion.commit()

    def ver(self):
        self.cursor.execute("""SELECT * FROM Productos""")
        registros = self.cursor.fetchall()
        return registros

class Articulos(Crear_base):
    def __init__(self):
        super().__init__()

    def agregar(self,institucion,id_producto,precio):
        ins_id = self.cursor.execute("""SELECT id FROM Instituciones WHERE nombre = '{}'""".format(institucion)).fetchone()[0]
        self.cursor.execute("""INSERT INTO Articulos VALUES (null,'{}','{}','{}')""".format(ins_id,id_producto,precio))
        self.conexion.commit()

    def existe(self,institucion,id_producto):
        try:
            ins_id = self.cursor.execute("""SELECT id FROM Instituciones WHERE nombre = '{}'""".format(institucion)).fetchone()[0]
            valor = self.cursor.execute("""SELECT id FROM Articulos WHERE institucion_id = {} AND producto_id = {}""".format(ins_id,id_producto)).fetchone()[0]
            return True
        except:
            return False
    def ver(self):
        registros = self.cursor.execute("""SELECT * FROM Articulos""").fetchall()
        lista = []
        for registro in registros:
            lista.append(registro)
        return lista
    def ver_instituciones(self):
        registros = self.cursor.execute("""SELECT I.nombre FROM Articulos A JOIN Instituciones I ON A.institucion_id = I.id""").fetchall()
        instituciones = []
        for valor in registros:
            if valor[0] not in instituciones:
                instituciones.append(valor[0])
        return instituciones
    def ver_productos_de(self,institucion):
        registros = self.cursor.execute("""SELECT P.nombre FROM Articulos A JOIN Productos P ON A.producto_id = P.id 
                                           WHERE A.institucion_id = (SELECT id FROM Instituciones WHERE nombre = '{}')""".format(institucion)).fetchall()
        productos = []
        for valor in registros:
            if valor[0] not in productos:
                productos.append(valor[0])
        return productos
    

b = Crear_base()

