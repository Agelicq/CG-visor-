import tkinter as tk


ventana = tk.Tk()
#redimeniona la ventana 500x1500
ventana.geometry("500x500")

etiqueta = tk.Label(ventana, text="Hola mundo")
etiqueta.pack()

#crea la venta 
ventana.mainloop()