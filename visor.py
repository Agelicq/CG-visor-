"""
Visor de Imágenes - Aplicación de procesamiento de imágenes.

Este módulo proporciona una interfaz gráfica para cargar, visualizar y aplicar
diversos ajustes y transformaciones a imágenes digitales.

Autor: Maria Angélica Alvarez Giraldo
Fecha: Octubre 2025
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog, messagebox, Scale
import ttkbootstrap as ttk
import auxVisor as aux


class VisorImagenes:
    """
    Clase principal para el visor de imágenes con capacidades de procesamiento.
    
    Esta clase crea una interfaz gráfica que permite cargar imágenes y aplicar
    diferentes transformaciones como ajustes de brillo, contraste, rotación,
    binarización, filtros de color RGB/CMY, fusión de imágenes y zoom.
    
    Attributes:
        ventana (ttk.Window): Ventana principal de la aplicación.
        ruta_img (str): Ruta de la imagen principal cargada.
        img_original (PIL.Image.Image): Imagen original sin procesar.
        img_tk (ImageTk.PhotoImage): Imagen convertida para mostrar en tkinter.
        ruta_fusion (str): Ruta de la segunda imagen para fusión.
        zoom_activo (bool): Indica si el modo zoom está activo.
    """
    
    def __init__(self, ventana):
        """
        Inicializa el visor de imágenes con todos sus componentes GUI.
        
        Args:
            ventana (ttk.Window): Ventana principal donde se montará la interfaz.
        """
        self.ventana = ventana
        self.ventana.title("Visor de imágenes")
        self.ventana.geometry("1750x950")

        # Tema general (puedes probar "flatly", "morph", "darkly", "cyborg", pulse.)
        style = ttk.Style("cosmo")


        fuente = ("Helvetica", 10)
        fuenteN = ("Helvetica", 10, "bold")

        # Personalizar todos los scales
        style.colors.set("light", "#D6D1D8FF")

        # Título
        titulo = ttk.Label(ventana, text="VISOR", font=("Helvetica", 24, "bold"), bootstyle="info")
        titulo.pack(pady=20)

        # Imagen principal
        self.label_img = ttk.Label(
            ventana,
            text="Espacio para la imagen\nLa imagen debe estar entre (1000x660)",
            anchor="center",
            bootstyle="secondary",
            background="#E9D5FF",
            font=fuente
        )
        self.label_img.place(x=40, y=130, width=1000, height=660)

        self.ruta_img = None
        self.img_original = None #imagen
        self.img_tk = None #imagen para tkinter


        # Ruta imagen
        self.label_ruta = ttk.Label(
            ventana, text="Ruta:", anchor="center",
            font=fuente, bootstyle="info", background="#E9D5FF"
        )
        self.label_ruta.place(x=40, y=80, width=1000, height=25)

        # Botones principales
        ttk.Button(ventana, text="Explorar", command=self.explorar_principal,  bootstyle="info-outline").place(x=1100, y=80)
        ttk.Button(ventana, text="Cargar", command=self.cargar_imagen,  bootstyle="info-outline").place(x=1180, y=80)

        # ----- SECCIÓN DE AJUSTES -----
        ttk.Label(ventana, text="Brillo:", font=fuente).place(x=1100, y=140)
        self.brilloS = ttk.Scale(ventana, from_=-1, to=1, command=lambda v:self.aplicar_ajustes(),bootstyle="info")
        self.brilloS.place(x=1180 ,y= 140, width=150)

        # mostrar valor slider
        self.label_brillo_val = ttk.Label(ventana, text="", foreground="#0A060E")
        self.label_brillo_val.place(x=1550, y=140)
        self.brilloS.bind("<B1-Motion>", lambda e: self.mostrar_valor_sliderfloat(e, self.brilloS, self.label_brillo_val))
        
        ttk.Label(ventana, text="Rotar:", font=fuente).place(x=1100, y=190)
        self.rotarS = ttk.Scale(ventana, from_=0, to=360,command=lambda v:self.aplicar_ajustes(), bootstyle="info")
        self.rotarS.place(x=1180, y=190, width=150)

        self.label_rotar_val = ttk.Label(ventana, text="", foreground="#0A060E")
        self.label_rotar_val.place(x=1550, y=190)
        self.rotarS.bind("<B1-Motion>", lambda e: self.mostrar_valor_sliderint(e, self.rotarS, self.label_rotar_val))

        ttk.Label(ventana, text="Contraste:", font=fuente).place(x=1100, y=240)
        self.contrasteS = ttk.Scale(ventana, from_=-1, to=1, command=lambda v:self.aplicar_ajustes(), bootstyle="info")
        self.contrasteS.place(x=1180, y=240, width=150)

        # mostrar valor slider
        self.label_contraste_val = ttk.Label(ventana, text="", foreground="#0A060E")
        self.label_contraste_val.place(x=1550, y=235)
        self.contrasteS.bind("<B1-Motion>", lambda e: self.mostrar_valor_sliderfloat(e, self.contrasteS, self.label_contraste_val))

        self.zo = ttk.BooleanVar()
        self.zc = ttk.BooleanVar()
        ttk.Checkbutton(ventana, text="Zonas oscuras", variable=self.zo, command=self.aplicar_ajustes).place(x=1400, y=230)
        ttk.Checkbutton(ventana, text="Zonas claras", variable=self.zc, command=self.aplicar_ajustes).place(x=1400, y=255)

        ttk.Label(ventana, text="Umbral\nbinarización:", font=fuente).place(x=1100, y=290)
        self.binS = ttk.Scale(ventana, from_=0, to=1, command=lambda v:self.aplicar_ajustes(), bootstyle="info")
        self.binS.place(x=1180, y=290, width=150)

        # mostrar valor slider
        self.label_bin_val = ttk.Label(ventana, text="", foreground="#0A060E")
        self.label_bin_val.place(x=1550, y=285)
        self.binS.bind("<B1-Motion>", lambda e: self.mostrar_valor_sliderfloat(e, self.binS, self.label_bin_val))

        # Check negativo
        self.neg = ttk.BooleanVar()
        ttk.Checkbutton(ventana, text="Negativo", variable=self.neg, command=self.aplicar_ajustes).place(x=1100, y=340)

        # ----- RGB / CMY -----
        ttk.Label(ventana, text="RGB:", font=fuenteN, foreground="#4B0082").place(x=1100, y=370)
        self.rojo = ttk.BooleanVar()
        self.verde = ttk.BooleanVar()
        self.azul = ttk.BooleanVar()
        ttk.Checkbutton(ventana, text="Capa Roja", variable=self.rojo, command=self.aplicar_ajustes).place(x=1100, y=395)
        ttk.Checkbutton(ventana, text="Capa Verde", variable=self.verde, command=self.aplicar_ajustes).place(x=1100, y=420)
        ttk.Checkbutton(ventana, text="Capa Azul", variable=self.azul, command=self.aplicar_ajustes).place(x=1100, y=445)

        ttk.Label(ventana, text="CMY:", font=fuenteN, foreground="#4B0082").place(x=1350, y=370)
        self.cian = ttk.BooleanVar()
        self.magenta = ttk.BooleanVar()
        self.amarillo = ttk.BooleanVar()
        ttk.Checkbutton(ventana, text="Capa Cian", variable=self.cian, command=self.aplicar_ajustes).place(x=1350, y=395)
        ttk.Checkbutton(ventana, text="Capa Magenta", variable=self.magenta, command=self.aplicar_ajustes).place(x=1350, y=420)
        ttk.Checkbutton(ventana, text="Capa Amarillo", variable=self.amarillo, command=self.aplicar_ajustes).place(x=1350, y=445)

        # ----- FUSIÓN -----
        ttk.Label(ventana, text="Fusionar:", font=fuenteN, foreground="#4B0082").place(x=1100, y=490)
        ttk.Button(ventana, text="1. Cargar segunda imagen", command=self.explorar_fusion, bootstyle="info-outline").place(x=1100, y=515)

        self.rutaFusionlabel = ttk.Label(ventana, text="Ruta segunda imagen:", bootstyle="info", background="#E9D5FF")
        self.rutaFusionlabel.place(x=1350, y=520, width=150, height=20)

        ttk.Label(ventana, text="2. Ajustar transparencia", font=fuente).place(x=1100, y=560)
        self.fusS = ttk.Scale(ventana, from_=0, to=1, command=lambda v:self.aplicar_ajustes(), bootstyle="info")
        self.fusS.place(x=1350, y=560, width=150)

        # mostrar valor slider
        self.label_fus_val = ttk.Label(ventana, text="", foreground="#0A060E")
        self.label_fus_val.place(x=1550, y=560)
        self.fusS.bind("<B1-Motion>", lambda e: self.mostrar_valor_sliderfloat(e, self.fusS, self.label_fus_val))

        # ----- OTRAS FUNCIONES -----
        ttk.Button(ventana, text="Zoom área", command=self.activar_zoom_area, bootstyle="info-outline").place(x=1100, y=610)
        ttk.Button(ventana, text="Histograma", command=self.histo, bootstyle="info-outline").place(x=1100, y=650)

        # ----- BOTONES INFERIORES -----
        ttk.Button(ventana, text="Restaurar", command=self.cargar_imagen,  bootstyle="info-outline").place(x=1400, y=750)
        ttk.Button(ventana, text="Guardar", command=self.guardar,  bootstyle="info-outline").place(x=1500, y=750)

    
    def mostrar_valor_sliderfloat(self, event, slider, label):
        """
        Actualiza y muestra el valor flotante de un slider en tiempo real.
        
        Args:
            event: Evento del mouse al mover el slider.
            slider (ttk.Scale): Widget slider del que obtener el valor.
            label (ttk.Label): Etiqueta donde mostrar el valor.
        """
        valor = slider.get()
        label.place(x=slider.winfo_x() + slider.winfo_width() + 10,
                    y=slider.winfo_y())
        label.config(text=f"{valor:.1f}")

    def mostrar_valor_sliderint(self, event, slider, label):
        """
        Actualiza y muestra el valor entero de un slider en tiempo real.
        
        Args:
            event: Evento del mouse al mover el slider.
            slider (ttk.Scale): Widget slider del que obtener el valor.
            label (ttk.Label): Etiqueta donde mostrar el valor.
        """
        valor = slider.get()
        label.place(x=slider.winfo_x() + slider.winfo_width() + 10,
                    y=slider.winfo_y())
        label.config(text=f"{valor:.0f}")

#metodos de carga
    def explorar_archivos(self):
        """
        Abre un cuadro de diálogo para seleccionar un archivo de imagen.
        
        Returns:
            str: Ruta del archivo de imagen seleccionado.
        """
        ruta_img = filedialog.askopenfilename(title = "Selecciona una imagen", 
        filetypes=[("Archivos de imagen", "*.PNG *.JPG *.BMP")])
        return ruta_img
    
    def explorar_principal(self):
        """
        Selecciona y establece la ruta de la imagen principal.
        
        Actualiza la etiqueta de ruta con la imagen seleccionada.
        """
        ruta_img = self.explorar_archivos()
        self.ruta_img = ruta_img
        self.label_ruta.config(text = ruta_img)

    def explorar_fusion(self):
        """
        Selecciona una segunda imagen para fusionar con la principal.
        
        Verifica que haya una imagen principal cargada antes de permitir
        la selección de la segunda imagen.
        """
        if not self.ruta_img:
            messagebox.showwarning("Cuidado", "Primero selecciona una imagen principal")
            return
        ruta2 = self.explorar_archivos()
        self.ruta_fusion = ruta2
        self.rutaFusionlabel.config(text = ruta2)

    def cargar_imagen(self):
        """
        Carga la imagen principal en el visor y restablece los ajustes.
        
        Redimensiona la imagen para que quepa en el área de visualización
        y resetea todos los controles a sus valores por defecto.
        """
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
        """
        Guarda la imagen procesada con todos los ajustes aplicados.
        
        Abre un cuadro de diálogo para seleccionar el nombre y formato
        del archivo de salida (JPG, PNG o BMP).
        """
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
        """
        Restablece todos los controles y ajustes a sus valores por defecto.
        
        Resetea sliders, checkboxes y la ruta de fusión a sus estados iniciales.
        """
        self.ruta_fusion = None
        self.rutaFusionlabel.config(text = "ruta segunda imagen:")
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
        """
        Aplica ajuste de contraste a la imagen.
        
        Permite ajustar el contraste priorizando zonas oscuras o claras
        según las opciones seleccionadas.
        
        Args:
            img (PIL.Image.Image): Imagen a la que aplicar el contraste.
            
        Returns:
            PIL.Image.Image: Imagen con el contraste ajustado, o None si hay error.
        """
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
        """
        Fusiona la imagen principal con una segunda imagen.
        
        Aplica transparencia para mezclar ambas imágenes. Verifica que
        ambas imágenes tengan el mismo tamaño.
        
        Args:
            img (PIL.Image.Image): Imagen base para la fusión.
            
        Returns:
            PIL.Image.Image: Imagen fusionada o la imagen original si hay error.
        """
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
        """
        Muestra histogramas de las capas RGB de la imagen.
        
        Genera una ventana con tres histogramas mostrando la distribución
        de intensidades para cada canal de color.
        """
        if not self.img_original:
            messagebox.showwarning("Cuidado", "Primero selecciona una imagen principal")
            return
        img = self.img_original.copy()
        aux.histogramas(img)

    
    #zoom 
    def activar_zoom_area(self):
        """
        Activa el modo de selección de área para zoom.
        
        Permite al usuario dibujar un rectángulo sobre la imagen para
        hacer zoom en esa región específica.
        """
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
        """
        Inicia el dibujo del rectángulo de selección para zoom.
        
        Args:
            event: Evento del mouse con las coordenadas iniciales.
        """
        self.zoom_start = (int(event.x), int(event.y))
        self.zoom_rect = None

    def dibujar_recuadro(self, event):
        """
        Dibuja el rectángulo de selección mientras el usuario arrastra el mouse.
        
        Actualiza visualmente el área seleccionada en tiempo real.
        
        Args:
            event: Evento del mouse con las coordenadas actuales.
        """
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
        """
        Aplica el zoom a la región seleccionada.
        
        Corta y redimensiona la región seleccionada para llenar el área
        de visualización. Valida que la selección sea suficientemente grande.
        
        Args:
            event: Evento del mouse al soltar el botón.
        """
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
        """
        Rota la imagen por el ángulo especificado.
        
        Args:
            img (PIL.Image.Image): Imagen a rotar.
            ang (float): Ángulo de rotación en grados.
            
        Returns:
            PIL.Image.Image: Imagen rotada.
        """
        pil = img if isinstance(img, Image.Image) else Image.fromarray(img.astype(np.uint8))
        return pil.rotate(ang, resample=Image.BICUBIC, expand=True)


    #metodo central(aplica todos los ajustes)
    def aplicar_ajustes(self):
        """
        Aplica todos los ajustes y transformaciones seleccionados a la imagen.
        
        Este es el método central que procesa la imagen aplicando en secuencia:
        brillo, contraste, rotación, binarización, filtros RGB/CMY, negativo
        y fusión. Actualiza la visualización con la imagen procesada.
        
        Returns:
            PIL.Image.Image: Imagen con todos los ajustes aplicados, o None si no hay imagen.
        """
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
    """
    Función principal que inicia la aplicación.
    
    Crea la ventana principal y ejecuta el loop de eventos de tkinter.
    """
    app = ttk.Window(themename="")
    visor = VisorImagenes(app)
    app.mainloop()

main()



