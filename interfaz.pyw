import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from stock import *
from conexion import *
from coneccion_a_base import *

class App1(tk.Tk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title("Lobo Uniformes")
        self.geometry("1200x550+50+50")
        base = Base()



        # barra de menu
        self.barra_menus = tk.Menu()

        # MENU CREAR
        self.menu_editar = tk.Menu(self.barra_menus, tearoff=False)

        self.menu_instituciones = tk.Menu(self.barra_menus,tearoff=False)
        self.menu_instituciones.add_command(label="nuevo", command=self.boton_nueva_institucion)
        self.menu_instituciones.add_command(label="editar",command=self.boton_editar_institucion)
        self.menu_editar.add_cascade(menu=self.menu_instituciones,label="Instituciones")

        self.menu_editar.add_command(label="talles",command=self.boton_talles)
        self.menu_editar.add_command(label="Productos",command=self.boton_productos)
        self.menu_editar.add_command(label="Articulos",command=self.boton_articulos)
        self.barra_menus.add_cascade(menu=self.menu_editar, label="Editar")

        # MENU STOCK
        self.menu_stock = tk.Menu(self.barra_menus,tearoff=False)
        self.menu_stock.add_command(label="Cargar",command=self.boton_cargar)
        self.menu_stock.add_command(label="Precios",command=self.boton_precios)
        self.barra_menus.add_cascade(menu=self.menu_stock,label="Stock")


        self.config(menu=self.barra_menus)


        self.libro = ttk.Notebook(self)
        self.pestana_stock = Stock(self.libro)
        self.libro.add(self.pestana_stock,text="Stock")
        self.libro.grid(column=0,row=0,pady=20)

# BOTONES
    def boton_nueva_institucion(self):
        ventana = Ventana_nueva_institucion()
    def boton_editar_institucion(self):
        ventana = Ventana_edit_inst()

    def boton_talles(self):
        ventana = Ventana_talles()
    def boton_productos(self):
        ventana = Ventana_productos()
    def boton_articulos(self):
        ventana = Ventana_articulos()
    def boton_cargar(self):
        ventana = Ventana_cargar()
    def boton_precios(self):
        ventana = Ventana_precio()


############################# VENTANAS DE LA BARRA MENU ############################################


########### INSTITUCIONES ####################
class Ventana_edit_inst(tk.Toplevel):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title("Editar instituciones")
        self.geometry("250x150+500+300")
        self.resizable(0,0)
        self.instituciones = Instituciones()
        self.institucion_selec = ""

        self.labelframe_editar =  ttk.LabelFrame(self,text="Editar")
        self.widgets_editar()
        self.labelframe_editar.grid(column=0,row=0)

        self.lista.focus()
        self.grab_set()

    def widgets_editar(self):
        self.lista = tk.Listbox(self.labelframe_editar,width=15,height=5)
        self.entry = ttk.Entry(self.labelframe_editar,width=10)

        self.botones = ttk.Frame(self.labelframe_editar)
        self.boton_edit = ttk.Button(self.botones, text="Editar", command=self.editar)
        self.boton_borrar = ttk.Button(self.botones, text="Borrar",command=self.borrar)

        self.lista.grid(column=0,row=0,pady=10, padx=10, rowspan=3)
        self.entry.grid(column=1,row=0,pady=10, padx=10)
        self.botones.grid(column=1,row=1)
        self.boton_edit.grid(column=1, row=1, pady=10, padx=10)
        self.boton_borrar.grid(column=1,row=2)

        self.cargar_lista()
        self.lista.bind('<<ListboxSelect>>',self.seleccion)

    def cargar_lista(self):
        self.lista.delete(0, tk.END)
        for n,registro in enumerate(self.instituciones.ver()):
            nombre = registro[1]
            self.lista.insert(n,nombre)
    def seleccion(self,event=None):
        if len(self.lista.curselection()) != 0:
            posicion = self.lista.curselection()[0]
            seleccion = self.lista.get(posicion)
            self.entry.delete(0,tk.END)
            self.entry.insert(0,seleccion)
            self.institucion_selec = seleccion

    def editar(self):
        nombre = self.institucion_selec
        nuevo_nombre = self.entry.get()
        self.instituciones.actualizar(nombre,nuevo_nombre)
        self.entry.delete(0,tk.END)
        self.cargar_lista()
    def borrar(self):
        nombre = self.lista.get(self.lista.curselection()[0])
        self.instituciones.borrar(nombre)
        self.cargar_lista()
        self.entry.delete(0,tk.END)
    def agregar(self):
        institucion = self.entry.get()
        self.instituciones.agregar(institucion)
        self.cargar_lista()

class Ventana_nueva_institucion(tk.Toplevel):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title("Nueva institucion")
        self.geometry("250x150+500+300")
        self.resizable(0,0)
        self.instituciones = Instituciones()

        self.lista = tk.Listbox(self, width=15, height=10,activestyle=tk.NONE,selectbackground="white",selectforeground="black")
        self.frame = ttk.Frame(self)
        self.entry = ttk.Entry(self.frame)
        self.boton = ttk.Button(self.frame, text="Agregar", command=self.agregar)
        self.entry.grid(column=0, row=0, padx=10, pady=5)
        self.boton.grid(column=0, row=1, padx=10, pady=5)
        self.lista.grid(column=0, row=0)
        self.frame.grid(column=1,row=0)

        self.cargar_lista()
        self.entry.focus()
        self.grab_set()
        self.boton.bind_all('<Return>', self.agregar)
    def agregar(self,event=None):
        institucion = self.entry.get()
        if len(institucion) != 0:
            self.instituciones.agregar((institucion).capitalize())
            self.entry.delete(0,tk.END)
            self.cargar_lista()
            self.entry.focus()
    def cargar_lista(self):
        self.lista.delete(0, tk.END)
        for n,registro in enumerate(self.instituciones.ver()):
            nombre = registro[1]
            self.lista.insert(n,nombre)


############# TALLES #############################
class Ventana_talles(tk.Toplevel):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title("Talles")
        self.geometry("280x170+500+300")
        self.resizable(0,0)
        self.focus()
        self.grab_set()
        self.talles = Base()
        self.talle_selec = ""

        self.scroll = tk.Scrollbar(self, orient=tk.VERTICAL)
        self.lista = tk.Listbox(self, width=8, height=10, activestyle=tk.NONE,yscrollcommand=self.scroll.set)
        self.frame_flechas = ttk.Frame(self)
        self.boton_arriba = ttk.Button(self.frame_flechas,text="▲",width=5,command=self.mover_arriba)
        self.boton_abajo = ttk.Button(self.frame_flechas,text="▼",width=5,command=self.mover_abajo)
        self.boton_arriba.grid(column=0,row=0,padx=5)
        self.boton_abajo.grid(column=0,row=1,padx=5)

        self.frame = ttk.Frame(self)
        self.entry = ttk.Entry(self.frame)
        self.boton_n = ttk.Button(self.frame, text="Nuevo", command=self.agregar)
        self.boton_e = ttk.Button(self.frame, text="Editar",command=self.editar)
        self.boton_b = ttk.Button(self.frame,text="Borrar",command=self.borrar)
        self.entry.grid(column=0, row=0, padx=10, pady=5)
        self.boton_n.grid(column=0, row=1, padx=10, pady=5)
        self.boton_e.grid(column=0, row=2, padx=10, pady=5)
        self.boton_b.grid(column=0,row=3,padx=10,pady=5)
        self.lista.grid(column=0, row=0,padx=5)
        self.scroll.configure(command=self.lista.yview)
        self.scroll.grid(column=1, row=0, sticky="NS")
        self.frame_flechas.grid(column=2,row=0)
        self.frame.grid(column=3, row=0)


        self.cargar_lista()
        self.entry.focus()
        self.grab_set()
        self.lista.bind('<<ListboxSelect>>', self.seleccion)
        self.boton_n.bind_all('<Return>', self.agregar)

    def agregar(self, event=None):
        talle = self.entry.get()
        if len(talle) != 0:
            self.talles.agregar(talle)
            self.entry.delete(0, tk.END)
            self.cargar_lista()
            self.entry.focus()

    def cargar_lista(self):
        self.lista.delete(0, tk.END)
        for n, registro in enumerate(self.talles.ver_talles()):
            self.lista.insert(n,registro)
    def seleccion(self,event=None):
        if len(self.lista.curselection()) != 0:
            posicion = self.lista.curselection()[0]
            seleccion = self.lista.get(posicion)
            self.entry.delete(0,tk.END)
            self.entry.insert(0,seleccion)
            self.talle_selec = seleccion
    ######### FUNCION DE BOTONES ###########
    def mover(self,valor):
        if len(self.lista.curselection()) != 0:
            nombre_actual = self.lista.get(self.lista.curselection()[0])
            posicion_nueva = max(0, (self.lista.curselection()[0]) - 1)
            nombre_arriba = self.lista.get(posicion_nueva) # si la posicion alcutal esta ubicada en 0 la posicion arriba sera 0
            self.talles.actualizar(nombre_arriba, "▲" + nombre_actual)
            self.talles.actualizar(nombre_actual, nombre_arriba)
            self.talles.actualizar("▲" + nombre_actual, nombre_actual)
            self.cargar_lista()
            self.lista.selection_set(posicion_nueva)

    def mover_arriba(self):
        if len(self.lista.curselection()) != 0:
            nombre_actual = self.lista.get(self.lista.curselection()[0])
            posicion_arriba = max(0, (self.lista.curselection()[0]) - 1)
            nombre_arriba = self.lista.get(posicion_arriba) # si la posicion alcutal esta ubicada en 0 la posicion arriba sera 0
            self.talles.actualizar(nombre_arriba, "▲" + nombre_actual)
            self.talles.actualizar(nombre_actual, nombre_arriba)
            self.talles.actualizar("▲" + nombre_actual, nombre_actual)
            self.cargar_lista()
            self.lista.selection_set(posicion_arriba)
    def mover_abajo(self):
        if len(self.lista.curselection()) != 0:
            ultimo_valor = self.lista.size()-1 # devuelve la posicion del ultimo valor de la lista
            nombre_actual = self.lista.get(self.lista.curselection()[0])
            posicion_abajo = min(ultimo_valor,(self.lista.curselection()[0]) + 1 )
            nombre_abajo = self.lista.get(posicion_abajo)
            self.talles.actualizar(nombre_abajo,"▼"+nombre_actual)
            self.talles.actualizar(nombre_actual,nombre_abajo)
            self.talles.actualizar("▼"+nombre_actual,nombre_actual)
            self.cargar_lista()
            self.lista.selection_set(posicion_abajo)

    def editar(self):
        nombre = self.talle_selec
        nuevo_nombre = self.entry.get()
        self.talles.actualizar(nombre,nuevo_nombre)
        self.entry.delete(0,tk.END)
        self.cargar_lista()
    def borrar(self):
        if len(self.lista.curselection()) != 0:
            posicion = self.lista.curselection()[0]
            seleccion = self.lista.get(posicion)
            id = self.talles.ver_id(seleccion)
            self.talles.eliminar(id)
            self.entry.delete(0,tk.END)
            self.cargar_lista()


############# PRODUCTOS #######################
class Ventana_productos(tk.Toplevel):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title("Productos")
        self.geometry("400x400+500+300")
        self.focus()
        self.grab_set()
        self.productos = Productos()

        self.labelframe_editar = ttk.LabelFrame(self,text="Editar")
        self.lf_editar()
        self.labelframe_nuevo = ttk.LabelFrame(self,text="Nuevo")
        self.lf_nuevo()
        self.labelframe_editar.grid(column=0, row=0, pady=10, padx=10)
        self.labelframe_nuevo.grid(column=0,row=1,pady=10,padx=10)


    def lf_editar(self):
        frame = ttk.Frame(self.labelframe_editar)
        self.scroll = ttk.Scrollbar(frame,orient=tk.VERTICAL)
        self.lista_pro = tk.Listbox(frame,yscrollcommand=self.scroll.set,width=15,height=5)
        self.scroll.configure(command=self.lista_pro.yview)
        self.lista_pro.grid(column=0, row=0, pady=5, padx=10)
        self.scroll.grid(column=1,row=0,sticky="NS")
        frame.grid(column=0, row=0)

        frame2 = ttk.Frame(self.labelframe_editar)
        self.entry_e = ttk.Entry(frame2,width=13)
        self.boton_e = ttk.Button(frame2,text="Editar",command=self.boton_editar_e)
        self.boton_b = ttk.Button(frame2, text="Borrar", command=self.boton_borrar_e)
        self.entry_e.grid(column=0,row=0,padx=10,pady=5)
        self.boton_e.grid(column=0,row=1,padx=4,pady=5)
        self.boton_b.grid(column=0,row=2,padx=4,pady=20)
        frame2.grid(column=1,row=0)

        self.lista_pro.bind("<<ListboxSelect>>",self.lista_selec)
        self.cargar_lista_pro()

    def boton_editar_e(self):
        if len(self.lista_pro.curselection()) != 0 and len(self.entry_e.get()) != 0 :
            ProductoAEditar = self.lista_pro.get(self.lista_pro.curselection()[0])
            nuevo_nombre = self.entry_e.get().capitalize()
            self.productos.actualizar(ProductoAEditar,nuevo_nombre)
            self.cargar_lista_pro()
            self.entry_e.delete(0,tk.END)
    def boton_borrar_e(self):
        if len(self.lista_pro.curselection()) != 0:
            producto_selec = self.lista_pro.get(self.lista_pro.curselection()[0])
            self.productos.eliminar(producto_selec)
            self.cargar_lista_pro()
    def cargar_lista_pro(self):
        self.lista_pro.delete(0,tk.END)
        productos = []
        for producto in self.productos.ver():
            productos.append(producto[1])
        for n,i in enumerate(productos):
            self.lista_pro.insert(n,i)

    def lista_selec(self,event):
            if len(self.lista_pro.curselection()) != 0:
                producto = self.lista_pro.get(self.lista_pro.curselection()[0])


    def lf_nuevo(self):
        self.frame = tk.Frame(self.labelframe_nuevo)
        self.label_n = ttk.Label(self.frame,text="Nombre")
        self.entry_n = ttk.Entry(self.frame)
        self.boton_n = ttk.Button(self.frame,text="Agregar",command=self.agregar_n)
        self.label_n.grid(column=0,row=0)
        self.entry_n.grid(column=0,row=1)
        self.boton_n.grid(column=0,row=2,pady=10)

        self.frame.grid(column=0,row=0,pady=10,padx=10)
    def agregar_n(self):
        if len(self.entry_n.get())!=0:
            producto = self.entry_n.get().capitalize()
            self.productos.agregar(producto)
            self.cargar_lista_pro()
            self.entry_n.delete(0,tk.END)

######## CARGAR ############################
class Ventana_cargar(tk.Toplevel):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title("Cargar stock")
        self.geometry("450x100+500+300")
        self.focus()
        self.grab_set()
        self.base = Base()
        self.instituciones = Instituciones()
        self.productos = Productos()
        self.talles = Base()
        inst = []
        prod = []
        talles = self.talles.ver()
        for v in self.instituciones.ver():
            inst.append(v[1])
        for v in self.productos.ver():
            prod.append(v[1])

###### widgets ######
        self.l_inst = ttk.Label(self,text="Institucion")
        self.cb_inst = ttk.Combobox(self,width=8,state="readonly",values=inst)
        self.l_prod = ttk.Label(self,text="Producto")
        self.cb_prod = ttk.Combobox(self,width=15,state="disabled",values=prod)
        self.l_talle = ttk.Label(self,text="Talle")
        self.cb_talle = ttk.Combobox(self,width=8,state="disabled",values=talles)
        self.l_prec = ttk.Label(self,text="Precio")
        self.e_prec = ttk.Entry(self,width=8,state="disabled")
        self.b_cargar = ttk.Button(self,text="Cargar",command=self.cargar,state="disabled")

        self.l_inst.grid(column=0,row=0,padx=5)
        self.cb_inst.grid(column=0,row=1,padx=5)
        self.l_prod.grid(column=1,row=0,padx=5)
        self.cb_prod.grid(column=1,row=1,padx=5)
        self.l_talle.grid(column=2,row=0,padx=5)
        self.cb_talle.grid(column=2,row=1,padx=5)
        self.l_prec.grid(column=3,row=0,padx=5)
        self.e_prec.grid(column=3,row=1,padx=5)
        self.b_cargar.grid(column=4,row=1,padx=5)

        self.cb_inst.bind("<<ComboboxSelected>>",self.cb_inst_selec)
        self.cb_prod.bind("<<ComboboxSelected>>",self.cb_prod_selec)
        self.cb_talle.bind("<<ComboboxSelected>>",self.cb_talle_selec)

    def cb_inst_selec(self,event):
        self.cb_prod["state"] = "readonly"
    def cb_prod_selec(self,event):
        self.cb_talle["state"] = "readonly"
    def cb_talle_selec(self,event):
        self.e_prec["state"] = "normal"
        self.b_cargar["state"] = "normal"
        precio = self.base.ver_precio_de(self.cb_prod.get(),self.cb_talle.get())
        self.e_prec.delete(0,tk.END)
        if len(precio) == 1:
            self.e_prec.delete(0,tk.END)
            self.e_prec.insert(0,precio[0])
        elif len(precio) >1:
            self.e_prec.delete(0,tk.END)
            self.e_prec.insert(0,min(precio))

    def cargar(self):
        institucion = self.cb_inst.get()
        tipo = self.cb_prod.get()
        talle = self.cb_talle.get()
        precio = 0
        if len(self.e_prec.get()) !=0:
            if self.e_prec.get().isdigit():
                precio = self.e_prec.get()
        if len(institucion)!=0 and len(tipo)!=0 and len(talle)!=0:
            self.base.modificar_dato(institucion,tipo,talle,0,precio,True)

######### PRECIOS ###################
class Ventana_precio(tk.Toplevel):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title("Editar precios")
        self.geometry("450x100+500+300")
        self.focus()
        self.grab_set()
        self.base = Base()
        self.instituciones = Instituciones()
        self.productos = Productos()
        self.talles = Base()
        inst = []
        self.prod = self.base.ver_tipos()
        talles = self.talles.ver()
        for v in self.instituciones.ver():
            inst.append(v[1])


        ###### widgets ######
        self.l_inst = ttk.Label(self, text="Institucion")
        self.cb_inst = ttk.Combobox(self, width=8, values=inst,postcommand=self.cb_inst_edit)
        self.l_prod = ttk.Label(self, text="Producto")
        self.cb_prod = ttk.Combobox(self, width=15, values=self.prod,postcommand=self.cb_prod_edit)
        self.l_talle = ttk.Label(self, text="Talle")
        self.cb_talle = ttk.Combobox(self, width=8, state="disabled", values=talles)
        self.l_prec = ttk.Label(self, text="Precio")
        self.e_prec = ttk.Entry(self, width=8,state="disabled")
        self.b_actualizar = ttk.Button(self, text="Actualizar", command=self.actualizar, state="disabled")

        self.l_inst.grid(column=0, row=0, padx=5)
        self.cb_inst.grid(column=0, row=1, padx=5)
        self.l_prod.grid(column=1, row=0, padx=5)
        self.cb_prod.grid(column=1, row=1, padx=5)
        self.l_talle.grid(column=2, row=0, padx=5)
        self.cb_talle.grid(column=2, row=1, padx=5)
        self.l_prec.grid(column=3, row=0, padx=5)
        self.e_prec.grid(column=3, row=1, padx=5)
        self.b_actualizar.grid(column=4, row=1, padx=5)

        self.cb_prod.bind("<<ComboboxSelected>>",self.cb_prod_selec)
        self.cb_talle.bind("<<ComboboxSelected>>",self.cb_talle_selec)
        self.cb_inst.bind("<<ComboboxSelected>>",self.cb_inst_selec)
    ####### habilitaciones #######
    def cb_prod_edit(self):
        self.cb_talle.delete(0, tk.END)
        self.e_prec.delete(0, tk.END)
        if len(self.cb_inst.get()) == 0:
            self.cb_prod["values"] = self.prod
        self.cb_talle["state"] = "disabled"
        self.e_prec["state"] = "disabled"
        self.b_actualizar["state"] = "disabled"
    def cb_prod_selec(self,event=None):
        self.cb_talle["state"] = "readonly"
        self.cb_talle["values"] = self.talles.ver_talles_de(self.cb_prod.get(),self.cb_inst.get())
        self.cb_talle.current(0)
    def cb_talle_selec(self,event):
        self.cb_inst["state"] = "normal"
        self.e_prec["state"] = "normal"
        self.b_actualizar["state"] = "normal"
        precio = self.base.ver_precio_de(self.cb_prod.get(), self.cb_talle.get())
        #self.e_prec.delete(0, tk.END)
        if len(precio) == 1:
            self.e_prec.delete(0, tk.END)
            self.e_prec.insert(0, precio[0])
        elif len(precio) > 1:
            self.e_prec.delete(0, tk.END)
            self.e_prec.insert(0, min(precio))
    def cb_inst_edit(self):
        self.cb_talle["state"] = "disabled"
        self.e_prec["state"] = "disabled"
    def cb_inst_selec(self,event):
        prod = self.base.ver_tipos_de(self.cb_inst.get())
        self.cb_prod["values"] = prod
        self.cb_prod["state"] = "readonly"
        if len(self.cb_prod["values"]) != 0:
            self.cb_prod.current(0)
    def actualizar(self):
        institucion = self.cb_inst.get()
        tipo = self.cb_prod.get()
        talle = self.cb_talle.get()
        precio = self.e_prec.get()
        self.talles.actualizar_precio(producto=tipo,talle=talle,precio=precio,institucion=institucion)

"""    def cb_desde_selec(self,event):
        indice = self.lista_talles.index(self.desde_selec.get())
        self.lista_hasta = self.lista_talles[indice:]
        self.cb_hasta['values'] = self.lista_hasta
    def limpiar_cb(self):
        self.cb_hasta['values'] = []
        self.cb_hasta.delete(0,tk.END)
    def agregar_n(self):
        productos = set()
        for producto in self.productos.ver():
            productos.add(producto[1])
        if self.entry_n.get().capitalize() not in productos and len(self.entry_n.get()) != 0 and len(self.cb_desde.get()) != 0 and len(self.cb_hasta.get()) != 0:
            finaliza_en = self.lista_hasta.index(self.cb_hasta.get()) +1
            for talle in self.lista_hasta[:finaliza_en]:
                producto = self.entry_n.get().capitalize()
                id_talle = self.talles.ver_id(talle)
                self.productos.agregar(producto,id_talle)
            self.entry_n.delete(0,tk.END)
            self.cb_desde.delete(0,tk.END)
            self.cb_hasta.delete(0,tk.END)
            self.cargar_lista_pro()
        else:
            self.entry_n.delete(0, tk.END)
            self.cb_desde.delete(0, tk.END)
            self.cb_hasta.delete(0, tk.END)"""

#################### ARTICULOS ##################
class Ventana_articulos(tk.Toplevel):
    instituciones = Instituciones()
    productos = Productos()
    articulos = Articulos()
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title("Articulos")
        self.geometry("550x450+500+300")
        self.focus()
        self.grab_set()
        self.widgets()

    def widgets(self):
        self.LabelFrame_nuevo = ttk.LabelFrame(self,text="Nuevo")
        self.widgets_LabelF_nuevo()
        frame = ttk.Frame(self)
        self.label_inst_e = ttk.Label(frame,text="Institucion")
        self.cb_inst_e = ttk.Combobox(frame,width=10,state="readonly",postcommand=self.limpiar_cb_prod_e)
        self.label_prod_e = ttk.Label(frame,text="Producto")
        self.cb_prod_e = ttk.Combobox(frame,width=10)
        self.boton_eliminar = ttk.Button(frame,text="Eliminar")
        self.treeview = ttk.Treeview(frame,columns=("Precio"))
        self.LabelFrame_nuevo.grid(column=0,row=0)
        frame.grid(column=0,row=1,padx=10,pady=20)
        self.label_inst_e.grid(column=0,row=0)
        self.cb_inst_e.grid(column=0,row=1,padx=5)
        self.label_prod_e.grid(column=1,row=0)
        self.cb_prod_e.grid(column=1,row=1,padx=5)
        self.boton_eliminar.grid(column=2,row=1,padx=5)
        self.treeview.grid(column=0,row=2,columnspan=2)

        self.treeview.heading("#0",text="Talle")
        self.treeview.heading("Precio",text="Precio")
        self.cargar_cb_inst_e()
        self.cb_inst_e.bind("<<ComboboxSelected>>",self.cargar_cb_prod_e)

    def cargar_cb_inst_e(self):
        instituciones = self.articulos.ver_instituciones()
        self.cb_inst_e["values"] = instituciones
    def limpiar_cb_prod_e(self):
        self.cb_prod_e.delete(0,tk.END)
    def cargar_cb_prod_e(self,event):
        institucion_selec = self.cb_inst_e.get()
        productos = self.articulos.ver_productos_de(institucion_selec)
        self.cb_prod_e["values"] = productos
    def cargar_treeview(self):
        self.limpiar_treeview()

    def limpiar_treeview(self):
        for valor in self.treeview.get_children():
            self.treeview.delete(valor)


    def widgets_LabelF_nuevo(self):

        frame = ttk.Frame(self.LabelFrame_nuevo)
        frame.grid(column=0, row=0)

        self.label_inst = ttk.Label(frame,text="Institucion")
        self.cb_inst = ttk.Combobox(frame,width=10,state="readonly")
        self.label_inst.grid(column=0, row=0, pady=5, padx=5)
        self.cb_inst.grid(column=0,row=1, pady=5, padx=5)

        self.label_prod = ttk.Label(frame,text="Producto")
        self.cb_prod = ttk.Combobox(frame,width=10,state="readonly")
        self.label_prod.grid(column=1, row=0, pady=5, padx=5)
        self.cb_prod.grid(column=1,row=1, pady=5, padx=5)


        self.label_talle = ttk.Label(frame,text="Talle")
        self.cb_talle = ttk.Combobox(frame,width=10,state="readonly")
        self.label_talle.grid(column=2, row=0, pady=5, padx=5)
        self.cb_talle.grid(column=2,row=1, pady=5, padx=5)

        self.label_prec = ttk.Label(frame,text="Precio")
        self.entry_prec = ttk.Entry(frame,width=10)
        self.label_prec.grid(column=3,row=0, pady=5, padx=5)
        self.entry_prec.grid(column=3,row=1, pady=5, padx=5)

        self.boton_crear = ttk.Button(self.LabelFrame_nuevo,text="Crear",command=self.agregar_n)
        self.boton_crear.grid(column=0,row=1,pady=5)

        ### cargar cb inst ###
        inst = []
        for institucion in self.instituciones.ver():
            inst.append(institucion[1])
        self.cb_inst["values"] = inst
        ### cargar cb prod ###
        prod = []
        for item in self.productos.ver():
            if item[1] not in prod:
                prod.append(item[1])
        self.cb_prod["values"] = prod
        self.cb_prod.bind("<<ComboboxSelected>>",self.cb_prod_selec)
    def cb_prod_selec(self,event):
        self.cargar_cb_talle()
    def cargar_cb_talle(self):
        talle = self.productos.ver_talles_de(self.cb_prod.get())
        self.cb_talle["values"] = talle
    def agregar_n(self):
        if len(self.cb_inst.get()) != 0 and len(self.cb_prod.get()) != 0 and len(self.cb_talle.get()) != 0 and len(self.entry_prec.get()) != 0:
            institucion = self.cb_inst.get()
            producto_id = self.productos.ver_id_de(self.cb_prod.get(),self.cb_talle.get())
            precio = int(self.entry_prec.get())
            self.articulos.agregar(institucion,producto_id,precio)











main = App1()
main.mainloop()
