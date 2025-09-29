import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from PIL import Image, ImageTk
#PIL es la libreria para trabajar con imagenes con tkinter
from tkinter import filedialog, messagebox


def ajusteBrillo(img, brillo):
    imgArray = np.array(img, dtype = np.float32) #convierte la imagen a un array de numpy
    imgArray = imgArray / 255
    imgBrillo = imgArray + brillo
    return Image.fromarray((imgBrillo*255).astype(np.uint8))

def ajusteContraste(img, contraste, tipo):
    #1 zonas oscuras en detrimento de las claras
    #2 zonas claras en detrimento de las oscuras 
    imgArray = np.array(img, dtype = np.float32) 
    imgArray = imgArray / 255

    if tipo == 1:
        imgContraste1 = contraste*np.log10(1+imgArray)
        return Image.fromarray((imgContraste1*255).astype(np.uint8))
        

    elif tipo == 2:
        imgContraste2 = contraste*np.exp(imgArray-1)
        return Image.fromarray((imgContraste2*255).astype(np.uint8))    