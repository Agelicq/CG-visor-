import tkinter as tk
from PIL import Image, ImageTk
#PIL es la libreria para trabajar con imagenes con tkinter
from tkinter import filedialog, messagebox, Scale
import auxVisor as aux
import matplotlib.pyplot as plt

#revisar el tamaño de la imagen / en proceso la funcion de contraste 

class VisorImagenes:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Visor de imagenes")
        #redimeniona la ventana 1500x1500
        self.ventana.geometry("1500x950")

        titulo = tk.Label(ventana, text="VISOR", fg = "DarkOrchid4", font = ("Helvetica", 24, "bold"))
        titulo.place(x = 750, y = 20)
    
        self.ruta_img = None
        self.img_tk = None

        self.label_img = tk.Label(ventana, text = "Espacio para la imagen \n la imagen debe estar entre (1000-660)", bg = "MediumPurple1")
        self.label_img.place(x = 40, y = 130, width = 1000, height = 660)

        self.label_ruta = tk.Label(ventana, text = "Ruta:", bg = "MediumPurple1")
        self.label_ruta.place(x = 40, y = 80, width = 1000, height=25)


        boton_explorar = tk.Button(ventana, text="Explorar", command=self.explorar_archivos)
        #1100 para la imagen considerar margen y 400 para el menu (sujeto a cambios)
        boton_explorar.place(x = 1100, y = 80 )

        boton_cargar = tk.Button(ventana, text="Cargar", command=self.cargar_imagen)
        boton_cargar.place(x =1180, y =80)

        #brillo
        label_brillo = tk.Label(ventana, text="Brillo:")
        label_brillo.place(x=1100, y=140)

        self.brilloS = Scale(ventana, from_=-1, to=1, resolution=0.1, orient=tk.HORIZONTAL, command=self.brillo)
        self.brilloS.place(x=1180 ,y= 120)

        #rotar sin funcion
        label_rotar = tk.Label(ventana, text="Rotar:")
        label_rotar.place(x=1100, y=190)

        self.rotarS = Scale(ventana, from_=0, to=360, resolution=1, orient=tk.HORIZONTAL)
        self.rotarS.place(x=1180 ,y= 170)

        #contraste sin funcion
        label_contraste = tk.Label(ventana, text="Contraste:")
        label_contraste.place(x=1100 , y=240)

        self.contrasteS = Scale(ventana, from_=-1, to=1, resolution=0.1, orient=tk.HORIZONTAL)
        self.contrasteS.place(x=1180 ,y= 220)

        x=intvar = tk.IntVar()

        checkZonas = tk.Checkbutton(ventana, text="Zonas oscuras", variable=x)
        checkZonas.place(x=1100, y=280)


    def explorar_archivos(self):
        ruta_img = filedialog.askopenfilename(title = "Selecciona una imagen", 
        filetypes=[("Archivos de imagen", "*.PNG *.JPG *.BMP")])
        self.ruta_img = ruta_img
        self.label_ruta.config(text = ruta_img)

    def cargar_imagen(self):
        if not self.ruta_img:
            messagebox.showwarning("Cuidado", "Primero selecciona una imagen")
            return
        img = Image.open(self.ruta_img)
        max_w, max_h = 1000, 650 #tamaño del label
        img.thumbnail((max_w, max_h)) #redimensiona la imagen
        self.img_tk = ImageTk.PhotoImage(img)
        self.label_img.config(image = self.img_tk, text = "Imagen cargada")
        self.label_img.image = self.img_tk

    def brillo(self, valor):
        img = Image.open(self.ruta_img)
        bri = float(valor)
        imgBrillo = aux.ajusteBrillo(img, bri)

        # Convertimos para tkinter
        self.img_tk = ImageTk.PhotoImage(imgBrillo)
        self.label_img.config(image=self.img_tk, text="")
        self.label_img.image = self.img_tk

    #def contraste(self,valor):





def main():
    ventana = tk.Tk()
    app = VisorImagenes(ventana)
    #crea la venta 
    ventana.mainloop()

main()




