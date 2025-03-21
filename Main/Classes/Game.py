import pygame as PG
from Config import LARGURA, ALTURA, NUM_PECAS_DAMAS, NUM_PECAS_XADREZ

from Classes.Pecas import Peca
from Classes.Tabuleiro import Tabuleiro

class Game:

    jogo = ""

    tabuleiro = None
    PecasBrancas = None
    PecasPretas = None

    rei_PB = None
    rei_PP = None

    num_rodadas = 0
    cor_rodada = 0

    sequencia_captura = False # Significa que caso um player capture uma peça e existe a possibilidade de capturar outras ele deve continuar na sequencia de capturas

    def __init__(self,jogo:str):

        self.jogo = jogo

        # PEÇAS BRANCAS
        PB = self.CreatePecas(0)
        PP = self.CreatePecas(1)

        self.PecasBrancas = PB
        self.PecasPretas = PP

        self.tabuleiro = Tabuleiro()

        self.tabuleiro.AdicionaPecasAoTabuleiro(PB,jogo,1)
        self.tabuleiro.AdicionaPecasAoTabuleiro(PP,jogo,0)



    def CreatePecas(self, cor:int):

        if (self.jogo == ""):
            return
        
        P = []

        if (self.jogo == "damas"):
            
            for _ in range(NUM_PECAS_DAMAS):

                p = Peca(cor,0,0)
                P.append(p)
        
        elif (self.jogo == "xadrez"):
            
            outros_tipos = [3] * 2 + [4] * 2 + [5] * 2 + [6, 7]

            for i, tipo in enumerate(outros_tipos):
                p = Peca(cor, 0, 0, tipo=tipo)

                if tipo == 7:  # O rei
                    if cor == 0:
                        self.rei_PB = p
                    else:
                        self.rei_PP = p

                P.append(p)

            for i in range(NUM_PECAS_XADREZ//2):
                p = Peca(cor, 0, 0, tipo=2)

                if (cor == 0):
                    P.insert(0,p)
                else:
                    P.append(p)        
        
        return P



    
    def EndTurn(self):
        self.num_rodadas += 1
        if (not self.sequencia_captura):
            self.cor_rodada = 0 if self.cor_rodada == 1 else 1
        # self.sequencia_captura = False

