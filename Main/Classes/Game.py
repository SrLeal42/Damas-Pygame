import pygame as PG
from Config import LARGURA, ALTURA, NUM_PECAS
from Classes.Pecas import Peca
from Classes.Tabuleiro import Tabuleiro

class Game:

    tabuleiro = None
    PecasBrancas = None
    PecasPretas = None

    def __init__(self):

        # PEÇAS BRANCAS
        PB = self.CreatePecas(0)
        PP = self.CreatePecas(1)

        self.tabuleiro = Tabuleiro()

        self.tabuleiro.AdicionaPecasAoTabuleiro(PB, 1)
        self.tabuleiro.AdicionaPecasAoTabuleiro(PP, 0)



    def CreatePecas(self, cor:int):

        P = []
        for _ in range(NUM_PECAS):
            p = Peca(cor,0,0)
            P.append(p)

        return P

