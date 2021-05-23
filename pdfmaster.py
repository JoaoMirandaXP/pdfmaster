#!/usr/bin/python
import sys
import os
import extensions
from PIL import Image

# Funcionalidade OS de listagem
def get_arquivos():
    arquivos = os.listdir()
    return arquivos
# Para configurar os formatos de arquivos que são aceitos vá em extensions.py
def filtra(arquivos):
    filtrados = []
    for arquivo in arquivos:
        if os.path.splitext(arquivo)[1].lower() in extensions.IMAGE_EXTENSIONS:
            filtrados.append(arquivo)
    return filtrados
#coloca os arquivos filtrados em uma ordem "coerente"
def organiza(arquivos_filtrados):
    return  sorted(arquivos_filtrados,key=lambda x: int(os.path.splitext(x)[0]))

# Tratamento de imagem para melhorar o uso.
# Abre a imagem como objeto pillow
def get_images_path():
    return organiza(filtra(get_arquivos()))
# Vai retornar uma lista de imagens do formato pillow
def open_image_path(path):
    return Image.open(path)
# retorna os objetos de imagem
def get_image_objects(img_list):
    objects = []
    for img in img_list:
        obj = open_image_path(img)
        objects.append(obj)
    return objects
#
# ---- Aqui fica a lógica do programa em melhorar a imagem ao se tornar um pdf
#
# Converte todas os objetos de imagem recebidos em um só objeto
def to_pdf(imgs, filename):
    main_image = imgs[0]
    imgs.pop(0)
    main_image.save(filename, save_all=True, append_images=imgs)
    return 'ok'

if __name__ == '__main__':
    arquivo = ''
    # recebendo nome esperado para o arquivo
    try:
        arquivo = sys.argv[1]
        if not arquivo.endswith('pdf'):
            arquivo += '.pdf'
        print('Gerando {}...'.format(arquivo))
    except IndexError:
        print('O nome de arquivo não foi informado ou não é compatível')
        exit()
    to_pdf(get_image_objects(get_images_path()), arquivo)
