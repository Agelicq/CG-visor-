import numpy as np
import matplotlib.pyplot as plt


img1 = plt.imread("imagenes/imagen1.jpg")/255
img2 = plt.imread("imagenes/imagen2.jpg")/255

def fusionImg(img1, img2):
    img3 = img1 + img2
    plt.imshow(img3)
    plt.show()

fusionImg(img1, img2)

def fusionImgEcualizada(img1, img2, factor):
    plt.figure("Fusion de imagenes ")
    plt.subplot(1,3,1) #todos es una fila, tres columnas, y este es el primero
    plt.title("Paisaje")
    plt.axis('off')
    img1 = plt.imread("imagen1.jpg")/255
    plt.imshow(img1)

    plt.subplot(1,3,2)
    plt.title("Tomoe")
    plt.axis('off')
    img2 = plt.imread("imagen2.jpg")/255
    plt.imshow(img2)

    #fusinamos
    plt.subplot(1,3,3)
    plt.title("Fusion")
    plt.axis('off')
    img3 = (img1*factor +img2*(1-factor))
    plt.imshow(img3)
    plt.show()

def ecualizador(img, factor):
    plt.figure("Imagen ecualizada")
    plt.subplot(1,2,1)
    plt.axis('off')
    plt.title("original")
    plt.imshow(img)

    imgE = img*factor
    plt.subplot(1,2,2)
    plt.axis('off')
    plt.title("Ecualizada")
    plt.imshow(imgE)
    plt.show()


def zoom(img):
    h, w = img.shape[:2] #extraer solo el ancho y el alto de la imagen
    #h -> hight alto
    #w -> width ancho
    zoomArea = 1000
    #filas
    startRow = h // 2 - zoomArea // 2
    endRow = h // 2 + zoomArea // 2
    #columas 
    starCol = w // 2 - zoomArea // 2
    endCol = w // 2 + zoomArea // 2

    recorte = img[startRow:endRow, starCol:endCol]
    factor = 5
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

def histogramas(img):
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

#histogramas(img2)