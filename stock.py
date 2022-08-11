import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from coneccion_a_base import *
from conexion import *


class Stock(ttk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.estilos = ttk.Style()
        self.estilos.configure("TLabel",font="Helvetica 10")
        self.estilos.configure("TEntry",font="Helvetica 15")

        self.base = Base()
        self.talles = Talles()
        self.datos = ["institucion seleccionada","tipo seleccionado","talle seleccionado","precio seleccionado"]

        self.labelframe_inst = ttk.LabelFrame(self,text="Institucion")
        self.institucion()
        self.labelframe_inst.grid(column=0,row=0,padx=5,pady=10)

        self.labelframe_prod = ttk.LabelFrame(self,text="Tipo")
        self.tipo()
        self.labelframe_prod.grid(column=1,row=0,padx=5,pady=10)

        self.labelframe_art = ttk.LabelFrame(self,text="Articulos")
        self.articulos()
        self.labelframe_art.grid(column=2,row=0,columnspan=2,padx=15,pady=10)

        self.boton_a = ttk.Button(self, text="Actualizar", command=self.cargar_lista_inst)
        self.boton_a.grid(column=0, row=2)


    def institucion(self):
        self.seleccionado_en_lista_inst = ""
        self.lista_inst = tk.Listbox(self.labelframe_inst,borderwidth=0,activestyle=tk.NONE,selectbackground="#7EBCFF",selectforeground="black",font="Helvetica 15",width=15)#REMOVER BORDES Y SUBRAYADO
        self.cargar_lista_inst()
        self.labeli = ttk.Label(self.labelframe_inst,text="")

        self.lista_inst.grid(column=0,row=0,padx=10,pady=10)

        self.lista_inst.bind('<<ListboxSelect>>',self.seleccion)

    def limpiarLista(self,lista):
        lista.delete(0,tk.END)

    def cargar_lista_inst(self):
        self.limpiarLista(self.lista_inst)
        for n,institucion in enumerate(self.base.ver_instituciones()):
            self.lista_inst.insert(n,institucion)



    def tipo(self) :
        self.lista_prod = tk.Listbox(self.labelframe_prod,borderwidth=0,activestyle=tk.NONE,selectbackground="#7EBCFF",selectforeground="black",font="Helvetica 15",width=15)
        self.label2 = ttk.Label(self.labelframe_prod,text="")

        self.lista_prod.grid(column=0,row=0,padx=10,pady=10)
        self.label2.grid(column=0,row=1)
        self.lista_prod.bind('<<ListboxSelect>>',self.seleccion_tipo)

    def cargar_lista_tipo(self,institucionSeleccionada="no hay"):
        if institucionSeleccionada != "no hay":
            self.limpiarLista(self.lista_prod)
            self.insertarDatosDe(institucionSeleccionada)
        else:
            self.limpiarLista(self.lista_prod)

    def insertarDatosDe(self,institucion):
        for dato in self.base.ver_tipos_de(institucion):
            self.lista_prod.insert(tk.END,dato)

    def articulos(self):
        #treeview
        style = ttk.Style()
        style.configure("estilo.Treeview",background="silver",font="Helvetica 15 ",rowheight=35)
        style.configure("estilo.Treeview.Heading",font="Helvetica 18 ")
        self.scroll = tk.Scrollbar(self.labelframe_art,orient=tk.VERTICAL)
        self.treeview = ttk.Treeview(self.labelframe_art,columns=("cant"),style="estilo.Treeview",yscrollcommand=self.scroll.set)
        self.treeview.heading("#0",text="Talle")
        self.treeview.column("# 0",anchor="center") #NO FUNCIONA EL CENTRADO EN TALLE
        self.treeview.heading("cant",text="Cantidad")
        self.treeview.column("cant",anchor="center")
        

        # CONFIGURACION DE LOS TAGS:
        self.treeview.tag_configure('oddrow',background='#FFDFDF')
        self.treeview.tag_configure('oddrow2', background='#FFC7C7')
        self.treeview.tag_configure('evenrow',background='#E0FFC7')
        self.treeview.tag_configure('evenrow2', background='#CEFFA8')
        self.treeview.tag_bind("oddrow","<<TreeviewSelect>>",self.treeview_select)
        self.treeview.tag_bind("oddrow2", "<<TreeviewSelect>>", self.treeview_select)
        self.treeview.tag_bind("evenrow","<<TreeviewSelect>>",self.treeview_select)
        self.treeview.tag_bind("evenrow2", "<<TreeviewSelect>>", self.treeview_select)

        # demas widgets 
        frame = ttk.Frame(self.labelframe_art)
        # precio 
        self.label_precio = ttk.Label(frame,text="Precio: -----",font="Helvetica 15",foreground="blue")
        # botones agregar y quitar
        self.agregar_b = ttk.Button(frame, text="Agregar", command=self.agregar_c,state="disabled")
        self.quitar_b = ttk.Button(frame,text="Quitar",state="disabled",command=self.quitar_c)
        # spinbox de cantidad 
        self.sb_cantidad = ttk.Spinbox(frame, width=3, from_=0, to=100, font="hevetica 15",state="readonly")
        self.sb_cantidad.set(1)
        # posicionamiento de los widgets 
        self.label_precio.grid(column=0,row=0)
        self.sb_cantidad.grid(column=0,row=1,pady=5)
        self.agregar_b.grid(column=0,row=2,pady=5)
        self.quitar_b.grid(column=0,row=3,pady=5)

        # boton eliminar
        self.b_eliminar = ttk.Button(self.labelframe_art,text="Eliminar",state="disabled",command=self.eliminar_a)

        self.treeview.grid(column=0,row=0,pady=5,columnspan=3)
        self.scroll.configure(command=self.treeview.yview)
        self.scroll.grid(column=3,row=0,sticky="NS")
        frame.grid(column=4, row=0, padx=10, pady=5)
        self.b_eliminar.grid(column=4,row=1)

    def eliminar_a(self):
        inst = self.datos[0]
        tipo = self.datos[1]
        talle = self.datos[2]
        self.base.eliminar_dato(inst,tipo,talle)
        self.cargar_treeview()
    def agregar_c(self):
        self.modificar_dato(a=True)
    def quitar_c(self):
        self.modificar_dato(q=True)
    def modificar_dato(self,a=False,q=False):
        institucion = self.datos[0]
        tipo = self.datos[1]
        talle = self.datos[2]
        precio = self.datos[3]
        cantidad = self.sb_cantidad.get()
        self.base.modificar_dato(institucion, tipo, talle, cantidad, precio, agregar=a,quitar=q)
        self.cargar_treeview()
        self.sb_cantidad.set(1)

    def CambiarestadoBotonesAQE(self,estado):
        self.agregar_b  ["state"] = estado
        self.quitar_b   ["state"] = estado
        self.b_eliminar ["state"] = estado

        # Configura el precio 
    def labelPrecio(self,precio=None):
        if precio != None:
            self.label_precio.config(text="Precio: {}".format(precio))
        else:
            self.label_precio.config(text="Precio: -----")

    def treeview_select(self,event=None):
        if self.treeview.selection() != 0 :
            posicion = self.treeview.selection()[0] #devuelve I001
            talle = self.treeview.item(posicion, option="text")
            valores = self.treeview.item(posicion,option="values")
            precio = valores[1]
            self.datos.insert(2,talle)
            self.datos.insert(3,precio)
            self.CambiarestadoBotonesAQE("normal")
            #precio 
            self.labelPrecio(precio)

# configuracion de la lista instituciones al seleccionar un item 
    def seleccion(self,event=None): 
        if len(self.lista_inst.curselection()) != 0: # en caso de no seleccionar algun item de la lista 
            self.configItemSeleccionado(self.lista_inst,0)
            # ver los tipos de las institucion seleccionada
            self.cargar_lista_tipo(self.seleccionDe(self.lista_inst))

    def configItemSeleccionado(self,lista,tipoDato):
        self.datos[tipoDato] = "no hay seleccion"
        self.datos[tipoDato] = self.seleccionDe(lista)
        self.mantenerSeleccionDe(lista)
        self.cargar_treeview()
        # actualizo el precio :
        self.labelPrecio()
            

    def seleccionDe(self,lista): # devuelve la institucion seleccionada de la lista institucion
        seleccion = lista.get(self.posicionDe(lista))
        return str(seleccion)
    def posicionDe(self,lista): # devuelve la posicion 
        return lista.curselection()


# la seleccion de una lista se pierde cuando selecciono un item de otra lista
#por lo tanto para mantener la seleccion se usa esta funcion 
    def mantenerSeleccionDe(self,lista): # mantiene el backgroudn de la seleccion en azul 
        for i in range(lista.size()):
            lista.itemconfigure(i,bg="white",fg="black")
        lista.itemconfigure(self.posicionDe(lista),bg="#7EBCFF",fg="black")

            #ver los articulos
    def seleccion_tipo(self,event=None):
        self.ver_total_p()
        if len(self.lista_prod.curselection()) != 0 :
            self.configItemSeleccionado(self.lista_prod,1)
            self.ver_total_p()
            #Mantener la seleccion
            self.mantenerSeleccionDe(self.lista_prod)
            

    def cargar_treeview(self):
        self.CambiarestadoBotonesAQE("disabled")
        # limpiar treeview
        for valor in self.treeview.get_children():
            self.treeview.delete(valor)
        # actualizar los valores de self.label2
        self.ver_total_p()
        # agregar registros a treeview
        contador = 1
        for registro in self.base.ver_articulos(self.datos[0],self.datos[1]):
            talle = registro[3]
            cantidad = registro[4]
            precio = registro[5]
            if cantidad != 0:
                if contador % 2 == 0:
                    self.treeview.insert("",tk.END,text=talle,values=(cantidad,precio),tags=('evenrow',))
                    contador += 1
                else :
                    self.treeview.insert("", tk.END, text=talle, values=(cantidad, precio), tags=('evenrow2',))
                    contador += 1
            elif cantidad == 0:
                if contador % 2 == 0:
                    self.treeview.insert("",tk.END,text=talle,values=(cantidad,precio),tags=('oddrow',))
                    contador += 1
                else:
                    self.treeview.insert("", tk.END, text=talle, values=(cantidad, precio), tags=('oddrow2',))
                    contador += 1

    def ver_total_p(self):
        self.label2.config(text=self.datos[1])
        cantidades = Cantidades()
        cantidad_de = cantidades.producto(self.datos[0],self.datos[1])
        if cantidad_de != None:
            self.label2.config(text="Total: {}".format(cantidad_de))
        else:
            self.label2.config(text="")


