import numpy as np
import matplotlib.pyplot as plt
#import auximagenes as aux
from PIL import Image, ImageTk
import tkinter as tk

img1 = plt.imread("imagenes/chimuelo.jpg")
img0 = plt.imread("imagenes/imagen1.jpg")
img2 = plt.imread("imagenes/imagen2.jpg")


def histogramas(img):
    img = np.array(img)
    if img.max() <= 1:
        img = (img * 255).astype(np.uint8)

    rojo = img[...,0]
    azul = img[...,1]
    verde = img[...,2]

    plt.figure("Histograma de las capas")
    #rojo
    plt.subplot(1,3,1)
    plt.hist(rojo.ravel(), bins=256, color='red', alpha=0.7) 
    plt.title("capa roja")
    plt.xlabel("intensidad")
    plt.ylabel("frecuencia")
    #azul
    plt.subplot(1,3,2)
    plt.hist(azul.ravel(), bins=256, color='blue', alpha=0.7) 
    plt.title("capa azul")
    plt.xlabel("intensidad")
    plt.ylabel("frecuencia")
    #verde
    plt.subplot(1,3,3)
    plt.hist(verde.ravel(), bins=256, color='green', alpha=0.7) 
    plt.title("capa verde")
    plt.xlabel("intensidad")
    plt.ylabel("frecuencia")

    plt.tight_layout()
    plt.show()

histogramas(img1)


def zoom(img):
    imgArray = np.array(img)
    h, w = imgArray.shape[:2] #extraer solo el ancho y el alto de la imagen
    #h -> hight alto
    #w -> width ancho
    zoomArea = 500
    #filas
    startRow = h // 2 - zoomArea // 2
    endRow = h // 2 + zoomArea // 2
    #columas 
    starCol = w // 2 - zoomArea // 2
    endCol = w // 2 + zoomArea // 2

    recorte = img[startRow:endRow, starCol:endCol]
    factor = 2
    zoomImg = np.kron(recorte, np.ones((factor, factor, 1)))

    plt.figure("zoom en una imagen")
    plt.subplot(1,2,1)
    plt.axis('off')
    plt.title("imagen original")
    plt.imshow(img)

    plt.subplot(1,2,2)
    plt.axis('off')
    plt.title("zoom")
    plt.imshow(zoomImg)
    plt.show()

#zoom(img1)
