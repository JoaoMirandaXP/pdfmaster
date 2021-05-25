#!/usr/bin/python
import sys
import os
from PIL import Image
# Altere aqui as extensões aceitas
IMAGE_EXTENSIONS = ['.jpg','.png']
LOGO = os.path.join(os.path.dirname(__file__), 'logo-colegio-master.png')


# Funcionalidade OS de listagem
def get_arquivos():
    arquivos = os.listdir()
    return arquivos
# Para configurar os formatos de arquivos que são aceitos vá em extensions.py
def filtra(arquivos):
    filtrados = []
    for arquivo in arquivos:
        if os.path.splitext(arquivo)[1].lower() in IMAGE_EXTENSIONS:
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

# Função que vai inserir a logo no canto superior esquerdo da imagem
def insere_logo(imagem):
    logo = Image.open(LOGO)
    img_wdt, img_hgt = imagem.size
    logo_wdt, logo_hgt = logo.size
    imagem.paste(logo,(img_wdt-logo_wdt, 0), mask=logo)
    return imagem
# Função para orientar as imagens corretamente
def orientacao(imagem, direcao='vertical'):
    w, h = imagem.size
    if(direcao == 'vertical'):
        if (w>h):
            return imagem.rotate(-90, expand=True)
        else:
            return imagem
    if(direcao == 'horizontal'):
        if (h>w):
            return imagem.rotate(90, expand=True)
        else:
            return imagem

# Funçao geral de formatação, nela serão inseridas as demais funcionalidades
def deixa_as_coisas_bonitinhas(imagem,direcao):
    imagem = orientacao(imagem, direcao)
    imagem = insere_logo(imagem)
    return imagem

# Converte todas os objetos de imagem recebidos em um só objeto
def to_pdf(imgs, filename):
    main_image = ''
    try:
        main_image = imgs[0]
    except IndexError:
        print('Não tem imagens nesse diretório')
        exit(0)
    imgs.pop(0)
    main_image.save(filename, save_all=True, append_images=imgs)
    return 'ok'

if __name__ == '__main__':
    arquivo = ''
    direcao ='vertical'
    # recebendo nome esperado para o arquivo
    try:
        arquivo = sys.argv[1]
        if not arquivo.endswith('pdf'):
            arquivo += '.pdf'
        print('Gerando {}...'.format(arquivo))
    except IndexError:
        print('O nome de arquivo não foi informado ou não é compatível')
        exit()
    try:
        direcao = sys.argv[2]
    except IndexError:
        print('Orientação padrão: {}'.format(direcao))

    imagens = get_image_objects(get_images_path())
    imagens_bonitinhas = []
    for imagem in imagens:
        imagens_bonitinhas.append(deixa_as_coisas_bonitinhas(imagem,direcao))
    to_pdf(imagens_bonitinhas,arquivo)
