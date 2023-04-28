import pydicom as dicom
import cv2
import numpy as np
from skimage import exposure
import matplotlib.pyplot as plt
import os

# Funcao que faz o recorte da imagem e equaliza
def cut_Equalize(img):
    # Load the MRI image of the brain
    img = dicom.dcmread(img)
    imgArray = img.pixel_array

    # Apply Otsu's threshold to binarize the image
    thresh = cv2.threshold(imgArray, 0, np.max(imgArray), cv2.THRESH_BINARY)[1].astype('uint8')

    # Encontra todos os contornos da imagem
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Pega o maior contorno
    largest_contour = max(contours, key=cv2.contourArea)

    # Cria a mascara a partir do maior contorno
    mask = np.zeros_like(thresh)

    cv2.drawContours(mask, [largest_contour], -1, (255, 255, 255), -1)

    # Multiply the original image with the mask to crop the irregular shape
    dst = cv2.bitwise_and(imgArray, imgArray, mask=mask)

    rect = cv2.boundingRect(largest_contour)
    # Coordenadas
    x,y,w,h = rect

    # Corta imagem com as coordenadas
    imgCroped = (dst)[y:y+h, x:x+w].copy()

    # Equalizar imagem
    imgCutEqualize = exposure.equalize_adapthist(imgCroped, clip_limit=0.1)

    return imgCutEqualize

def pre_Process_Images(pathImages, pathSave):
    """
        Cut and equalize a list of images inside a folder, then save in format .png
    """
    listImages = os.listdir(pathImages)
    # percorre todas as imagens
    for img in listImages:
        nameImg = str(img)[:-4] + '.png'
        # ja existe na cortadoEqualizado?
        if not os.path.exists(os.path.join(pathSave, nameImg)):
            if os.path.exists(os.path.join(pathImages, img)):
                # Retira os 4 ultimos caracteres do nome da imagem
                nameImg = str(img)[:-4] + '.png'
                print('Imagem para salvar: ' + nameImg)
                imgFinal = cut_Equalize(os.path.join(pathImages, img))
                # Salva imagem
                plt.imsave(fname=pathSave+nameImg, arr=imgFinal, cmap='gray')
            else:
                print('Nao existe na ' + pathImages)
        else:
            print('Imagem na pasta: ' + nameImg)
        
    # Verifica se tem a mesma quantidade
    if len(os.listdir(pathImages)) == len(os.listdir(pathSave)):
        print('Todas imagens cortadas e finalizadas!')
    else:
        print('Faltou imagens!')