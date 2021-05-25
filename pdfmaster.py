#!/usr/bin/python
import sys
import os
from PIL import Image
import cv2
#não gosto dessas importações
from imutils.perspective import four_point_transform
from skimage.filters import threshold_local

# Altere aqui as extensões aceitas
IMAGE_EXTENSIONS = ['.jpg','.jpeg']
LOGO = os.path.join(os.path.dirname(__file__), 'logo-colegio-master.png')
# ----- Definições para o scan
#   Diminua para aumentar a taxa de detecção
EDGE_DETECTION = 35
#   Quanto menor a proporção, menos ruido a imagem, cuidado ao usar
PROPORCAO = 0.2
#   Valor padrão para o "melhoramento" da imagem
OFFSET = 10

# Funcionalidade OS de listagem
def get_arquivos(local=None):
    arquivos = os.listdir(local)
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
# Retorna os caminhos para chegar as imagens
def get_images_path(local=None):
    organizados = organiza(filtra(get_arquivos(local)))
    if local != None:
        organizados = [os.path.join(local, filename) for filename in organizados]
    return organizados
# Vai retornar uma lista de imagens do formato pillow
def open_image_path(path):
    return Image.open(path).convert('RGB')
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

# ---- Aqui fica a parte do CV
# redimenciona
def redimenciona(imagem, escala):
    width, height = int(imagem.shape[1]*escala), int(imagem.shape[0]*escala)
    dimensoes = (width, height)
    redimensionada = cv2.resize(imagem,dimensoes,interpolation=cv2.INTER_AREA)
    return redimensionada
# filtra a imagem em pontos booleanos
def canny_edge_detector(imagem):
    # escala de cinza, blur, find edges
    gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0) # ao dar um certo desfoque com GaussianBlur o ruido da imagem diminui
    #Detecção de quinas de Canny, o valor optimo segundo canny é 3
        # thresholding baixo identifica mais informação na imagem
    canny_edge = cv2.Canny(blur,EDGE_DETECTION ,3*EDGE_DETECTION)
    return canny_edge

# como vamos supor que todas as imagens são retangulares
# o contorno será, o maior contorno com 4 pontos ligados diretamente
def find_contours(canny):
    contorno = ''
    contours = cv2.findContours(canny.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # Imutils functions
    if len(contours) == 2:
        contours = contours[0]
    contours = sorted(contours, key=cv2.contourArea,  reverse=True)
    for x in contours:
        perimetro = cv2.arcLength(x, True)
        # serve para calcular a distância máxima entre dois pontos para a aproximação, 10% parece um bom começo
        epsilon = 0.1*perimetro
        # Aproximação de douglas-pecker
        douglas_pecker = cv2.approxPolyDP(x, epsilon, True)

        if len(douglas_pecker) == 4:
            contorno = douglas_pecker
            break
    return contorno

#escaneia
def scan(path):
    imagem = cv2.imread(path)
    original = imagem.copy()
    ratio = PROPORCAO
    # Redimensionar para utilizar menos recursos
    imagem = redimenciona(imagem, ratio)

    canny_edge = canny_edge_detector(imagem)

    contorno = find_contours(canny_edge)
    cv2.drawContours(imagem,[contorno], -1, (255,0,0), 2)

    em_perspectiva = four_point_transform(original, contorno.reshape(4,2)/ratio)

    #melhoramento da imagem... Não gosto dessa parte do código
    em_perspectiva_bw = cv2.cvtColor(em_perspectiva, cv2.COLOR_BGR2GRAY)
    T = threshold_local(em_perspectiva_bw, 11, offset=OFFSET, method='gaussian')
    em_perspectiva_bw = (em_perspectiva_bw > T).astype('uint8') * 255

    #cv2.imshow('Aspecto final', redimenciona(em_perspectiva_bw, ratio))
    #cv2.imshow('Perspectiva', em_perspectiva)
    #cv2.imshow('Canny Edge Detection', canny_edge)
    #cv2.imshow('Contorno', imagem)

    #cv2.waitKey(10000)
    #cv2.destroyAllWindows()
    return em_perspectiva

def create_temp_path(name):
    destino = os.path.join('.temp',name)
    if not os.path.exists('.temp'):
        os.mkdir('.temp')
    return destino

#salva a imagem escaneada
def save_scan(local, imagem):
    cv2.imwrite(local,imagem)

def scan_dir_images():
    images  = get_images_path()
    for image in images:
        scanned = scan(image)
        destino = create_temp_path(image)
        save_scan(destino, scanned)
# -------------------------------
def agrupar_pdf(nome_do_arquivo, folder=None):

    imagens = get_image_objects(get_images_path(folder))
    imagens_bonitinhas = []
    for imagem in imagens:
        imagens_bonitinhas.append(deixa_as_coisas_bonitinhas(imagem,direcao))
    to_pdf(imagens_bonitinhas,nome_do_arquivo, folder)

def deixa_as_coisas_bonitinhas(imagem,direcao):
    imagem = orientacao(imagem, direcao)
    imagem = insere_logo(imagem)
    return imagem

# Converte todas os objetos de imagem recebidos em um só objeto
def to_pdf(imgs, filename, dir):
    main_image = ''
    try:
        main_image = imgs[0]
    except IndexError:
        print('Não tem imagens nesse diretório')
        exit(0)
    imgs.pop(0)

    main_image.save(filename, save_all=True, append_images=imgs)
    return 'ok'

def clear_temp():
    if os.path.exists('.temp'):
        for x in os.listdir('.temp'):
            os.remove(os.path.join('.temp', x))

if __name__ == '__main__':
    arquivo = ''
    direcao ='vertical'
    opcao = 'pdf_scan'
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
    try:
        opcao = sys.argv[3]
    except IndexError:
        print('Modo padrão: {}'.format(opcao))

    if opcao == '?':
        print('Insira uma função')
    if opcao == 'pdf':
        agrupar_pdf(arquivo)
        clear_temp()
    if opcao == 'scan':
        scan_dir_images()
        agrupar_pdf(arquivo, '.temp')
        clear_temp()
    else:
        print('Opção Desconhecida')
        print('Saindo do programa....')
        exit(0)
