import pygame

# configuracoes dos carros
escala = 0.075  # será usando para que a imagem apareça com tamanho escalado 10%

# carro vermelho (carro do jogador)
carro_vermelho = pygame.image.load('assets/carro-vermelho.png')

# carro azul
carro_azul = pygame.image.load('assets/carro-azul.png') # carregando a imagem

# carro verde
carro_verde = pygame.image.load('assets/carro-verde.png')

#largura e altura
largura_carro, altura_carro = carro_vermelho.get_size()  # atribuindo largura e altura da imagem à uma variável
largura_carro = int(largura_carro * escala)
altura_carro = int(altura_carro * escala)