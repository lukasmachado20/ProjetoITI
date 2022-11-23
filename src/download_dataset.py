import os

def download(file:str = None, folder:str = None) -> None:
    """
    teste
    
    """
    print('Baixando imagem {} ...'.format(file))
    commandS3 = "aws s3 cp s3://2021-204/2021-204-1-1/data/ {0} --recursive --exclude \"*\"  --include {1}  --endpoint-url https://s3.ki.se".format(folder,file)
    os.system(commandS3)