import pygame
import sys
import carros
import estrada

from pygame.locals import *

import random


# funcoes
def loop_game(inicio_estrada=estrada.inicio_estrada, final_estrada=estrada.final_estrada,
              largura_carro=carros.largura_carro, altura_carro=carros.altura_carro):
    pygame.init()

    # configuracoes de largura e altura da tela
    largura = 1280
    altura = 720

    fonte = pygame.font.SysFont('arial', 18, True, False)

    # definindo o tamanho da tela
    tela = pygame.display.set_mode((largura, altura))

    # nome da janela
    pygame.display.set_caption('Car Race')

    # configuracoes do background
    bg = pygame.image.load('assets/bg.png').convert_alpha()
    bg = pygame.transform.scale(bg, (largura, altura))

    carro_principal = pygame.transform.scale(carros.carro_vermelho,
                                             (largura_carro, altura_carro))

    lista_carros_inimigos = [
        pygame.transform.scale(carros.carro_azul, (largura_carro, altura_carro)),
        pygame.transform.scale(carros.carro_verde, (largura_carro, altura_carro)),
        pygame.transform.scale(carros.carro_azul, (largura_carro, altura_carro)),
        pygame.transform.scale(carros.carro_verde, (largura_carro, altura_carro)),
    ]

    # posicao inicial carro do jogador
    pos_jogador_x = (largura / 2) - (carros.altura_carro / 2)
    pos_jogador_y = altura - carros.altura_carro

    # posicao inicial carro inimigo para os 4 carros
    '''
    pos_inimigo_x = [random.randint(inicio_estrada, final_estrada), random.randint(inicio_estrada, final_estrada),
                     random.randint(inicio_estrada, final_estrada), random.randint(inicio_estrada, final_estrada)]
    '''
    pos_inimigo_x = [respawn()[0], respawn()[1], respawn()[2], respawn()[3]]
    pos_inimigo_y = -100




    # relogio
    relogio = pygame.time.Clock()  # Frame

    # variavel de controle do sitema de pontos
    score = 0
    velocidade_estrada = 5
    velocidade_controle = 10

    # flag para rodar o jogo
    rodando = True

    while rodando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

        # configurações para animação da estrada acontecer
        rel_y = altura % bg.get_rect().height  # recebendo o resto da divisao de rel_x pela altura da tela
        tela.blit(bg, (0, rel_y - bg.get_rect().height))  # recriando o bg com base no resto da divisao

        # a cada passo do while, vai fazendo o carossel vertical acontecer
        if rel_y < 720:
            tela.blit(bg, (0, rel_y))
        # movimento acontecendo:
        altura += 1.3 * velocidade_estrada
        pos_inimigo_y += 1 * velocidade_estrada
        score += 0.2

        # controles
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_UP] and pos_jogador_y > 0:
            pos_jogador_y -= velocidade_controle
        if tecla[pygame.K_DOWN] and pos_jogador_y < 595:
            pos_jogador_y += velocidade_controle
        if tecla[pygame.K_LEFT] and pos_jogador_x > inicio_estrada:
            pos_jogador_x -= velocidade_controle
        if tecla[pygame.K_RIGHT] and pos_jogador_x < final_estrada:
            pos_jogador_x += velocidade_controle

        # controle da animação da velocidade da estrada (ilusao de que o carro estará mais rápido)
        if score < 50:
            relogio.tick(20)
        elif 50 <= score < 100:
            relogio.tick(30)
        elif 100 <= score < 150:
            relogio.tick(32)
        elif 150 <= score < 200:
            relogio.tick(34)
        elif 200 <= score < 250:
            relogio.tick(33)
        elif 250 <= score < 300:
            relogio.tick(34)
        elif 300 <= score < 350:
            relogio.tick(35)
        elif 350 <= score < 400:
            relogio.tick(36)
        elif 350 <= score < 400:
            relogio.tick(36)

        # condicao de respawn
        if pos_inimigo_y > 719:
            posicoes_respawn = respawn()
            pos_inimigo_x = [posicoes_respawn[0], posicoes_respawn[1], posicoes_respawn[2], posicoes_respawn[3]]
            pos_inimigo_y = -100

        # retangulos colisao
        blit_carro_principal = tela.blit(carro_principal, (pos_jogador_x, pos_jogador_y))
        blits_carros_inimigos = [tela.blit(lista_carros_inimigos[0], (pos_inimigo_x[0], pos_inimigo_y)),
                                 tela.blit(lista_carros_inimigos[1], (pos_inimigo_x[1], pos_inimigo_y)),
                                 tela.blit(lista_carros_inimigos[2], (pos_inimigo_x[2], pos_inimigo_y)),
                                 tela.blit(lista_carros_inimigos[3], (pos_inimigo_x[3], pos_inimigo_y))]

        # verificando colisoes
        for i in range(4):
            if blit_carro_principal.colliderect(blits_carros_inimigos[i]):

                font_2 = pygame.font.SysFont("arial", 20, True, False)
                messagem = "GAME OVER! VOCÊ BATEU! REINICIAR O JOGO: R"
                messagem_2 = f'Score: {int(score)}'

                text_formatado = font_2.render(messagem, True, (255, 255, 255), (0, 0, 0))
                text_formatado_2 = font_2.render(messagem_2, True, (255, 255, 255), (0, 0, 0))

                ret_texto = text_formatado.get_rect()
                ret_texto_2 = text_formatado_2.get_rect()

                jogando = False

                while not jogando:

                    tela.blit(bg, (0, 0))

                    for event in pygame.event.get():

                        if event.type == QUIT:
                            pygame.quit()
                            exit()

                        ret_texto.center = (largura // 2, 380)
                        ret_texto_2.center = (largura // 2, 460)
                        tela.blit(text_formatado_2, ret_texto_2)
                        tela.blit(text_formatado, ret_texto)

                        pygame.display.update()

                        tecla = pygame.key.get_pressed()

                        if tecla[pygame.K_r]:
                            loop_game()
                            jogando = True

        # desenhando na tela
        tela.blit(carro_principal, (pos_jogador_x, pos_jogador_y))

        tela.blit(lista_carros_inimigos[0], (pos_inimigo_x[0], pos_inimigo_y))
        tela.blit(lista_carros_inimigos[1], (pos_inimigo_x[1], pos_inimigo_y))
        tela.blit(lista_carros_inimigos[2], (pos_inimigo_x[2], pos_inimigo_y))
        tela.blit(lista_carros_inimigos[3], (pos_inimigo_x[3], pos_inimigo_y))

        pontuacao = f'Score: {int(score)}'
        texto_formatado = fonte.render(pontuacao, True, (255, 255, 255))
        tela.blit(texto_formatado, (65, 20))
        pygame.display.update()

    pygame.mixer.init()


def respawn(inicio_estrada=estrada.inicio_estrada, final_estrada=estrada.final_estrada, largura_carro= carros.largura_carro):

    lista_posicoes = [inicio_estrada,
                      inicio_estrada+(largura_carro*1),
                      inicio_estrada+(largura_carro*2),
                      inicio_estrada+(largura_carro*3),
                      inicio_estrada+(largura_carro*4),
                      inicio_estrada+(largura_carro*5),
                      inicio_estrada+(largura_carro*1),
                      inicio_estrada+(largura_carro*6),
                      inicio_estrada+(largura_carro*7),
                      inicio_estrada+(largura_carro*8),
                      inicio_estrada+(largura_carro*9),
                      inicio_estrada+(largura_carro*10)]

    #embaralha a lista de posicoes
    random.shuffle(lista_posicoes)

    #obtendo 4 elementos aleatorios
    x_carro_inimigo = random.sample(lista_posicoes, 4)

    return x_carro_inimigo


loop_game()
