import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from coneccion_a_base import *


class Stock(ttk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.base = Base()
        self.datos = ["institucion seleccionada","tipo seleccionado"]

        self.labelframe_inst = ttk.LabelFrame(self,text="Institucion")
        self.institucion()
        self.labelframe_inst.grid(column=0,row=0,padx=5,pady=10)

        self.labelframe_prod = ttk.LabelFrame(self,text="Tipo")
        self.tipo()
        self.labelframe_prod.grid(column=1,row=0,padx=5,pady=10)

        self.labelframe_art = ttk.LabelFrame(self,text="Articulos")
        self.articulos()
        self.labelframe_art.grid(column=2,row=0,columnspan=2,padx=15,pady=10)

        self.labelframe_mod = ttk.LabelFrame(self,text="Modificar")
        self.modificar()
        self.labelframe_mod.grid(column=0,row=1,columnspan=3,padx=10,pady=10)


    def institucion(self):
        self.seleccionado_en_lista_inst = ""
        self.lista_inst = tk.Listbox(self.labelframe_inst,borderwidth=0,activestyle=tk.NONE,selectbackground="green",selectforeground="white")#REMOVER BORDES Y SUBRAYADO
        #self.instituciones = set()
        self.cargar_lista_inst()

        self.labeli = ttk.Label(self.labelframe_inst,text="")

        self.lista_inst.grid(column=0,row=0,padx=10,pady=10)
        self.labeli.grid(column=0,row=1)
        #self.entry_inst.grid(column=0,row=2,padx=5,pady=5)
        #self.boton_nuevo_inst.grid(column=0,row=3,padx=5,pady=5)

        #self.lista_inst.selection_set(0)
        #self.seleccion() # al iniciar si el usuario usa la otra lista la variable queda vacia
        self.lista_inst.bind('<<ListboxSelect>>',self.seleccion)

    def cargar_lista_inst(self):
        self.lista_inst.delete(0,tk.END)
        for n,institucion in enumerate(self.base.ver_instituciones()):
            self.lista_inst.insert(n,institucion)



    def tipo(self) :
        self.lista_prod = tk.Listbox(self.labelframe_prod,borderwidth=0,activestyle=tk.NONE,selectbackground="green",selectforeground="white")
        #self.entry_prod = ttk.Entry(self.labelframe_prod)
        #self.boton_agregar_prod = ttk.Button(self.labelframe_prod,text="Nuevo")
        self.label2 = ttk.Label(self.labelframe_prod,text="")

        self.lista_prod.grid(column=0,row=0,padx=10,pady=10)
        self.label2.grid(column=0,row=1)
        #self.entry_prod.grid(column=0,row=1,padx=5,pady=5)
        #self.boton_agregar_prod.grid(column=0,row=2,padx=5,pady=5)
        self.lista_prod.bind('<<ListboxSelect>>',self.seleccion_tipo)

    def cargar_lista_tipo(self,institucion="no hay"):
        if institucion != "no hay":
            self.lista_prod.delete(0,tk.END)
            for tipo in self.base.ver_tipos_de(institucion):
                self.lista_prod.insert(tk.END,tipo)
        else:
            self.lista_prod.delete(0,tk.END)


    def articulos(self):
        #treeview
        style = ttk.Style()
        style.configure("Treeview",background="silver",fount=("",12))
        self.treeview = ttk.Treeview(self.labelframe_art,columns=("cant","precio"),style="estilo.Treeview")
        self.treeview.heading("#0",text="Talle")
        self.treeview.column("# 0",anchor="center") #NO FUNCIONA EL CENTRADO EN TALLE
        self.treeview.heading("cant",text="Cantidad")
        self.treeview.column("cant",anchor="center")
        self.treeview.heading("precio",text="Precio")
        self.treeview.column("precio",anchor="center")
        self.treeview.tag_configure('no hay',background='red')
        self.treeview.tag_configure('hay',background='green')
        self.treeview.tag_bind("no hay","<<TreeviewSelect>>",self.treeview_select)
        self.treeview.tag_bind("hay","<<TreeviewSelect>>",self.treeview_select)


        self.labelframe_agregar = tk.LabelFrame(self.labelframe_art,text="Modificar articulo")
        #talles

        self.boton_agregar = ttk.Button(self.labelframe_agregar,text="Agegar")
        self.boton_quitar = ttk.Button(self.labelframe_agregar,text="Quitar")


        #self.combobox.grid(column=1,row=0,padx=5,pady=5)
        #self.boton_agregar.grid(column=2,row=0,padx=5,pady=5)
        #self.boton_quitar.grid(column=3,row=0,padx=5,pady=5)

        #self.labelframe_agregar.grid(column=0,row=1,padx=5,pady=5)

        self.treeview.grid(column=0,row=0,padx=10,pady=5,columnspan=3)


    def modificar(self):
        self.talles = ("No aplica","mediano","grande","2","4","6","8","10","12","14","XS","S","M","L","XL","XXL")
        self.talle_select = tk.StringVar()

        self.labelinst = ttk.Label(self.labelframe_mod,text="Institucion")
        self.labelt = ttk.Label(self.labelframe_mod,text="Tipo")
        label3 = ttk.Label(self.labelframe_mod,text="Talle")
        self.labelc = ttk.Label(self.labelframe_mod,text="Cant.")
        self.entry_mod_inst = ttk.Entry(self.labelframe_mod,width=15)
        self.entry_mod_tipo = ttk.Entry(self.labelframe_mod,width=15)
        self.combobox = ttk.Combobox(self.labelframe_mod,textvariable=self.talle_select,values=self.talles,width=5,state='readonly')
        self.combobox.current(0)
        self.cant = ttk.Spinbox(self.labelframe_mod,width=5,from_=1,to=100)
        self.cant.set(1)
        self.agregar = ttk.Button(self.labelframe_mod,text="Agregar",command=self.agregar)
        self.quitar = ttk.Button(self.labelframe_mod,text="Quitar",command=self.quitar)

        self.labelinst.grid(column=0,row=0)
        self.entry_mod_inst.grid(column=0,row=1,padx=5,pady=5)
        self.labelt.grid(column=1,row=0)
        self.entry_mod_tipo.grid(column=1,row=1,padx=10,pady=5)
        label3.grid(column=2,row=0)
        self.combobox.grid(column=2,row=1,padx=10,pady=5)
        self.labelc.grid(column=3,row=0)
        self.cant.grid(column=3,row=1,padx=10,pady=5)
        self.agregar.grid(column=4,row=1,padx=10,pady=5)
        self.quitar.grid(column=5,row=1,padx=5,pady=5)

    def verificar(self,institucion,tipo,talle,cantidad):
        ####### verificar que hay datos para modificar ##########
        if len(institucion) != 0:
            print("hay institucion")
            self.labelinst.config(text="Institucion",foreground="black")
            if len(tipo) != 0:
                print("hay todo")
                self.labelt.config(text="Tipo",foreground="black")
                ############# verifico si cantidad es un numero #########
                if cantidad.isdigit():
                    self.labelc.config(text="Cant.",foreground="black")
                    ############ si todos los campos estan completos se realiza la consulta ##########
                    return True
                else:
                    self.labelc.config(text="Cant. *",foreground="red")
            else:
                self.labelt.config(text="Tipo *",foreground="red")
                print("hay institucion pero no tipo")
        else:
            self.labelinst.config(text="Institucion *",foreground="red")
            if len(tipo) == 0:
                self.labelt.config(text="Tipo *",foreground="red")

    def realizar_consulta(self,consulta):
        institucion = self.entry_mod_inst.get()
        tipo = self.entry_mod_tipo.get()
        talle = self.combobox.get()
        cantidad = self.cant.get()
        ###### si verificar devuelve true se realiza la consulta #########
        if self.verificar(institucion,tipo,talle,cantidad):
            print("todo bien para consultar")
            #### si el dato ya se encuentra y se tiene que actualizar ####
            if self.base.verificar_dato(institucion,tipo,talle):
                print("actualizando dato")
                if consulta == "agregar":
                    self.base.modificar_dato(institucion,tipo,talle,cantidad,agregar=True)
                elif consulta == "quitar":
                    print("listo para quitar")
                    self.base.modificar_dato(institucion,tipo,talle,cantidad,quitar=True)

            else:
                print("agregando dato nuevo ")
                ### para que las listas esten ordenadas los valores deben empezar en mayusculas ####
                institucion[0].upper()
                tipo[0].upper()
                ####################################################################################
                ###### Agregando el dato nuevo #######
                self.base.modificar_dato(institucion,tipo,talle,cantidad,agregar=True)
                ######################################
                ####### Actualizando las listas ########
                self.cargar_lista_inst()
                self.cargar_lista_tipo()
                #######################################
                ###### SELECCIONO LA NUEVA INSTITUCION ######
                lista = self.lista_inst.get(0,tk.END)
                indice = lista.index(institucion)
                self.lista_inst.selection_set(indice)
                self.seleccion()
                ###### SELECCIONO EL NUEVO TIPO #############
                tipos = self.lista_prod.get(0,tk.END)
                indi = tipos.index(tipo)
                self.lista_prod.selection_set(indi)
                self.seleccion_tipo()
                #############################################
            ##### ACTUALIZO LA TREEVIEW #######
            self.cargar_treeview()
            ######### vuelve cantidad a 1 #######
            self.cant.set(1)

    def agregar(self):
        self.realizar_consulta("agregar")
    def quitar(self):
        self.realizar_consulta("quitar")



    def treeview_select(self,event=None):
        if self.treeview.selection() != 0 :
            posicion = self.treeview.selection()[0] #devuelve I001
            print(posicion)
            print(self.treeview.item(posicion,option="text"))
            seleccion = self.treeview.item(posicion,option="text")
            self.combobox.set(seleccion)


    def seleccion(self,event=None):
        if len(self.lista_inst.curselection()) != 0:
            self.datos[0] = "no hay seleccion"
            #actualizar treeview
            self.cargar_treeview()
            posicion = self.lista_inst.curselection()[0]
            self.institucion_seleccionada = str(self.lista_inst.get(posicion))
            self.datos.insert(0,self.institucion_seleccionada)
            self.labeli.config(text=self.datos[0])
            ########## ENTRY DE MODIFICAR #####
            self.entry_mod_tipo.delete(0,tk.END)
            self.entry_mod_inst.delete(0,tk.END)
            self.entry_mod_inst.insert(0,self.datos[0])
            #self.labeli.config(text=institucion_seleccionada)
            for i in range(self.lista_inst.size()):
                self.lista_inst.itemconfigure(i,bg="white",fg="black")
            self.lista_inst.itemconfigure(posicion,bg="green",fg="white")
            # ver los tipos de las institucion seleccionada
            self.cargar_lista_tipo(self.institucion_seleccionada)



            #ver los articulos
    def seleccion_tipo(self,event=None):
        self.label2.config(text=self.datos[1])
        if len(self.lista_prod.curselection()) != 0 :
            self.datos[1] = "no hay seleccion"
            tipo_seleccionado = str(self.lista_prod.get(self.lista_prod.curselection()[0]))
            self.datos[1] = tipo_seleccionado
            self.label2.config(text=self.datos[1])
            ######## ENTRY MODIFICAR TIPO ########
            self.entry_mod_tipo.delete(0,tk.END)
            self.entry_mod_tipo.insert(0,self.datos[1])
            self.cargar_treeview()
            #Mantener la seleccion
            for i in range(self.lista_prod.size()):
                self.lista_prod.itemconfigure(i,bg="white",fg="black") # poner los items de lista en fondo blanco y letras negras
            self.lista_prod.itemconfigure(self.lista_prod.curselection()[0],bg="green",fg="white")# y dejar el item seleccionado en fondo verde y letras blancas

    def cargar_treeview(self):
        # limpiar treeview
        for valor in self.treeview.get_children():
            self.treeview.delete(valor)
        # agregar registros a treeview
        for registro in self.base.ver_articulos(self.datos[0],self.datos[1]):
            talle = registro[3]
            cantidad = registro[4]
            precio = registro[5]
            if cantidad != 0:
                self.treeview.insert("",tk.END,text=talle,values=(cantidad,precio),tags=('hay',))
            elif cantidad == 0:
                self.treeview.insert("",tk.END,text=talle,values=(cantidad,precio),tags=('no hay',))





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
