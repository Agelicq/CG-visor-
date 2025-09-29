def invertir(img):
    plt.figure("escala de grises")
    plt.subplot(1,2,1)
    plt.axis('off')
    plt.title("original")
    plt.imshow(img)

    imgN = 1 - img
    plt.subplot(1,2,2)
    plt.axis('off')
    plt.title('negativo')
    plt.imshow(imgN)
    plt.show()

def capaRoja(img):
    imgC = np.copy(img)
    imgC[:,:,1] = imgC[:,:,2] = 0
    return imgC

def capaVerde(img):
    imgC = np.copy(img)
    imgC[:,:,0] = imgC[:,:,2] = 0
    return imgC

def capaAzul(img):
    imgC = np.copy(img)
    imgC[:,:,0] = imgC[:,:,1] = 0
    return imgC

def canalCian(img):
    imgC = np.copy(img)
    imgC[:,:,1] = imgC[:,:,2] = 1
    return imgC

def canalMagenta(img):
    imgC = np.copy(img)
    imgC[:,:,0] = imgC[:,:,2] = 1
    return imgC

def canalAmarillo(img):
    imgC = np.copy(img)
    imgC[:,:,0] = imgC[:,:,1] = 1
    return imgC

def fusionarCapas(img):
    imgR = capaRoja(img)
    imgV = capaVerde(img)
    imgA = capaAzul(img)
    #suma de capas
    plt.figure("suma de capas")
    plt.subplot(2,2,1)
    plt.axis('off')
    plt.title('R+V+A')
    imgRVA = imgR+imgV+imgA
    plt.imshow(imgRVA)

    plt.subplot(2,2,2)
    plt.axis('off')
    plt.title("capa roja")
    plt.imshow(imgR)

    plt.subplot(2,2,3)
    plt.axis('off')
    plt.title("capa azul")
    plt.imshow(imgA)

    plt.subplot(2,2,4)
    plt.axis('off')
    plt.title("capa verde")
    plt.imshow(imgV)
    plt.show()

def fusionImg(img1, img2):
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
    img3 = img1 + img2
    plt.imshow(img3)
    plt.show()

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

def average(img):
    plt.figure("average")
    plt.subplot(1,2,1)
    plt.axis('off')
    plt.title("original")
    plt.imshow(img)

    plt.subplot(1,2,2)
    plt.axis('off')
    plt.title("average")
    imgC = np.copy(img)
    imgGray = (imgC[:,:,0]+imgC[:,:,1]+imgC[:,:,2])/3
    plt.imshow(imgGray, cmap='gray')
    plt.show()



def ajusteContraste(img, contraste):
    #tipo hacia parte de las variables pero no lo considere necesario
    #1 zonas oscuras en detrimento de las claras
    #2 zonas claras en detrimento de las oscuras 
    plt.figure("Ajuste de contraste ")
    plt.subplot(1,3,1)
    plt.axis('off')
    plt.title("original")
    plt.imshow(img1)

    plt.subplot(1,3,2)
    plt.axis('off')
    imgContraste1 = contraste*np.log10(1+img)
    plt.title(" zonas oscuras ")
    plt.imshow(imgContraste1)

    plt.subplot(1,3,3)
    plt.axis('off')
    imgContraste2 = contraste*np.exp(img-1)
    plt.title(" zonas claras")
    plt.imshow(imgContraste2)
    plt.show()