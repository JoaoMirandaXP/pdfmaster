# pdfmaster

  Template de formatação para provas de segunda fase do colégio Master
  
  **Não** está pronto para utilização em provas
---
## Para usar esse programa você vai precisar
---

- Ter o python3 instalado no seu computador (lembre de adicionar o python as VARIAVEIS DE AMBIENTE ou PATH)
https://www.python.org/downloads/

- Instalar os requirements do programa
(basta ir na pasta em que foi baixado e digitar)
```
pip install -r requirements.txt
```
ou no windows
```
python -m pip install -r requirements.txt
```
---
## Utilização
---
```localização/das/imagens $ python pdfmaster [nome_do_seu_arquivo] [orientacao] [opcao]```

Atenção: a orientação deve ser escrita: ```horizontal``` ou ```vertical``` (a orientação padrão é vertical)
---
## Todo

- [X] Abstrair as funções e fazer com que elas tenham mais sentido juntas de maneira concisa

- [X] Inserir a logomarca no canto superior esquerdo

- [X] Deixar que o usuário escolha a orientação das imagens no pdf

- [X] Identificar com precisão as bordas das Imagens

- [x] Usar as bordas para encontrar o contorno

- [x] Transformação de perspectiva

- [x] Otimizar a qualidade de leitura

- [X] Fazer os requirements.txt

- [X] Salvar as imagens novas

- [X] Gerar pdf

- [ ] Aceitar **kwargs como por exemplo ```python pdfmaster [arquivo] [orientacao] kwargs``` com opções e ativar funções específicas
