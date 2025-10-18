"""
Módulo de funciones auxiliares para procesamiento de imágenes.

Este módulo contiene funciones para aplicar diversos ajustes y transformaciones
a imágenes digitales, incluyendo operaciones de brillo, contraste, filtros de
color, binarización, fusión, rotación e histogramas.

Autor: Maria Angélica Alvarez Giraldo
Fecha: Octubre 2025
"""
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

#Funciones auxiliares para el visor de imagenes

def ajusteBrillo(img, brillo):
    """
    Ajusta el brillo de una imagen.
    
    Args:
        img (PIL.Image.Image): Imagen a procesar.
        brillo (float): Factor de brillo a aplicar (-1.0 a 1.0).
            Valores positivos aumentan el brillo, negativos lo disminuyen.
    
    Returns:
        PIL.Image.Image: Imagen con el brillo ajustado.
    """
    imgArray = np.array(img)  # convierte la imagen a un array de numpy
    imgArray = imgArray/255
    imgBrillo = imgArray + brillo
    imgBrillo = np.clip(imgBrillo, 0, 1) #evita saturacion
    return Image.fromarray((imgBrillo * 255).astype(np.uint8))

def ajusteContraste(img, contraste, tipo):
    """
    Ajusta el contraste de una imagen priorizando zonas claras u oscuras.
    
    Args:
        img (PIL.Image.Image): Imagen a procesar.
        contraste (float): Factor de contraste a aplicar.
        tipo (int): Tipo de ajuste de contraste:
            1 - Prioriza zonas oscuras (función logarítmica).
            2 - Prioriza zonas claras (función exponencial).
    
    Returns:
        PIL.Image.Image: Imagen con el contraste ajustado.
    """
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
    """
    Extrae únicamente el canal rojo de la imagen.
    
    Args:
        img (PIL.Image.Image): Imagen RGB a procesar.
    
    Returns:
        PIL.Image.Image: Imagen con solo el canal rojo activo.
    """
    imgArray = np.array(img, dtype=np.float32)
    imgArray = imgArray / 255
    #imgArray = np.copy(img)
    imgArray[:,:,1] = imgArray[:,:,2] = 0
    return Image.fromarray((imgArray * 255).astype(np.uint8))

def capaVerde(img):
    """
    Extrae únicamente el canal verde de la imagen.
    
    Args:
        img (PIL.Image.Image): Imagen RGB a procesar.
    
    Returns:
        PIL.Image.Image: Imagen con solo el canal verde activo.
    """
    imgArray = np.array(img, dtype = np.float32)
    imgArray = imgArray/255
    imgArray[:,:,0] = imgArray[:,:,2] = 0
    return Image.fromarray((imgArray * 255).astype(np.uint8))

def capaAzul(img):
    """
    Extrae únicamente el canal azul de la imagen.
    
    Args:
        img (PIL.Image.Image): Imagen RGB a procesar.
    
    Returns:
        PIL.Image.Image: Imagen con solo el canal azul activo.
    """
    imgArray = np.array(img, dtype = np.float32)
    imgArray = imgArray/255
    imgArray[:,:,0] = imgArray[:,:,1] = 0
    return Image.fromarray((imgArray * 255).astype(np.uint8))

def canalCian(img):
    """
    Genera el canal cian (combinación de verde y azul).
    
    Args:
        img (PIL.Image.Image): Imagen RGB a procesar.
    
    Returns:
        PIL.Image.Image: Imagen con el canal cian (rojo = 0, verde y azul = 255).
    """
    imgArray = np.array(img, dtype = np.float32)
    imgArray = imgArray/255
    imgArray[:,:,1] = imgArray[:,:,2] = 1
    return Image.fromarray((imgArray * 255).astype(np.uint8))

def canalMagenta(img):
    """
    Genera el canal magenta (combinación de rojo y azul).
    
    Args:
        img (PIL.Image.Image): Imagen RGB a procesar.
    
    Returns:
        PIL.Image.Image: Imagen con el canal magenta (rojo y azul = 255, verde = 0).
    """
    imgArray = np.array(img, dtype = np.float32)
    imgArray = imgArray/255
    imgArray[:,:,0] = imgArray[:,:,2] = 1
    return Image.fromarray((imgArray * 255).astype(np.uint8))

def canalAmarillo(img):
    """
    Genera el canal amarillo (combinación de rojo y verde).
    
    Args:
        img (PIL.Image.Image): Imagen RGB a procesar.
    
    Returns:
        PIL.Image.Image: Imagen con el canal amarillo (rojo y verde = 255, azul = 0).
    """
    imgArray = np.array(img, dtype = np.float32)
    imgArray = imgArray/255
    imgArray[:,:,0] = imgArray[:,:,1] = 1
    return Image.fromarray((imgArray * 255).astype(np.uint8))

def negroConceptual(img):
    """
    Genera una imagen completamente negra (todos los canales en 0).
    
    Representa conceptualmente el negro en el modelo CMY.
    
    Args:
        img (PIL.Image.Image): Imagen RGB base (se usa solo para obtener dimensiones).
    
    Returns:
        PIL.Image.Image: Imagen negra del mismo tamaño que la entrada.
    """
    imgArray = np.array(img, dtype = np.float32)
    imgArray = imgArray/255
    imgArray[:,:,0] = imgArray[:,:,1] = imgArray[:,:,2] = 0
    return Image.fromarray((imgArray * 255).astype(np.uint8))

def negativo(img):
    """
    Genera el negativo de una imagen.
    
    Invierte los valores de todos los píxeles (255 - valor original).
    
    Args:
        img (PIL.Image.Image): Imagen a invertir.
    
    Returns:
        PIL.Image.Image: Imagen negativa.
    """
    imgN = np.array(img, dtype = np.float32 )
    imgN = imgN/255
    imgN = 1 - imgN
    return Image.fromarray((imgN * 255).astype(np.uint8))

def rotar_imagen(img, ang):
    """
    Rota una imagen en escala de grises usando interpolación manual.
    
    Aplica una transformación de rotación píxel por píxel usando
    matrices de rotación. Convierte imágenes de color a escala de grises.
    
    Args:
        img (PIL.Image.Image o np.ndarray): Imagen a rotar.
        ang (float): Ángulo de rotación en grados.
    
    Returns:
        PIL.Image.Image: Imagen rotada en escala de grises.
    
    Note:
        Esta función convierte la imagen a escala de grises. Para rotar
        imágenes a color, usar PIL.Image.rotate() directamente.
    """
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
    """
    Convierte una imagen RGB a escala de grises usando promedio simple.
    
    Calcula el promedio de los tres canales RGB para cada píxel.
    
    Args:
        img (PIL.Image.Image): Imagen RGB a convertir.
    
    Returns:
        np.ndarray: Imagen en escala de grises como array numpy (valores 0-1).
    """
    img_array = np.array(img, dtype=np.float32)

    if img_array.max() > 1.0:
        img_array = img_array / 255.0

    imgGray = (img_array[:,:,0] + img_array[:,:,1] + img_array[:,:,2]) / 3
    return imgGray

def binarizar(img, umbral):
    """
    Binariza una imagen usando un umbral específico.
    
    Convierte la imagen a escala de grises y luego a blanco y negro
    según el valor umbral.
    
    Args:
        img (PIL.Image.Image): Imagen a binarizar.
        umbral (float): Valor umbral (0-1). Píxeles por encima del umbral
            se vuelven blancos, los demás negros.
    
    Returns:
        PIL.Image.Image: Imagen binarizada en modo 'L' (escala de grises).
    """
    imgGray = average(img)
    imgBin = (imgGray > umbral)
    
    #Convertir a PIL con modo 'L' (escala de grises)
    imgBin = (imgBin * 255).astype(np.uint8)
    return Image.fromarray(imgBin, mode='L')

def fusionImgEcualizada(img1, img2, factor):
    """
    Fusiona dos imágenes usando transparencia.
    
    Combina dos imágenes del mismo tamaño aplicando un factor de transparencia
    para crear una mezcla ponderada.
    
    Args:
        img1 (PIL.Image.Image): Primera imagen (base).
        img2 (PIL.Image.Image): Segunda imagen (overlay).
        factor (float): Factor de transparencia (0-1). 
            1.0 = solo img1, 0.0 = solo img2.
    
    Returns:
        PIL.Image.Image: Imagen fusionada.
    
    Note:
        Ambas imágenes deben tener las mismas dimensiones.
    """
    img1 = np.array(img1, dtype=np.float32) / 255
    img2 = np.array(img2, dtype=np.float32) / 255
    img3 = (img1*factor + img2*(1-factor))
    img3 = np.clip(img3, 0, 1)
    return Image.fromarray((img3 * 255).astype(np.uint8))

def histogramas(img):
    """
    Genera y muestra histogramas de los canales RGB de una imagen.
    
    Crea una figura con tres subgráficas mostrando la distribución
    de intensidades para cada canal de color (rojo, azul, verde).
    
    Args:
        img (PIL.Image.Image o np.ndarray): Imagen RGB a analizar.
    
    Note:
        Muestra los histogramas en una ventana matplotlib interactiva.
    """
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

def overlay(img_proc: Image.Image, label_size: tuple[int, int], rect: tuple[int,int,int,int]):
    """
    Crea una imagen overlay con un rectángulo de selección dibujado.
    
    Centra la imagen procesada en un canvas del tamaño del label y dibuja
    un rectángulo sobre ella para visualizar el área de selección.
    
    Args:
        img_proc (PIL.Image.Image): Imagen procesada a mostrar.
        label_size (tuple[int, int]): Tamaño del canvas (ancho, alto).
        rect (tuple[int, int, int, int]): Coordenadas del rectángulo (x1, y1, x2, y2).
    
    Returns:
        tuple: (imagen_overlay, (offset_x, offset_y)) donde:
            - imagen_overlay (PIL.Image.Image): Imagen con el rectángulo dibujado.
            - offsets (tuple): Desplazamientos de la imagen dentro del canvas.
    """
    if img_proc is None:
        return None, (0,0)
    ancho, alto = label_size
    img_w, img_h = img_proc.size

    offset_x = max(0, (ancho - img_w) // 2)
    offset_y = max(0, (alto - img_h) // 2)

    overlay_img = Image.new('RGBA', (ancho, alto), (255,255,255,0))
    img = img_proc.convert('RGBA')
    overlay_img.paste(img, (offset_x, offset_y))

    x1,y1,x2,y2 = rect
    draw = ImageDraw.Draw(overlay_img)
    draw.rectangle([x1,y1,x2,y2], outline='black', width = 3)

    return overlay_img, (offset_x, offset_y)

def cortar_redimensionar(img_proc: Image.Image, offsets: tuple[int, int], rect: tuple[int,int,int,int], out_size: tuple[int,int]):
    """
    Corta una región de la imagen y la redimensiona al tamaño deseado.
    
    Extrae la región seleccionada de la imagen teniendo en cuenta los offsets
    del canvas, y la redimensiona para llenar el área de visualización.
    
    Args:
        img_proc (PIL.Image.Image): Imagen procesada de origen.
        offsets (tuple[int, int]): Desplazamiento de la imagen (offset_x, offset_y).
        rect (tuple[int, int, int, int]): Coordenadas del rectángulo seleccionado
            en coordenadas del canvas (x1, y1, x2, y2).
        out_size (tuple[int, int]): Tamaño de salida deseado (ancho, alto).
    
    Returns:
        PIL.Image.Image: Región recortada y redimensionada, o None si la región es inválida.
    """
    if img_proc is None:
        return None
    offset_x, offset_y = offsets
    x1,y1,x2,y2 = rect

    ix1 = x1 - offset_x
    iy1 = y1 - offset_y
    ix2 = x2 - offset_x
    iy2 = y2 - offset_y

    img_w, img_h = img_proc.size

    left = max(0, min(img_w, int(min(ix1, ix2))))
    top  = max(0, min(img_h, int(min(iy1, iy2))))
    right= max(0, min(img_w, int(max(ix1, ix2))))
    bottom=max(0, min(img_h, int(max(iy1, iy2))))

    if right - left < 1 or bottom - top < 1:
        return None
    
    region = img_proc.crop((left, top, right, bottom))
    region_zoom = region.resize(out_size, Image.LANCZOS)
    return region_zoom