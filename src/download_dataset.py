import os
import time
def download(file:str = None, folder:str = None) -> None:
    """
        * Funcao que baixa imagens DICOM do bucket da AWS para estudo em projeto de pesquisa

        Parametros
        ---------
            file : str 
                Nome do arquivo para baixar
            
            folder : str
                Local da pasta onde o arquivo vai ser salvo
    
    """
    while not os.path.exists(folder+file):
        startTime = time.time()
        print('Baixando imagem {} ...'.format(file))
        commandS3 = "aws s3 cp s3://2021-204/2021-204-1-1/data/ {0} --recursive --exclude \"*\"  --include {1}  --endpoint-url https://s3.ki.se".format(folder,file)
        os.system(commandS3)
        elapsedTime = time.strftime("%H:%M:%S", time.gmtime(time.time() - startTime))
        print("---> Tempo para baixar imagem {} : {}.\n".format(file, elapsedTime))
        
    #verificando
    if os.path.exists(folder+file): 
        print("Imagem {} EXISTE na pasta {}!\n".format(file,folder))
    else:
        print("Imagem {} NÃO EXISTE na pasta {}!\n".format(file,folder))