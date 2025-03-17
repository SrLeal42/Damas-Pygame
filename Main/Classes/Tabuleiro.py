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
                    PG.draw.circle(window,BLACK,(LARGURA/2 + (-self.x_OffSet + (self.x_OffSet/4 * j)),ALTURA/2 + (-self.y_OffSet + (self.y_OffSet/4 * i))),2)
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

        print(closest)
        return closest


    def VerifyMove(self, linha:int, coluna:int, peca:Peca):
        orientacao_peca = -1 if peca.cor == 0 else 1
        dif_linha = linha - peca.start_linha
        dif_coluna = coluna - peca.start_coluna
        
        alguma_peca_capturada = False

        if (dif_linha == 0 or dif_coluna == 0):
            return {"canMove": False, "mensage":"Não movel"}
        
        if (self.tabuleiro[linha][coluna] != None):
            return {"canMove": False, "mensage":"Há uma peça no local"}
        
        # Peça normal
        if (peca.tipo == 0):

            # Verificando a direção
            if ((orientacao_peca < 0) != (dif_linha < 0)):
                return {"canMove": False, "mensage":"Direção incorreta"}
            
            # Verificando quantidade de quadrados pulados 
            if (abs(dif_coluna) > 2 or abs(dif_linha) > 2):
                return {"canMove": False, "mensage":"Pulou casas demais"}
            
            if (abs(dif_coluna) == 2 or abs(dif_linha) == 2):

                linha_between = linha + (orientacao_peca * -1)

                orientacao_coluna = -1 if dif_coluna < 0 else 1
                coluna_between = coluna + (orientacao_coluna * -1)

                peca_between = self.tabuleiro[linha_between][coluna_between]

                if (peca_between == None or peca_between.cor == peca.cor):
                    return {"canMove": False, "mensage":"Não pode se mover para essa casa"}
                else:
                    alguma_peca_capturada = True
                    peca_between.CapturarPeca(self.tabuleiro)
        else:
            
            orientacao_coluna = -1 if dif_coluna < 0 else 1
            orientacao_linha = -1 if dif_linha < 0 else 1

            for dif in range(abs(dif_coluna) - 1):

                ver_linha = peca.start_linha + (dif + 1) * orientacao_linha
                ver_coluna = peca.start_coluna + (dif + 1) * orientacao_coluna

                content = self.tabuleiro[ver_linha][ver_coluna]

                if (content == None):
                    continue

                if (content.cor == peca.cor):
                    return {"canMove": False, "mensage":"Há peças da mesma cor da peça movida no caminho"}
                
                if (linha != (ver_linha + 1 * orientacao_linha) or coluna != (ver_coluna + 1 * orientacao_coluna)):
                    return {"canMove": False, "mensage":"Não pode se mover para essa casa"}

                alguma_peca_capturada = True
                content.CapturarPeca(self.tabuleiro)


        return {"canMove": True, "mensage":"Sucess", "pecaCapturada":alguma_peca_capturada}


    def TryChangePecaPlace(self, peca, game):

        closest = self.ClosePlace(peca.x,peca.y)
        # print(closest)
        
        response = self.VerifyMove(closest[1][0],closest[1][1],peca)
        # print(response)
        if (not response["canMove"]):
            peca.SetCoord(peca.start_x,peca.start_y,True)
            return response

        if (game.sequencia_captura and not response["pecaCapturada"]):
            peca.SetCoord(peca.start_x,peca.start_y,True)
            return {"canMove":False, "mensage":"Em uma sequencia de captura voce deve se movimentar apenas capturando outras peças", "pecaCapturada":False}

        self.tabuleiro[peca.start_linha][peca.start_coluna] = None
        self.tabuleiro[closest[1][0]][closest[1][1]] = peca

        peca.SetCoord(closest[0][0],closest[0][1],True)
        peca.SetTabCoord(closest[1][0],closest[1][1],True)

        return response
    
    def VerifyPecaCanCapture(self, peca:Peca):

        orientacao_peca = -1 if peca.cor == 0 else 1

        if (peca.tipo == 0):
            linha = peca.linha + orientacao_peca if peca.linha + orientacao_peca < self.tamanho and peca.linha + orientacao_peca >= 0 else None 
            peca_esquerda = self.tabuleiro[linha][peca.coluna - 1] if (peca.coluna - 1 < self.tamanho and peca.coluna - 1 >= 0) and linha != None else None
            peca_direita = self.tabuleiro[linha][peca.coluna + 1] if (peca.coluna + 1 < self.tamanho and peca.coluna + 1 >= 0) and linha != None else None

            canCaptureLeft = False
            canCaptureRight = False

            quad_vazio_linha = peca.linha + (2 * orientacao_peca) if peca.linha + (2 * orientacao_peca) < self.tamanho and peca.linha + (2 * orientacao_peca) >= 0 else None

            # Verificando a esquerda 
            if (peca_esquerda != None):
                
                quad_vazio_esquerda = self.tabuleiro[quad_vazio_linha][peca.coluna - 2] if (peca.coluna - 2 < self.tamanho and peca.coluna - 2 >= 0) and quad_vazio_linha != None else -1
                if (peca.cor == peca_esquerda.cor):
                    
                    canCaptureLeft = False
                elif (quad_vazio_esquerda != None):
                    canCaptureLeft = False
                else: 
                    canCaptureLeft = True

            # Verificando a direita
            if (peca_direita != None):
                
                quad_vazio_direita = self.tabuleiro[quad_vazio_linha][peca.coluna + 2] if (peca.coluna + 2 < self.tamanho and peca.coluna + 2 >= 0) and quad_vazio_linha != None else -1

                if (peca.cor == peca_direita.cor):
                    
                    canCaptureRight = False
                elif (quad_vazio_direita != None):
                    
                    canCaptureRight = False
                else:
                    
                    canCaptureRight = True
            
            return canCaptureLeft or canCaptureRight
        
        else:
            
            for direct in range(4): # 4 pois são quatro direções: cima-direita, cima-esquerda, baixo-esquerda e baixo-direita
                orientacao_linha = -1 if direct <= 1 else 1
                
                orientacao_coluna = -1 if direct == 1 or direct == 3 else 1
                
                for i in range(1,self.tamanho):

                    linha = peca.start_linha + (i * 1) * orientacao_linha
                    coluna = peca.start_coluna + (i * 1) * orientacao_coluna

                    if (linha >= self.tamanho or linha < 0 or coluna >= self.tamanho or coluna < 0):
                        break

                    content = self.tabuleiro[linha][coluna]
                    
                    if (content == None):
                        continue

                    if (content.cor == peca.cor):
                        break
                    
                    next_linha = linha + 1 * orientacao_linha
                    next_coluna = coluna + 1 * orientacao_coluna

                    if (next_linha >= self.tamanho or next_linha < 0 or next_coluna >= self.tamanho or next_coluna < 0):
                        break

                    next_content = self.tabuleiro[next_linha][next_coluna]

                    if (next_content == None):
                        return True
        
        return False


        



