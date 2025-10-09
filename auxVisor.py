import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

#Funciones auxiliares para el visor de imagenes

def ajusteBrillo(img, brillo):
    imgArray = np.array(img)  # convierte la imagen a un array de numpy
    imgArray = imgArray/255
    imgBrillo = imgArray + brillo
    imgBrillo = np.clip(imgBrillo, 0, 1) #evita saturacion
    return Image.fromarray((imgBrillo * 255).astype(np.uint8))

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

def capaRoja(img):
    imgArray = np.array(img, dtype=np.float32)
    imgArray = imgArray / 255
    #imgArray = np.copy(img)
    imgArray[:,:,1] = imgArray[:,:,2] = 0
    return Image.fromarray((imgArray * 255).astype(np.uint8))

def capaVerde(img):
    imgArray = np.array(img, dtype = np.float32)
    imgArray = imgArray/255
    imgArray[:,:,0] = imgArray[:,:,2] = 0
    return Image.fromarray((imgArray * 255).astype(np.uint8))

def capaAzul(img):
    imgArray = np.array(img, dtype = np.float32)
    imgArray = imgArray/255
    imgArray[:,:,0] = imgArray[:,:,1] = 0
    return Image.fromarray((imgArray * 255).astype(np.uint8))

def canalCian(img):
    imgArray = np.array(img, dtype = np.float32)
    imgArray = imgArray/255
    imgArray[:,:,1] = imgArray[:,:,2] = 1
    return Image.fromarray((imgArray * 255).astype(np.uint8))

def canalMagenta(img):
    imgArray = np.array(img, dtype = np.float32)
    imgArray = imgArray/255
    imgArray[:,:,0] = imgArray[:,:,2] = 1
    return Image.fromarray((imgArray * 255).astype(np.uint8))

def canalAmarillo(img):
    imgArray = np.array(img, dtype = np.float32)
    imgArray = imgArray/255
    imgArray[:,:,0] = imgArray[:,:,1] = 1
    return Image.fromarray((imgArray * 255).astype(np.uint8))

def negroConceptual(img):
    imgArray = np.array(img, dtype = np.float32)
    imgArray = imgArray/255
    imgArray[:,:,0] = imgArray[:,:,1] = imgArray[:,:,2] = 0
    return Image.fromarray((imgArray * 255).astype(np.uint8))

def negativo(img):
    imgN = np.array(img, dtype = np.float32 )
    imgN = imgN/255
    imgN = 1 - imgN
    return Image.fromarray((imgN * 255).astype(np.uint8))

def rotar_imagen(img, ang):
    img = np.array(img, dtype=np.float32)
    if img.ndim == 3:
        # Si la imagen es a color, la convertimos a escala de grises para simplificar
        img_gray = np.dot(img[...,:3], [0.2989, 0.5870, 0.1140]).astype(np.uint8)
        img = img_gray
    
    angulo_rad = np.radians(ang)
    h, w = img.shape
    cos = np.cos(angulo_rad)
    sin = np.sin(angulo_rad)

    # 2. Calcular las nuevas dimensiones del lienzo
    new_h = int(np.abs(h * cos) + np.abs(w * sin)) + 1
    new_w = int(np.abs(h * sin) + np.abs(w * cos)) + 1
    rotada = np.zeros((new_h, new_w), dtype=img.dtype)
    
    # 3. Encontrar el centro de ambas imágenes
    center_y, center_x = h // 2, w // 2
    new_center_y, new_center_x = new_h // 2, new_w // 2

    # 4. Iterar sobre la nueva imagen y mapear hacia la original
    for y_new in range(new_h):
        for x_new in range(new_w):
            # Calcular las coordenadas relativas al centro
            x_rel = x_new - new_center_x
            y_rel = y_new - new_center_y

            # Aplicar la rotación inversa para encontrar las coordenadas originales
            x_orig = int(x_rel * cos + y_rel * sin + center_x)
            y_orig = int(-x_rel * sin + y_rel * cos + center_y)

            # 5. Asignar el valor del píxel si está dentro de los límites
            if 0 <= y_orig < h and 0 <= x_orig < w:
                rotada[y_new, x_new] = img[y_orig, x_orig]
                
    return Image.fromarray((rotada * 1).astype(np.uint8))


def average(img):
    img_array = np.array(img, dtype=np.float32)

    if img_array.max() > 1.0:
        img_array = img_array / 255.0

    imgGray = (img_array[:,:,0] + img_array[:,:,1] + img_array[:,:,2]) / 3
    return imgGray

def binarizar(img, umbral):
    imgGray = average(img)
    imgBin = (imgGray > umbral)
    
    #Convertir a PIL con modo 'L' (escala de grises)
    imgBin = (imgBin * 255).astype(np.uint8)
    return Image.fromarray(imgBin, mode='L')

def fusionImgEcualizada(img1, img2, factor):
    img1 = np.array(img1, dtype=np.float32) / 255
    img2 = np.array(img2, dtype=np.float32) / 255
    img3 = (img1*factor + img2*(1-factor))
    img3 = np.clip(img3, 0, 1)
    return Image.fromarray((img3 * 255).astype(np.uint8))

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