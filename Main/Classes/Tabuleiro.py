import pygame as PG
import math
from Classes.Pecas import Peca
from Config import LARGURA,ALTURA,WHITE,BLACK,GRAY,NUM_PECAS


class Tabuleiro:

    tamanho = 8
    tabuleiro = []
    x_OffSet = 250 # A distancia do primeiro quadrado até o centro da tela no eixo x
    y_OffSet = 250

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

                x = LARGURA/2 + (-self.x_OffSet + (self.x_OffSet/4 * j)) # calculando a posição na tela 
                y = ALTURA/2 + (-self.y_OffSet + (self.y_OffSet/4 * i))

                Pecas[indexPecas].SetCoord(x,y,True)
                Pecas[indexPecas].SetTabCoord(i,j,True)

                self.tabuleiro[i][j] = Pecas[indexPecas]
                indexPecas += 1
                

            


    def DesenhaTabuleiro(self, window):
        
        # PG.draw.line(window, 
        #              WHITE, 
        #              (LARGURA/2 + (-x_OffSet + (x_OffSet/4 * 0))- Peca.tamanho, ALTURA/2 + (-y_OffSet + (y_OffSet/4 * 0))- Peca.tamanho),
        #              (LARGURA/2 + (-x_OffSet + (x_OffSet/4 * self.tamanho)), ALTURA/2 + (-y_OffSet + (y_OffSet/4 * 0))- Peca.tamanho)
        #              )
        
        # PG.draw.line(window, 
        #              WHITE, 
        #              (LARGURA/2 + (-x_OffSet + (x_OffSet/4 * 0))- Peca.tamanho, ALTURA/2 + (-y_OffSet + (y_OffSet/4 * 0))- Peca.tamanho),
        #              (LARGURA/2 + (-x_OffSet + (x_OffSet/4 * 0))- Peca.tamanho, ALTURA/2 + (-y_OffSet + (y_OffSet/4 * self.tamanho))- Peca.tamanho)
        #              )

        for i in range(self.tamanho):
            for j in range(self.tamanho):

                peca = self.tabuleiro[i][j]

                if peca == None:
                    continue

                color = WHITE if peca.cor == 0 else BLACK

                # x = LARGURA/2 + (-self.x_OffSet + (self.x_OffSet/4 * j))
                # y = ALTURA/2 + (-self.y_OffSet + (self.y_OffSet/4 * i))


                PG.draw.circle(window,color,(peca.x,peca.y),peca.tamanho)

    def ClosePlace(self,x1,y1):

        closest = []
        closest_dist = math.inf

        for i in range(self.tamanho):
            for j in range(self.tamanho):

                x2 = LARGURA/2 + (-self.x_OffSet + (self.x_OffSet/4 * j)) # calculando a posição na tela 
                y2 = ALTURA/2 + (-self.y_OffSet + (self.y_OffSet/4 * i))

                dist = math.dist((x1,y1),(x2,y2))

                if (dist < closest_dist):
                    closest_dist = dist
                    closest = [(x2,y2),(i,j)]


        return closest


    def TryChangePecaPlace(self, peca):

        closest = self.ClosePlace(peca.x,peca.y)
        # print(closest)
        
        if (self.tabuleiro[closest[1][0]][closest[1][1]] != None):
            peca.SetCoord(peca.start_x,peca.start_y,True)
            return
        self.tabuleiro[peca.start_linha][peca.start_coluna] = None
        self.tabuleiro[closest[1][0]][closest[1][1]] = peca

        peca.SetCoord(closest[0][0],closest[0][1],True)
        peca.SetTabCoord(closest[1][0],closest[1][1],True)


        



