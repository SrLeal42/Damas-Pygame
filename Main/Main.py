import pygame as PG
from Config import LARGURA, ALTURA,GRAY
from Classes.Pecas import Peca
from Classes.Tabuleiro import Tabuleiro
from Classes.Game import Game


PG.init()

running = True

window = PG.display.set_mode((LARGURA,ALTURA))

PG.display.set_caption("Damas")

current_game = None

def CreateGame():
    global current_game 
    current_game = Game()


while(running):
    for evento in PG.event.get():
            if evento.type == PG.QUIT:
                running = False
                # for i in range(current_game.tabuleiro.tamanho):
                #     for j in range(current_game.tabuleiro.tamanho):
                #         print(current_game.tabuleiro.tabuleiro[i][j])

    window.fill(GRAY)

    if (current_game == None):
         CreateGame()

    current_game.tabuleiro.DesenhaTabuleiro(window)

    PG.display.flip()



    