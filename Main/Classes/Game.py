import pygame as PG
from Config import LARGURA, ALTURA, NUM_PECAS
from Classes.Pecas import Peca
from Classes.Tabuleiro import Tabuleiro

class Game:

    tabuleiro = None
    PecasBrancas = None
    PecasPretas = None

    num_rodadas = 0
    cor_rodada = 0

    def __init__(self):

        # PEÇAS BRANCAS
        PB = self.CreatePecas(0)
        PP = self.CreatePecas(1)

        self.PecasBrancas = PB
        self.PecasPretas = PP

        self.tabuleiro = Tabuleiro()

        self.tabuleiro.AdicionaPecasAoTabuleiro(PB, 1)
        self.tabuleiro.AdicionaPecasAoTabuleiro(PP, 0)



    def CreatePecas(self, cor:int):

        P = []
        for _ in range(NUM_PECAS):

            p = Peca(cor,0,0)
            P.append(p)

        return P
    
    def EndTurn(self):
        self.num_rodadas += 1
        self.cor_rodada = 0 if self.cor_rodada == 1 else 1

