import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
#PIL es la libreria para trabajar con imagenes con tkinter
from tkinter import filedialog, messagebox, Scale
import auxVisor as aux
import matplotlib.pyplot as plt
"""
falta documentar y manual de usuario
"""

fuente = ("Helvetica", 10)
fuenteN = ("Helvetica", 10, "bold")

class VisorImagenes:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Visor de imagenes")
        #redimeniona la ventana 1500x1500
        self.ventana.geometry("1750x950")

        titulo = tk.Label(ventana, text="VISOR", fg = "DarkOrchid4", font = ("Helvetica", 24, "bold"))
        titulo.pack(pady = 20)
    
        self.ruta_img = None
        self.img_original = None #imagen
        self.img_tk = None #imagen para tkinter

        self.label_img = tk.Label(ventana, font=fuente, text="Espacio para la imagen \n la imagen debe estar entre (1000-660)",
                                bg = "MediumPurple1")
        self.label_img.place(x = 40, y = 130, width = 1000, height = 660)

        self.label_ruta = tk.Label(ventana, font= fuente, text = "Ruta:", bg = "MediumPurple1")
        self.label_ruta.place(x = 40, y = 80, width = 1000, height=25)


        boton_explorar = tk.Button(ventana, text="Explorar", font=fuenteN, command=self.explorar_principal)
        #1100 para la imagen considerar margen y 400 para el menu (sujeto a cambios)
        boton_explorar.place(x = 1100, y = 80 )

        # cargar imagen
        boton_cargar = tk.Button(ventana, text="Cargar", font=fuenteN, command=self.cargar_imagen)
        boton_cargar.place(x =1180, y =80)

        #brillo
        label_brillo = tk.Label(ventana, font=fuente, text="Brillo:")
        label_brillo.place(x=1100, y=140)

        #usamos lmbda v: para descartar el valor que retorna el slide
        self.brilloS = Scale(ventana, from_=-1, to=1, resolution=0.1, orient=tk.HORIZONTAL, command=lambda v:self.aplicar_ajustes())
        self.brilloS.place(x=1180 ,y= 120)

        #rotar sin funcion
        label_rotar = tk.Label(ventana, font=fuente, text="Rotar:")
        label_rotar.place(x=1100, y=190)

        self.rotarS = Scale(ventana, from_=0, to=360, resolution=1, orient=tk.HORIZONTAL, command=lambda v:self.aplicar_ajustes())
        self.rotarS.place(x=1180 ,y= 170)

        #contraste
        label_contraste = tk.Label(ventana, font=fuente, text="Contraste:")
        label_contraste.place(x=1100 , y=240)

        self.contrasteS = Scale(ventana, from_=-1, to=1, resolution=0.1, orient=tk.HORIZONTAL, command=lambda v:self.aplicar_ajustes())
        self.contrasteS.place(x=1180 ,y= 220)

        self.zo=tk.BooleanVar()
        self.zc=tk.BooleanVar()

        checkZonaOscura = tk.Checkbutton(ventana, text="Zonas oscuras", font=fuente, activebackground ="MediumPurple1", variable=self.zo, 
                                        command=self.aplicar_ajustes)
        checkZonaOscura.place(x=1300, y=220)

        checkZonasClaras= tk.Checkbutton(ventana, text="Zonas claras", font=fuente, activebackground ="MediumPurple1", variable=self.zc, 
                                        command=self.aplicar_ajustes)
        checkZonasClaras.place(x=1300, y=245)

        #binarizacion con slider
        label_bin = tk.Label(ventana, font=fuente, text="Umbral \nbinarizacion:")
        label_bin.place(x=1100, y=280)

        self.binS = Scale(ventana, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, command= lambda v:self.aplicar_ajustes())
        self.binS.place(x=1180 ,y= 270)

        #capas RGB
        self.rojo = tk.BooleanVar()
        self.verde = tk.BooleanVar()
        self.azul = tk.BooleanVar()
        
        RGBlabel = tk.Label(ventana, text= "RGB:",fg = "DarkOrchid4", font = fuenteN)
        RGBlabel.place(x=1100, y=355)

        checkRojo = tk.Checkbutton(ventana, font = fuente, text = "Capa Roja", variable = self.rojo, command=self.aplicar_ajustes)
        checkRojo.place(x = 1100, y = 375)

        checkVerde = tk.Checkbutton(ventana, font = fuente, text = "Capa Verde", variable = self.verde, command=self.aplicar_ajustes)
        checkVerde.place(x = 1100, y = 400)

        checkAzul = tk.Checkbutton(ventana, font = fuente, text = "Capa Azul", variable = self.azul, command=self.aplicar_ajustes)
        checkAzul.place(x = 1100, y = 425)

        #canales CMY
        self.cian = tk.BooleanVar()
        self.magenta = tk.BooleanVar()
        self.amarillo = tk.BooleanVar()

        CMYlabel = tk.Label(ventana, text= "CMY:",fg = "DarkOrchid4", font = fuenteN)
        CMYlabel.place(x=1300, y=355)

        checkCian = tk.Checkbutton(ventana, font = fuente, text = "Capa Cian", variable = self.cian, command=self.aplicar_ajustes)
        checkCian.place(x = 1300, y = 375)

        checkMagenta = tk.Checkbutton(ventana, font = fuente, text = "Capa Magenta", variable = self.magenta, command=self.aplicar_ajustes)
        checkMagenta.place(x = 1300, y = 400)

        checkAmarillo = tk.Checkbutton(ventana, font = fuente, text = "Capa Amarillo", variable = self.amarillo, command=self.aplicar_ajustes)
        checkAmarillo.place(x = 1300, y = 425)

        #negativo (me gustaria moverlo)
        self.neg = tk.BooleanVar()
        checkNegativo = tk.Checkbutton(ventana, font = fuente, text = "Negativo", variable=self.neg, command=self.aplicar_ajustes)
        checkNegativo.place(x = 1100, y = 325)

        #fusionar
        fusionlabel = tk.Label(ventana, font = fuenteN, text= "Fusionar: ", fg = "DarkOrchid4")
        fusionlabel.place(x=1100, y=470)

        boton_cargarSegunda = tk.Button(ventana, font = fuente, text="1. Cargar segunda imagen", command=self.explorar_fusion)
        boton_cargarSegunda.place(x = 1100, y = 500)

        self.ruta_fusion = None
        self.rutaFusionlabel = tk.Label(ventana, font = fuente, text="Ruta segunda imagen:", bg = "MediumPurple1")
        self.rutaFusionlabel.place(x = 1300, y = 500, width = 250, height=20)

        label_fus = tk.Label(ventana, font = fuente, text="2. Ajustar transparencia")
        label_fus.place(x=1100, y=540)
        self.fusS = Scale(ventana, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, command=lambda v:self.aplicar_ajustes())
        self.fusS.place(x=1300 ,y= 520)

        #zoom
        boton_zoom = tk.Button(ventana, font = fuente, text="Zoom área", command = self.activar_zoom_area)
        boton_zoom.place(x = 1100, y = 600)

        #histograma
        boton_histograma = tk.Button(ventana, font = fuente, text="Histograma", command=self.histo)
        boton_histograma.place(x = 1100, y = 640)

        #restaurar
        boton_restaurar = tk.Button(ventana, font = fuenteN, text="Restaurar",bg = "MediumPurple1", command=self.cargar_imagen)
        boton_restaurar.place(x = 1400, y = 750)

        #guardar
        boton_guardar = tk.Button(ventana, font = fuenteN, text="Guardar", bg = "MediumPurple1", command=self.guardar)
        boton_guardar.place(x = 1500, y = 750)


#metodos de carga
    def explorar_archivos(self):
        ruta_img = filedialog.askopenfilename(title = "Selecciona una imagen", 
        filetypes=[("Archivos de imagen", "*.PNG *.JPG *.BMP")])
        return ruta_img
    
    def explorar_principal(self):
        ruta_img = self.explorar_archivos()
        self.ruta_img = ruta_img
        self.label_ruta.config(text = ruta_img)

    def explorar_fusion(self):
        if not self.ruta_img:
            messagebox.showwarning("Cuidado", "Primero selecciona una imagen principal")
            return
        ruta2 = self.explorar_archivos()
        self.ruta_fusion = ruta2
        self.rutaFusionlabel.config(text = ruta2)

    def cargar_imagen(self):
        if not self.ruta_img:
            messagebox.showwarning("Cuidado", "Primero selecciona una imagen")
            return
        self.img_original = Image.open(self.ruta_img)
        max_w, max_h = 1000, 650 #tamaño del label
        self.img_original.thumbnail((max_w, max_h)) #redimensiona la imagen

        self.img_tk = ImageTk.PhotoImage(self.img_original.copy())
        self.label_img.config(image = self.img_tk, text = "Imagen cargada")
        self.label_img.image = self.img_tk

        #resetea los ajustes
        self.reset()

    def guardar(self):
        if not self.img_original:
            messagebox.showwarning("Cuidado", "Primero selecciona una imagen principal")
            return
        
        img_proc = self.aplicar_ajustes()
        save_img = filedialog.asksaveasfilename(defaultextension=".jpg",
            filetypes=[("Archivos JPG", "*.jpg"), ("Archivos PNG", "*.png"), ("Archivos BMP", "*.bmp")]
            )
        if save_img:
            img_proc.save(save_img)

    def reset(self):
        self.ruta_fusion = None
        self.rutaFusionlabel.config(font=fuente,text = "ruta segunda imagen:")
        self.brilloS.set(0)
        self.contrasteS.set(0)
        self.rotarS.set(0)
        self.binS.set(0)
        self.fusS.set(0)
        self.zc.set(False)
        self.zo.set(False)
        self.cian.set(False)
        self.magenta.set(False)
        self.amarillo.set(False)
        self.rojo.set(False)
        self.verde.set(False)
        self.azul.set(False)
        self.neg.set(False)
        

    def contraste(self, img):
        cont = self.contrasteS.get()
        if self.zo.get() and self.zc.get():
            messagebox.showwarning("Cuidado", "No se puede aplicar ambos ajustes a la vez")
            return
        if self.zo.get() == True:
            img = aux.ajusteContraste(img, cont, 1)
        elif self.zc.get() == True:
            img = aux.ajusteContraste(img, cont, 2)
        return img
    
    
    def fusion(self, img):
        if self.ruta_fusion:
            try:
                img2 = Image.open(self.ruta_fusion)
            except Exception:
                messagebox.showwarning("Cuidado", "No se pudo abrir la segunda imagen")
                img2 = None

            if img2 is not None:
                # Comprobar tamaños (y canales) antes de fusionar
                # Convertir a un modo común para comparar canales (usar RGB)
                img_check = img.convert('RGB') if isinstance(img, Image.Image) else img
                img2_check = img2.convert('RGB')

                if img_check.size != img2_check.size:
                    # Mostrar advertencia pero no interrumpir otras operaciones
                    messagebox.showwarning("Cuidado", "Las imágenes no tienen el mismo tamaño")
                else:
                    transparencia = float(self.fusS.get())
                    imgFusion = aux.fusionImgEcualizada(img_check, img2_check, transparencia)
                    if imgFusion is None:
                        messagebox.showwarning("Cuidado", "Error al fusionar las imágenes")
                    else:
                        img = imgFusion
                        return img

    def histo(self):
        if not self.img_original:
            messagebox.showwarning("Cuidado", "Primero selecciona una imagen principal")
            return
        img = self.img_original.copy()
        aux.histogramas(img)

    
    #zoom 
    def activar_zoom_area(self):
        if not self.img_original:
            messagebox.showwarning("Cuidado", "Primero selecciona una imagen principal")
            return

        # Asegurar que la imagen procesada esté actualizada
        img_proc = self.aplicar_ajustes()
        if img_proc is None:
            return

        self.zoom_activo = True
        self.zoom_start = None
        self.zoom_rect = None
        # Bind eventos al label
        self.label_img.bind("<Button-1>", self.iniciar_recuadro)
        self.label_img.bind("<B1-Motion>", self.dibujar_recuadro)
        self.label_img.bind("<ButtonRelease-1>", self.aplicar_zoom_area)
        self.label_img.configure(cursor="crosshair")


    def iniciar_recuadro(self, event):
        self.zoom_start = (int(event.x), int(event.y))
        self.zoom_rect = None

    def dibujar_recuadro(self, event):
        if not getattr(self, 'zoom_activo', False) or self.zoom_start is None:
            return
        x1, y1 = self.zoom_start
        x2, y2, = int(event.x), int(event.y)

        proc = self.aplicar_ajustes()
        if proc is None:
            return
        
        overlay, offsets = aux.overlay(proc, (1000, 660), (x1, y1, x2, y2))
        if overlay is None:
            return
        
        self.img_tk = ImageTk.PhotoImage(overlay)
        self.label_img.config(image=self.img_tk)
        self.label_img.image = self.img_tk

        self.zoom_rect = (x1, y1, x2, y2)
        self.zoom_offsets = offsets

    def aplicar_zoom_area(self, event):
        if not getattr(self, 'zoom_activo', False) or not self.zoom_rect:
            # limpiar bindings por si acaso
            try:
                self.label_img.unbind("<Button-1>")
                self.label_img.unbind("<B1-Motion>")
                self.label_img.unbind("<ButtonRelease-1>")
                self.label_img.configure(cursor="")
            except Exception:
                pass
            self.zoom_activo = False
            return

        x1, y1, x2, y2 = self.zoom_rect
        if abs(x2 - x1) < 10 or abs(y2 - y1) < 10:
            messagebox.showinfo("Zoom", "Selecciona un área más grande.")
            # restaurar imagen procesada
            proc = self.aplicar_ajustes()
            if proc:
                self.img_tk = ImageTk.PhotoImage(proc)
                self.label_img.config(image=self.img_tk)
                self.label_img.image = self.img_tk
            try:
                self.label_img.unbind("<Button-1>")
                self.label_img.unbind("<B1-Motion>")
                self.label_img.unbind("<ButtonRelease-1>")
                self.label_img.configure(cursor="")
            except Exception:
                pass
            self.zoom_activo = False
            self.zoom_rect = None
            return

        proc = self.aplicar_ajustes()
        if proc is None:
            return

        region_zoom = aux.cortar_redimensionar(proc, self.zoom_offsets, self.zoom_rect, (1000,660))
        if region_zoom is None:
            messagebox.showinfo("Zoom", "Área inválida.")
            self.zoom_activo = False
            self.zoom_rect = None
            try:
                self.label_img.unbind("<Button-1>")
                self.label_img.unbind("<B1-Motion>")
                self.label_img.unbind("<ButtonRelease-1>")
                self.label_img.configure(cursor="")
            except Exception:
                pass
            return

        self.img_tk = ImageTk.PhotoImage(region_zoom)
        self.label_img.config(image=self.img_tk)
        self.label_img.image = self.img_tk

        # limpiar bindings
        try:
            self.label_img.unbind("<Button-1>")
            self.label_img.unbind("<B1-Motion>")
            self.label_img.unbind("<ButtonRelease-1>")
            self.label_img.configure(cursor="")
        except Exception:
            pass

        self.zoom_activo = False
        self.zoom_rect = None

    def rotar(self,img, ang):
        pil = img if isinstance(img, Image.Image) else Image.fromarray(img.astype(np.uint8))
        return pil.rotate(ang, resample=Image.BICUBIC, expand=True)


    #metodo central(aplica todos los ajustes)
    def aplicar_ajustes(self):
        if not self.img_original:
            messagebox.showwarning("Cuidado", "Primero selecciona una imagen principal")
            return
        img = self.img_original.copy()

        if self.brilloS.get() != 0:
            bri = self.brilloS.get()
            img = aux.ajusteBrillo(img, bri)

        if self.contrasteS.get() != 0:
            img = self.contraste(img)

        if self.rotarS.get() != 0:
            ang = self.rotarS.get()
            img = self.rotar(img, ang)
            #img = aux.rotar_imagen(img, ang) en caso de usar rotar de la funcion aux


        if self.binS.get() != 0:
            umbral = self.binS.get()
            img = aux.binarizar(img, umbral)

        #mezcla RGB
        if self.rojo.get() and self.verde.get() and self.azul.get() == True:
            img = self.img_original
        elif self.rojo.get() and self.azul.get() == True:
            img = aux.canalMagenta(img)
        elif self.rojo.get() and self.verde.get() == True:
            img = aux.canalAmarillo(img)
        elif self.verde.get() and self.azul.get() == True:
            img = aux.canalCian(img)
        elif self.verde.get() == True:
            img = aux.capaVerde(img)
        elif self.rojo.get() == True:
            img = aux.capaRoja(img)
        elif self.azul.get() == True:
            img = aux.capaAzul(img)

        #mezcla CMY
        if self.cian.get() and self.magenta.get() and self.amarillo.get() == True:
            img = aux.negroConceptual(img)
        elif self.cian.get() and self.magenta.get() == True:
            img = aux.capaAzul(img)
        elif self.cian.get() and self.amarillo.get() == True:
            img = aux.capaVerde(img)
        elif self.magenta.get() and self.amarillo.get() == True:
            img = aux.capaRoja(img)
        elif self.cian.get() == True:
            img = aux.canalCian(img)
        elif self.magenta.get() == True:
            img = aux.canalMagenta(img)
        elif self.amarillo.get() == True:
            img = aux.canalAmarillo(img)

        if self.neg.get() == True:
            img = aux.negativo(img)

        #fusion
        if self.fusS.get() >= 0 and self.ruta_fusion:
            img = self.fusion(img)

        self.img_tk = ImageTk.PhotoImage(img)
        self.label_img.config(image=self.img_tk, text="")
        self.label_img.image = self.img_tk

        return img

def main():
    ventana = tk.Tk()
    app = VisorImagenes(ventana)
    #crea la ventana
    ventana.mainloop()

main()




