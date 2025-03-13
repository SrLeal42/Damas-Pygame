import pygame as PG
from Config import LARGURA,WHITE


class Tabuleiro:

    tamanho = 8
    tabuleiro = []

    def __init__(self):

        for i in range(self.tamanho):
            
            coluna = []
            
            for j in range(self.tamanho):
                coluna.append(None)
            
            self.tabuleiro.append(coluna)


    def DesenhaTabuleiro(self, window):
        PG.draw.rect(window,WHITE,(0,0,5,5))


