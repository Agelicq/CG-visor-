import matplotlib.pyplot as plt
import numpy as np

img1 = plt.imread("imagenes/kero.jpg")

def ajusteContraste(img, contraste, tipo):
    #1 zonas oscuras en detrimento de las claras
    #2 zonas claras en detrimento de las oscuras 
    img = img/255

    if tipo == 1:
        imgContraste1 = contraste*np.log10(1+img)
        plt.imshow(imgContraste1)
        plt.show()

    elif tipo == 2:
        imgContraste2 = contraste*np.exp(img-1)
        plt.imshow(imgContraste2)
        plt.show()

ajusteContraste(img1, 1, 1)