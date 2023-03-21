import pydicom as dicom
import cv2
import imutils
import numpy as np
from matplotlib import pyplot as plt
from skimage import exposure
from skimage import img_as_float

def croped_Img_With_Threshold(imgArray:np.array, threshold:int=0) -> np.array:
    '''
        Funcao
        ------
            Faz o retorte da imagem a partir do contorno dela

        Parametros
        ----------
            imgArray : numpy array
                array da imagem para recorte
            
            threshold : int
                threshold para definicao do binarizacao da imagem
        
        Retorno
        -------
            imgCroped -> numpy array
            * retorna a imagem cortada
    '''
    # todos os valores maiores que o threshold irao receber 1, senao recebe 0
    ret, temp1 = cv2.threshold(imgArray, threshold, np.max(imgArray), cv2.THRESH_BINARY)
    arrayThresh = temp1.astype('uint8')

    # Iremos pegar os contornos da imagem
    # Utilizando cv2.CHAIN_APPROX_SIMPLE pegamos apenas as bordas do contorno da imagem, assim poupando processamento e memoria
    countours = cv2.findContours(arrayThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    countours = imutils.grab_contours(countours)
    countours = sorted(countours, key= cv2.contourArea, reverse = True) #pegando as coordenadas que resultam na maior área
    rect = cv2.boundingRect(countours[0])

    # Coordenadas
    x,y,w,h = rect

    # Corta imagem com as coordenadas
    imgCroped = (imgArray)[y:y+h, x:x+w].copy()

    return imgCroped

def plot_Img_And_Hist(img, axes, nBins=4095):
    image = img_as_float(img)

    axeImg, axeHist = axes
    axeCdf = axeHist.twinx()

    # Display na imagem
    axeImg.imshow(image, cmap=plt.cm.gray)
    axeImg.set_axis_off()

    # Display no Histograma da imagem
    axeHist.hist(image.ravel(), bins=nBins, histtype='step', color='black')
    axeHist.semilogy()
    axeHist.set_xlabel('Intensidade do Pixel')
    axeHist.set_xlim(-0.1, 1)

    # Cumulative Distribution da imagem
    imgCdf, bins = exposure.cumulative_distribution(image, nBins)
    axeCdf.plot(bins, imgCdf, 'r')
    axeCdf.set_yticks([])
    
    return axeImg, axeHist, axeCdf

def cria_Axis(fig:plt.figure) -> np.array:
    rows, columns = 2, 3
    axes = np.zeros((rows, columns), dtype=object)
    axes[0, 0] = fig.add_subplot(rows, columns, 1)
    for i in range(1, columns):
        axes[0, i] = fig.add_subplot(rows, columns, 1+i, sharex=axes[0,0], sharey=axes[0,0])
    for i in range(0, columns):
        axes[1, i] = fig.add_subplot(rows, columns, 4+i)
    return fig, axes