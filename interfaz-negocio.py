
import tkinter as tk
from tkinter  import ttk
from tkinter import messagebox
import sqlite3


#--verificacion--      
def verificar_credenciales(usuario, contraseña):
    return usuario == "a" and contraseña == "a"

def iniciar_sesion():
    usuario_ingresado = entry_usuario.get()
    contraseña_ingresada = entry_contraseña.get()

    if verificar_credenciales(usuario_ingresado, contraseña_ingresada):
        ventana_login.destroy()  # Cerrar la ventana de inicio de sesión
        mostrar_interfaz_principal()
    else:
        messagebox.showerror("Error", "Credenciales incorrectas")
        
    
#--agregar info a la base de datos--
def agregar(articulo,cantidad,precio_costo,precio, seccion):
    try:
        miConec = sqlite3.connect("negocioBD", isolation_level=None, check_same_thread=False)

        miCursor = miConec.cursor()

        #miCursor.execute("CREATE TABLE PRODUCTOS (ARTICULO VARCHAR(50),CANTIDAD INTERGER,PRECIO_COSTO INTERGER, PRECIO INTEGER, SECCION VARCHAR(20))")
        miCursor.execute("INSERT INTO PRODUCTOS (articulo,cantidad,precio_costo,precio,seccion) VALUES (?,?,?,?,?)", (articulo,cantidad,precio_costo, precio, seccion))
        miConec.commit()
        miConec.close()
        
        messagebox.showinfo("Éxito", "Producto guardado correctamente.")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el producto: {e}")
        


#--interfaces---

def mostrar_interfaz_principal():
    ventana = tk.Tk()   
    ventana.title("MI NEGOCIO")
    ventana.resizable(False, False)
    ventana.configure(bg="lightgray", cursor="circle")
    barra_menu = tk.Menu(ventana)
    ventana.config(menu=barra_menu)
    
    menu_principal = tk.Menu(barra_menu)
    barra_menu.add_cascade(label="PRODUCTOS Y STOCK", menu=menu_principal)

    menu_principal.add_command(label="AGREGAR A STOCK", command=on_button_click)
    menu_principal.add_command(label="STOCK", command=on_button_click2)
    menu_principal.add_separator()
    menu_principal.add_command(label="SALIDA", command=ventana.destroy)
            
    miConec = sqlite3.connect("negocioBD", isolation_level=None, check_same_thread=False)
    miCursor = miConec.cursor()
    
    def buscar():
        # Limpiar la lista de resultados
        resultados_listbox.delete(0, tk.END)

        # Obtener el término de búsqueda
        termino_busqueda = buscar_entry.get()

        # Realizar la búsqueda en la base de datos
        miCursor.execute("SELECT ARTICULO,PRECIO,CANTIDAD FROM PRODUCTOS WHERE SECCION LIKE ?", ('%' + termino_busqueda + '%',))
        filas = miCursor.fetchall()
        # Actualizar la lista de productos con los resultados de la base de datos
        productos.clear()
        for fila in filas:
            ARTICULO, PRECIO, CANTIDAD = fila
            # Mostrar resultados en la lista
            resultado_str = f"{ARTICULO.ljust(50)} | ${PRECIO:,.2f} | {CANTIDAD} "
            resultados_listbox.insert(tk.END, resultado_str)
            # Almacenar información del producto en la lista
            productos.append({"ARTICULO": ARTICULO, "PRECIO": PRECIO, "CANTIDAD": CANTIDAD})
         
            
    def calcular_total():
        seleccionados = resultados_listbox.curselection()

        total = 0
        for index in seleccionados:
            productos_index = int(index)
            total += productos[productos_index]["PRECIO"]

        total_label.config(text=f"PRECIO: ${total:.2f}")

    tk.Label(ventana, bg="lightgray", text="BUSCAR PRODUCTO:", font=("Comic 12")).grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
    buscar_entry = tk.Entry(ventana, width=40)
    buscar_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.E)

    tk.Button(ventana, bg="#888", fg="white", text="BUSCAR", command=buscar, width=21, font=("Comic 10")).grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)

    # Lista de resultados
    resultados_listbox = tk.Listbox(ventana, width=40, height=10, font=("Comic", 15))
    resultados_listbox.grid(row=1, column=0, columnspan=3, sticky=tk.EW)

    # Etiqueta para mostrar el total
    total_label = tk.Label(ventana, text="PRECIO: $0.00",bg="#555",fg="white")
    total_label.grid(row=2, column=0, padx=10, pady=10, sticky=tk.W)

    # Manejar el evento de selección
    resultados_listbox.bind("<<ListboxSelect>>", lambda event: calcular_total())
    # Lista para almacenar la información de los productos
    productos = []
    ventana.mainloop()
def on_button_click():
    
    raiz = tk.Tk() 
    raiz.title("EDICION DE PRODUCTOS")
    raiz.configure(bg="lightgray",cursor="circle")
    raiz.resizable(False,False)

    tk.Label(raiz,text="ARTICULO",font="comic 12",bg="lightgray").pack(pady=5)
    entry_articulo = tk.Entry(raiz,width=30)
    entry_articulo.pack(padx=10)
    tk.Label(raiz,text="CANTIDAD",font="comic 12",bg="lightgray").pack(pady=5)
    entry_cantidad = tk.Entry(raiz,width=30 )
    entry_cantidad.pack(padx=10)
    tk.Label(raiz,text="PRECIO COSTO",font="comic 12",bg="lightgray").pack(pady=5)
    entry_costo = tk.Entry(raiz,width=30 )
    entry_costo.pack(padx=10)
    tk.Label(raiz,text="PRECIO VENDER",font="comic 12",bg="lightgray").pack(pady=5)
    entry_precio = tk.Entry(raiz,width=30 )
    entry_precio.pack(padx=10)
    tk.Label(raiz,text="SECCION",font="comic 12",bg="lightgray").pack(pady=5)
    entry_seccion = tk.Entry(raiz,width=30)
    entry_seccion.pack(padx=10)
            
    boton_agregar = tk.Button(raiz,font="comic 10",bg="#888",fg="white",text="AGREGAR",command=lambda: agregar(entry_articulo.get(),entry_cantidad.get(),entry_costo.get(), entry_precio.get(),entry_seccion.get()),width=20)
    boton_agregar.pack(padx=10,pady=15)
    boton_salir = tk.Button(raiz,bg="#888",fg="white", text="SALIR",command=raiz.destroy ,width=20,font="comic 10")
    boton_salir.pack(padx=10,pady=5)

    raiz.mainloop()

        
def on_button_click2():
    
    miConec = sqlite3.connect("negocioBD", isolation_level=None, check_same_thread=False)
    miCursor = miConec.cursor()
    def eliminar_registro():
        # Obtener el item seleccionado en el Treeview
        selected_item = tree.selection()
    
        if selected_item:
            # Obtener el valor de la columna SECCION del registro seleccionado
            seccion_a_eliminar = tree.item(selected_item, 'values')[4]

            # Eliminar el registro de la base de datos
            miCursor.execute("DELETE FROM PRODUCTOS WHERE SECCION=?", (seccion_a_eliminar,))
            miConec.commit()

            # Eliminar el item seleccionado del Treeview
            tree.delete(selected_item)
            messagebox.showinfo("Éxito", "Registro eliminado correctamente")
        else:
            messagebox.showwarning("Advertencia", "Selecciona un registro antes de eliminar")
    def mostrar_datos():
        # Limpiar la tabla antes de cargar nuevos datos  
        for row in tree.get_children():
            tree.delete(row)

        # Consultar datos de la base de datos
        miCursor.execute('SELECT * FROM PRODUCTOS')
        datos = miCursor.fetchall()

        # Mostrar datos en la tabla
        for dato in datos:
            tree.insert('', 'end', values=dato)
            
    def editar_registro():
        # Obtener el item seleccionado en el Treeview
        selected_item = tree.selection()
        if selected_item:
            # Obtener los valores actuales del registro seleccionado
            current_values = tree.item(selected_item, 'values')

            # Crear una ventana emergente para la edición
            edit_window = tk.Toplevel(raiz)
            edit_window.title("Editar Registro")


            
            # Etiquetas y cajas de entrada para la edición
            tk.Label(edit_window, text="NUEVO ARTICULO:").grid(row=0, column=0, padx=10, pady=5)
            articulo_entry = tk.Entry(edit_window)
            articulo_entry.grid(row=0, column=1, padx=10, pady=5)
            articulo_entry.insert(0, current_values[0])
            
            tk.Label(edit_window, text="NUEVA CANTIDAD:").grid(row=1, column=0, padx=10, pady=5)
            cantidad_entry = tk.Entry(edit_window)
            cantidad_entry.grid(row=1, column=1, padx=10, pady=5)
            cantidad_entry.insert(0, current_values[1])
            
            tk.Label(edit_window, text="NUEVO PRECIO COSTO:").grid(row=2, column=0, padx=10, pady=5)
            costo_entry = tk.Entry(edit_window)
            costo_entry.grid(row=2, column=1, padx=10, pady=5)
            costo_entry.insert(0, current_values[2])
            
            tk.Label(edit_window, text="NUEVO PRECIO:").grid(row=3, column=0, padx=10, pady=5)
            newprecio_entry = tk.Entry(edit_window)
            newprecio_entry.grid(row=3, column=1, padx=10, pady=5)
            newprecio_entry.insert(0, current_values[3])
            
            tk.Label(edit_window, text="NUEVA SECCION:").grid(row=4, column=0, padx=10, pady=5)
            newseccion_entry = tk.Entry(edit_window)
            newseccion_entry.grid(row=4, column=1, padx=10, pady=5)
            newseccion_entry.insert(0, current_values[4])
      
            def aplicar_edicion():
                try:
                    # Crear variables Tkinter para almacenar los nuevos datos
                    nuevo_articulo = articulo_entry.get()
                    nuevo_cantidad = cantidad_entry.get()
                    nuevo_costo = costo_entry.get()
                    nuevo_precio = newprecio_entry.get()
                    nuevo_seccion = newseccion_entry.get()
                    print("Nuevos valores:", nuevo_articulo, nuevo_cantidad, nuevo_costo, nuevo_precio, nuevo_seccion)
                    # Actualizar los datos en la base de datos
                    miCursor.execute("UPDATE PRODUCTOS SET ARTICULO=?, CANTIDAD=?, PRECIO_COSTO=?, PRECIO=?, SECCION=? WHERE SECCION=?", (nuevo_articulo, nuevo_cantidad, nuevo_costo, nuevo_precio, nuevo_seccion, current_values[4]))
                    # Guardar los cambios
                    miConec.commit()
                
                    # Cerrar la ventana de edición
                    edit_window.destroy()

                    # Actualizar la interfaz para reflejar los cambios
                    mostrar_datos()
                except Exception as e:
                    print("Error al aplicar edicion:",e)
                
            tk.Button(edit_window, text="Aplicar Edición", command=aplicar_edicion).grid(row=5, columnspan=2, pady=10)

    # Crear un árbol para mostrar los datos
    raiz = tk.Tk()
    raiz.title("GESTION DE STOCK")
    raiz.configure(bg="lightgray",cursor="circle")
    raiz.resizable(False,False)

    btn_editar = tk.Button(raiz,bg="#888",fg="white",  text='EDITAR REGISTRO', command=editar_registro,width=30)
    btn_editar.pack(pady=5)
    btn_eliminar = tk.Button(raiz,bg="#888",fg="white",  text='ELIMINAR REGISTRO', command=eliminar_registro,width=30)
    btn_eliminar.pack(pady=5)
    tree = ttk.Treeview(raiz, columns=('ARTICULO', 'CANTIDAD', 'PRECIOCOSTO','PRECIO','SECCION'),show="headings")
    tree.heading('ARTICULO', text='ARTICULO')
    tree.heading('CANTIDAD', text='CANTIDAD')
    tree.heading('PRECIOCOSTO', text='PRECIO DE COSTO')
    tree.heading('PRECIO', text='PRECIO A VENDER')
    tree.heading('SECCION', text='SECCION')

    mostrar_datos()

    
    
    tree.pack(expand=True,fill='both', pady=20)

    raiz.mainloop()


#--ventana de inicio de sesión--
ventana_login = tk.Tk()
ventana_login.title("Inicio de Sesión")
ventana_login.geometry("250x150")
ventana_login.resizable(False,False)
label_usuario = tk.Label(ventana_login, text="Usuario:", font="Comic 12")
label_usuario.pack()

entry_usuario = tk.Entry(ventana_login,width=35)
entry_usuario.pack()

label_contraseña = tk.Label(ventana_login, text="Contraseña:",font="Comic 12")
label_contraseña.pack()

entry_contraseña = tk.Entry(ventana_login, show="*",width=35)
entry_contraseña.pack()

boton_iniciar_sesion = tk.Button(ventana_login,font="Comic 12", text="Iniciar Sesión",height=2 ,width=10,command=iniciar_sesion)
boton_iniciar_sesion.pack(padx=0,pady=15)

ventana_login.mainloop()
