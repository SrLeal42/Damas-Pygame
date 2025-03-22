import pygame as PG
import math
from Classes.Pecas import Peca
from Config import LARGURA,ALTURA,NUM_PECAS_XADREZ,WHITE,BLACK,GRAY,GOLDEN_BLACK,GOLDEN_WHITE,DARK_GRAY


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


    def AdicionaPecasAoTabuleiro(self,Pecas,jogo:str,cor:int):

        indexPecas = 0
        indexlinhas = 0
        pularLinhas = 0
        

        if (jogo == "damas"):
            
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

        elif (jogo == "xadrez"):
            
            pularLinhas = 6 if cor == 1 else 0 # Dependendo da cor da peca pular um numero de linhas

            pecas_count = 0 # Contador de peças que foram alocadas no tabuleiro
            
            for i in range(self.tamanho):
                if i < pularLinhas:
                    continue

                indexlinhas += 1
                
                if indexlinhas > 2:
                    break

                for j in range(self.tamanho):

                    peca = Pecas[indexPecas]   

                    y = ALTURA/2 + (-self.y_OffSet + (self.y_OffSet/4 * i))

                    if (peca.tipo == 2 or peca.tipo == 6 or peca.tipo == 7):

                        x = LARGURA/2 + (-self.x_OffSet + (self.x_OffSet/4 * j))

                        peca.SetCoord(x,y,True)
                        peca.SetTabCoord(i,j,True)

                        self.tabuleiro[i][j] = peca
                        
                        indexPecas += 1
                        pecas_count += 1

                    elif (peca.tipo > 2 and peca.tipo < 6): # (peca.tipo > 2 and peca.tipo < 6):
 
                        x_1 = LARGURA/2 + (-self.x_OffSet + (self.x_OffSet/4 * j))
                        
                        peca.SetCoord(x_1,y,True)
                        peca.SetTabCoord(i,j,True)

                        self.tabuleiro[i][j] = peca

                        # Partimos do presuposto que a proxima peça é do mesmo tipo que a anterior
                        proxima_peca = Pecas[indexPecas+1]
                        
                        coluna_inversa = (self.tamanho - 1) - j

                        x_2 = LARGURA/2 + (-self.x_OffSet + (self.x_OffSet/4 * coluna_inversa))

                        proxima_peca.SetCoord(x_2,y,True)
                        proxima_peca.SetTabCoord(i,coluna_inversa,True)
                        
                        self.tabuleiro[i][coluna_inversa] = proxima_peca

                        indexPecas += 2
                        pecas_count += 2

                    if (pecas_count == NUM_PECAS_XADREZ//2 or pecas_count == NUM_PECAS_XADREZ):
                        break



            


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

        # Desenhando os quadrados
        for i in range(self.tamanho):
            for j in range(self.tamanho):

                peca = self.tabuleiro[i][j]
                x = LARGURA/2 + (-self.x_OffSet + (self.x_OffSet/4 * j))
                y = ALTURA/2 + (-self.y_OffSet + (self.y_OffSet/4 * i))

                if j % 2 == i % 2:
                    quad_tam = 63
                    PG.draw.rect(window,DARK_GRAY,(x-quad_tam/2,y-quad_tam/2,quad_tam,quad_tam))
                    # PG.draw.circle(window,BLACK,(LARGURA/2 + (-self.x_OffSet + (self.x_OffSet/4 * j)),ALTURA/2 + (-self.y_OffSet + (self.y_OffSet/4 * i))),2)

                
                


        peca_being_dragged = None

        # Desenhado as peças 
        for i in range(self.tamanho):
            for j in range(self.tamanho):
                
                peca = self.tabuleiro[i][j]
                
                if (peca == None):
                    continue
                
                if (peca.sendo_arrastada):
                    peca_being_dragged = peca
                    continue
                    
                grupo_sprite = PG.sprite.Group(peca)
                grupo_sprite.draw(window)
                # color = WHITE if peca.cor == 0 else BLACK
                
                # if (peca.tipo == 1):
                #     color = GOLDEN_WHITE if color == WHITE else GOLDEN_BLACK

                # PG.draw.circle(window,color,(peca.x,peca.y),peca.tamanho)

        # Desenhando a peça que esta sendo arrastada por ultimo para deixar ela sobre as outras
        if(peca_being_dragged != None):
            grupo_sprite = PG.sprite.Group(peca_being_dragged)
            grupo_sprite.draw(window)

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

        # print(closest)
        return closest


    def VerifyMove(self, linha:int, coluna:int, peca:Peca):
        orientacao_peca = -1 if peca.cor == 0 else 1
        dif_linha = linha - peca.start_linha
        dif_coluna = coluna - peca.start_coluna
        
        dif_linha_abs =  abs(dif_linha)
        dif_coluna_abs =  abs(dif_coluna)

        alguma_peca_capturada = False

        if (dif_linha == 0 and dif_coluna == 0):
            return {"canMove": False, "mensage":"Não movel"}
        
        content = self.tabuleiro[linha][coluna]

        if (content != None and content.cor == peca.cor):
            return {"canMove": False, "mensage":"Há uma peça da mesma cor no local"}
        
        # Peça normal
        if (peca.tipo == 0):

            if(dif_linha_abs != dif_coluna_abs):
                return {"canMove": False, "mensage":"Movimento invalido"}

            if (self.tabuleiro[linha][coluna] != None):
                return {"canMove": False, "mensage":"Há uma peça no local"}

            # Verificando a direção
            if ((orientacao_peca < 0) != (dif_linha < 0)):
                return {"canMove": False, "mensage":"Direção incorreta"}
            
            # Verificando quantidade de quadrados pulados 
            if (dif_coluna_abs > 2 or dif_linha_abs > 2):
                return {"canMove": False, "mensage":"Pulou casas demais"}
            
            if (dif_coluna_abs == 2 or dif_linha_abs == 2):

                linha_between = linha + (orientacao_peca * -1)

                orientacao_coluna = -1 if dif_coluna < 0 else 1
                coluna_between = coluna + (orientacao_coluna * -1)

                peca_between = self.tabuleiro[linha_between][coluna_between]

                if (peca_between == None or peca_between.cor == peca.cor):
                    return {"canMove": False, "mensage":"Não pode se mover para essa casa"}
                else:
                    alguma_peca_capturada = True
                    peca_between.CapturarPeca(self.tabuleiro)

            # Peça Damas
        elif (peca.tipo == 1):
            
            if(dif_linha_abs != dif_coluna_abs):
                return {"canMove": False, "mensage":"Movimento invalido"}

            if (self.tabuleiro[linha][coluna] != None):
                return {"canMove": False, "mensage":"Há uma peça no local"}

            orientacao_coluna = -1 if dif_coluna < 0 else 1
            orientacao_linha = -1 if dif_linha < 0 else 1

            for dif in range(dif_coluna_abs - 1):

                ver_linha = peca.start_linha + (dif + 1) * orientacao_linha
                ver_coluna = peca.start_coluna + (dif + 1) * orientacao_coluna

                if (content == None):
                    continue

                if (content.cor == peca.cor):
                    return {"canMove": False, "mensage":"Há peças da mesma cor da peça movida no caminho"}
                
                if (linha != (ver_linha + 1 * orientacao_linha) or coluna != (ver_coluna + 1 * orientacao_coluna)):
                    return {"canMove": False, "mensage":"Não pode se mover para essa casa"}

                alguma_peca_capturada = True
                content.CapturarPeca(self.tabuleiro)


            # Peça Peão
        elif (peca.tipo == 2):
            
            if (dif_linha == 0):
                return {"canMove": False, "mensage":"Movimento invalido"}
            
            if ((orientacao_peca < 0) != (dif_linha < 0)):
                return {"canMove": False, "mensage":"Direção incorreta"}

            if ((dif_linha_abs > 2 or dif_coluna_abs > 1) or (dif_linha_abs == 2 and not peca.primeiro_movimento)):
                return {"canMove": False, "mensage":"Pulou quadrados demais"}

            if (dif_linha_abs == 1 and dif_coluna_abs == 1):
                
                if (content == None):
                    return {"canMove": False, "mensage":"Movimento invalido"}
                
                alguma_peca_capturada = True

                content.CapturarPeca(self.tabuleiro)
            
            elif (dif_linha_abs <= 2):

                if (content != None):
                    return {"canMove": False, "mensage":"Há uma peça no local"}
                
                if (dif_linha_abs == 2 and (self.tabuleiro[linha - (1 * orientacao_peca)][coluna] != None)):
                    return {"canMove": False, "mensage":"O peão não pode pular peças"}

        elif (peca.tipo == 3):

            if (dif_linha_abs != 0 and dif_coluna_abs != 0):
                return {"canMove": False, "mensage":"Movimento invalido"}

            qtd_quadrados_pulados = dif_coluna_abs if dif_coluna_abs > dif_linha_abs else dif_linha_abs

            direcao_mov = "horizontal" if dif_coluna_abs > dif_linha_abs else "vertical"

            orientacao_coluna = -1 if dif_coluna < 0 else 1
            orientacao_linha = -1 if dif_linha < 0 else 1

            for i in range(qtd_quadrados_pulados -1):
                
                _linha = peca.start_linha
                _coluna = peca.start_coluna

                if (direcao_mov == "vertical"):
                    _linha = peca.start_linha + (i + 1) * orientacao_linha
                else:
                    _coluna = peca.start_coluna + (i + 1) * orientacao_coluna

                # print(f"{_linha} {_coluna}")

                _content = self.tabuleiro[_linha][_coluna]

                if (_content != None):
                    return {"canMove": False, "mensage":"Há uma peça no caminho"}
                
            if (content != None):
                alguma_peca_capturada = True
                content.CapturarPeca(self.tabuleiro)

        elif (peca.tipo == 4):

            if (dif_linha_abs != 2 or dif_coluna_abs != 1):
                return {"canMove": False, "mensage":"Movimento invalido"}

            if (content != None):

                alguma_peca_capturada = True
                content.CapturarPeca(self.tabuleiro)

        elif (peca.tipo == 5):
            
            if(dif_linha_abs != dif_coluna_abs):
                return {"canMove": False, "mensage":"Movimento invalido"}

            orientacao_coluna = -1 if dif_coluna < 0 else 1
            orientacao_linha = -1 if dif_linha < 0 else 1

            for dif in range(dif_coluna_abs - 1):

                ver_linha = peca.start_linha + (dif + 1) * orientacao_linha
                ver_coluna = peca.start_coluna + (dif + 1) * orientacao_coluna

                _content = self.tabuleiro[ver_linha][ver_coluna]

                if (_content != None):
                    return {"canMove": False, "mensage":"Há peças no caminho"}



            if (content != None):
                alguma_peca_capturada = True
                content.CapturarPeca(self.tabuleiro)

        elif (peca.tipo == 6):

            if((dif_linha_abs != dif_coluna_abs) and (dif_linha_abs != 0 and dif_coluna_abs != 0)):
                return {"canMove": False, "mensage":"Movimento invalido"}

            qtd_quadrados_pulados = dif_coluna_abs if dif_coluna_abs > dif_linha_abs else dif_linha_abs

            orientacao_coluna = -1 if dif_coluna < 0 else 1
            orientacao_linha = -1 if dif_linha < 0 else 1

            index_linha = 0
            index_coluna = 0

            for i in range(qtd_quadrados_pulados -1 ):
                index_linha += 1 if index_linha < dif_linha_abs else 0
                index_coluna += 1 if index_coluna < dif_coluna_abs else 0

                _linha = peca.start_linha + index_linha * orientacao_linha
                _coluna = peca.start_coluna + index_coluna * orientacao_coluna
                # print(f"{_linha},{_coluna}")
                _content = self.tabuleiro[_linha][_coluna]

                if (_content != None):
                    return {"canMove": False, "mensage":"Há peças no caminho"}

            if (content != None):
                alguma_peca_capturada = True
                content.CapturarPeca(self.tabuleiro)
        
        
        elif (peca.tipo == 7):

            if(dif_linha_abs > 1 or dif_coluna_abs > 1):
                return {"canMove": False, "mensage":"Movimento invalido"}
            
            if (content != None):
                alguma_peca_capturada = True
                content.CapturarPeca(self.tabuleiro)
      
        
        return {"canMove": True, "mensage":"Sucess", "pecaCapturada":alguma_peca_capturada}


    def TryChangePecaPlace(self, peca, game):

        closest = self.ClosePlace(peca.x,peca.y)
        # print(closest)
        
        response = self.VerifyMove(closest[1][0],closest[1][1],peca)
        
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

        peca.primeiro_movimento = False

        turn = False # Deve ou não transforma a peça em Dama

        if (game.jogo == "damas"):
            turn = self.TurnPecaInToDamaVerification(peca)

            if(turn):
                peca.TurnPecaInToDama()

        response["turnThisRound"] = turn
        
        print(response)
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
        
        elif (peca.tipo == 1):
            
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


    def TurnPecaInToDamaVerification(self, peca:Peca):
        return (peca.linha == self.tamanho-1 and (peca.cor == 1 and peca.tipo == 0)) or (peca.linha == 0 and (peca.cor == 0 and peca.tipo == 0))


