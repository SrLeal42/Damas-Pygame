import pygame as PG
from Config import LARGURA, ALTURA
from Classes.Pecas import Peca
from Classes.Tabuleiro import Tabuleiro


PG.init()

running = True

window = PG.display.set_mode((LARGURA,ALTURA))

PG.display.set_caption("Damas")

tabuleiro = Tabuleiro()

while(running):
    for evento in PG.event.get():
            if evento.type == PG.QUIT:
                running = False

    tabuleiro.DesenhaTabuleiro(window)

    PG.display.flip()



    