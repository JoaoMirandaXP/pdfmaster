#!/usr/bin/python
import os
from PIL import Image
import sys
import time

#Listagem de arquivos da pasta
#filtrar apenas os arquivos que são imagens já na ordem numérica, selecionando apenas arquivos png ou jpg
listagem = os.listdir()
DIRETORIO = os.getcwd() 
ARQUIVOS = []
FILE_NAME = sys.argv[1]
print('Um momento, gerando o arquivo {}'.format(FILE_NAME))
for x in sorted(listagem):
    if x.endswith('.jpg') or x.endswith('.png'):
        location = os.path.join(DIRETORIO,x)
        ARQUIVOS.append(location)
print('Arquivos identificados: {}'.format(ARQUIVOS))
#Rotaciona certas imagens na horizontal

#

#converte as imagens passadas em parâmetro para pdf
def converter_para_pdf(path_to_images):
    #Trás a imagem inicial para a função
    inicial = Image.open(path_to_images[0])
    imagem_inicial = inicial.convert('RGB')
    #Remove a imagem inicial da array
    path_to_images.pop(0)

    image_list = []
    
    for image in path_to_images:
        file = Image.open(image)
        converted = file.convert('RGB')
        image_list.append(converted)

    imagem_inicial.save(os.path.join(DIRETORIO,FILE_NAME),save_all=True,append_images=image_list)

converter_para_pdf(ARQUIVOS)
print('--------------------------------------------------------------------------------------------')
print('Finalizado com sucesso!')



