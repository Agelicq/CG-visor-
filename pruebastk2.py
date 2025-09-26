#para ver los cambios reflejados commit

import tkinter as tk


ventana = tk.Tk()
#redimeniona la ventana 500x1500
ventana.geometry("500x500")

etiqueta = tk.Label(ventana, text="Hola mundo")
#se pone en pantalla y centrado 
#etiqueta.pack()
#cambia la posicion
etiqueta.pack(side=tk.BOTTOM)

#crea la venta 
ventana.mainloop()