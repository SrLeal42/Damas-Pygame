import pygame as PG
from Classes.Pecas import Peca
from Config import LARGURA,ALTURA,WHITE,BLACK,NUM_PECAS


class Tabuleiro:

    tamanho = 8
    tabuleiro = []

    def __init__(self):

        for i in range(self.tamanho):
            
            coluna = []
            
            for j in range(self.tamanho):
                coluna.append(None)
            
            self.tabuleiro.append(coluna)


    def AdicionaPecasAoTabuleiro(self,Pecas, cor:int):
        indexPecas = 0
        indexlinhas = 0
        pularLinhas = 5 if cor == 1 else 0 # Dependendo da cor da peca pular um numero de linhas

        for i in range(self.tamanho):
            if i < pularLinhas:
                continue
            else:
                indexlinhas += 1

            if indexlinhas > 3:
                break

            for j in range(self.tamanho):
                if j%2 == i%2:
                    continue
                self.tabuleiro[i][j] = Pecas[indexPecas]
                indexPecas += 1
                

            


    def DesenhaTabuleiro(self, window):
        x_OffSet = 250 # A distancia do primeiro quadrado até o centro da tela no eixo x
        y_OffSet = 250
        for i in range(self.tamanho):
            for j in range(self.tamanho):

                color = WHITE if self.tabuleiro[i][j] == None else BLACK

                x = LARGURA/2 + (-x_OffSet + (x_OffSet/4 * j))
                y = ALTURA/2 + (-y_OffSet + (y_OffSet/4 * i))
                PG.draw.rect(window,color,(x,y,5,5))




