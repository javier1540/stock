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
            self.label_precio.config(text="Precio: -----")
            self.label_precio.config(text="Precio: {}".format(precio))
    
    def CambiarestadoBotonesAQE(self,estado):
        self.agregar_b  ["state"] = estado
        self.quitar_b   ["state"] = estado
        self.b_eliminar ["state"] = estado


    def seleccion(self,event=None):
        if len(self.lista_inst.curselection()) != 0:
            self.datos[0] = "no hay seleccion"
            #actualizar treeview
            self.cargar_treeview()
            self.datos.insert(0,self.institucionSeleccionada())
            self.mantenerSeleccion()
            # ver los tipos de las institucion seleccionada
            self.cargar_lista_tipo(self.institucionSeleccionada())
             # borro el precio anterior :
            self.label_precio.config(text="Precio: -----")

    def institucionSeleccionada(self): # devuelve la institucion seleccionada de la lista institucion
        institucion     = self.lista_inst.get(self.posicionInst())
        return str(institucion)
    def posicionInst(self): # devuelve la posicion 
        return self.lista_inst.curselection()[0]
    def mantenerSeleccion(self): # mantiene el backgroudn de la seleccion en azul 
        for i in range(self.lista_inst.size()):
            self.lista_inst.itemconfigure(i,bg="white",fg="black")
        self.lista_inst.itemconfigure(self.posicionInst(),bg="#7EBCFF",fg="black")

            #ver los articulos
    def seleccion_tipo(self,event=None):
        self.ver_total_p()
        if len(self.lista_prod.curselection()) != 0 :
            self.datos[1] = "no hay seleccion"
            tipo_seleccionado = str(self.lista_prod.get(self.lista_prod.curselection()[0]))
            self.datos[1] = tipo_seleccionado
            self.ver_total_p()
            self.cargar_treeview()
            #Mantener la seleccion
            for i in range(self.lista_prod.size()):
                self.lista_prod.itemconfigure(i,bg="white",fg="black") # poner los items de lista en fondo blanco y letras negras
            self.lista_prod.itemconfigure(self.lista_prod.curselection()[0],bg="#7EBCFF",fg="black")# y dejar el item seleccionado en fondo verde y letras blancas
            # borro el precio anterior :
            self.label_precio.config(text="Precio: -----")

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



"""

            LISTAS
    * configurar el boton nuevo de la lista institucion :
        * al precionar el boton nuevo se agrega lo que se escribio en el entry a la base en un registro donde todos los campos ecepto institucion estan en none
            * el boton nuevo puede tener una toplevel y sacar el entry de la ventana principal
    * configurar la lista tipo
        * que reciba en un conjunto los tipos de la base
        * personalizar

    cuestiones:
    * que pasaria si yo quisiera modificar el nombre de una institucion ?
        1 con el mismo entry y un boton modificar actualizaria con update todos los campos de insticion seleccionado por la lista
        2 haciendo doble clic en la posicion de la lista y superponer un entry y que precionando enter se modifique el valor


            TREEVIEW
    * la treeview articulos tiene que mostrar los elementos de la base filtrados por la lista inst y tipo



"""
