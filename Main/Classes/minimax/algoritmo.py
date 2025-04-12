import pygame as PG
from copy import deepcopy, copy
from Config import NUM_PECAS_DAMAS
from Classes.Tabuleiro import Tabuleiro
from Classes.Pecas import Peca


def minimax(position, depth, max_player, game, isStrBoard=False):
    
    strBoard = ConvertBoardToString(position) if not isStrBoard else position

    if depth == 0:
        return EvalueteBoard(strBoard), position

    # print(GetAllMoves(strBoard, 1, game))

    # return 0,0,0

    if max_player:
        maxEval = float('-inf')
        best_move = None
        peca_to_move = None

        for move in GetAllMoves(strBoard, 1, game):
            # print(move[0])
            evaluation = minimax(move[0], depth-1, False, game, True)[0]
            maxEval = max(maxEval, evaluation)

            if (maxEval == evaluation):
                best_move = move[1]
                peca_to_move = move[2]


        return maxEval, best_move, peca_to_move

    else:
        minEval = float('inf')
        best_move = None
        peca_to_move = None

        for move in GetAllMoves(strBoard, 0, game):
            evaluation = minimax(move[0], depth-1, True, game, True)[0]
            minEval = min(minEval, evaluation)

            if (minEval == evaluation):
                best_move = move[1]
                peca_to_move = move[2]
                
        return minEval, best_move, peca_to_move



def SimulateMove(peca, strPeca:str, move, tabuleiro, game):
    new_tab = TryChangePecaPlaceStrBoard(tabuleiro, strPeca, peca, game, move[0], move[1])
    # print(peca)
    # tabuleiro.tabuleiro[peca.start_linha][peca.start_coluna] = None

    return new_tab


def CopyBoard(tabuleiro):

    new_tab = Tabuleiro()

    new_tab.num_brancas_capturadas = tabuleiro.num_brancas_capturadas
    new_tab.num_pretas_capturadas = tabuleiro.num_pretas_capturadas

    for i in range(tabuleiro.tamanho):
            for j in range(tabuleiro.tamanho):

                content = tabuleiro.tabuleiro[i][j]
                if (content == None):
                    new_tab.tabuleiro[i][j] = None
                else:
                    new_peca = Peca(content.cor,content.linha,content.coluna,content.escala,content.x,content.y,content.tipo)
                    new_tab.tabuleiro[i][j] = new_peca

    return new_tab



# def GetAllMoves(tabuleiro, color, game):

#     moves = []

#     for peca in tabuleiro.GetAllPecas(color):

#         valid_moves = []

#         for i in range(tabuleiro.tamanho):
#             for j in range(tabuleiro.tamanho):

#                 response = tabuleiro.VerifyMove( i, j, peca)

#                 if (response["canMove"]):
#                     # print(response["canMove"], i, j)
#                     valid_moves.append((i,j))
        
#         for move in valid_moves:
#             # print(id(tabuleiro))
#             temp_tabu = CopyBoard(tabuleiro)
#             # print(id(temp_tabu))
#             temp_peca = temp_tabu.tabuleiro[peca.start_linha][peca.start_coluna]
#             # print(id(temp_peca))
#             # print(tabuleiro.tabuleiro[peca.start_linha][peca.start_coluna])
#             new_tabu = SimulateMove(temp_peca, move, temp_tabu, game)
#             # print(tabuleiro.tabuleiro[peca.start_linha][peca.start_coluna])
#             # print(peca.linha, peca.coluna)
#             # print(temp_peca.linha, temp_peca.coluna)
#             moves.append([new_tabu, move, peca])
        
#         # if (len(moves) > 0 ):
#         #     return moves

#     return moves


def GetAllMoves(board, color:int, game):

    moves = []

    for strPeca in GetAllPecas(board, color):

        valid_moves = []

        tipo = 0 if strPeca[0] == "1" or strPeca[0] == "2" else 1

        peca = Peca(color, strPeca[1], strPeca[2], 3, tipo=tipo)

        for i in range(len(board)):
            for j in range(len(board)):

                response = VerifyMoveStrDamas(board, i, j, peca)

                if (response["canMove"]):
                    # print("COORDS: ", strPeca[1], strPeca[2])
                    # print(response["canMove"], i, j)
                    valid_moves.append((i,j))

        for move in valid_moves:
            temp_tabu = deepcopy(board)
            new_tabu = SimulateMove(peca, strPeca[0], move, temp_tabu, game)
            moves.append([new_tabu, move, (strPeca[1], strPeca[2])])



    return moves




def ConvertBoardToString(board:Tabuleiro):
    # 0 = None / 1 = Peca preta comum / 2 = Peca branca comum / 3 = Damas preta / 4 = Damas branca
    strTab = []

    for i in range(board.tamanho):
            
            coluna = []

            for j in range(board.tamanho):

                content = board.tabuleiro[i][j]

                if (content == None):

                    coluna.append("0")

                elif (content.cor == 0):

                    p = "2" if content.tipo == 0 else "4"
                    coluna.append(p)
                
                else:

                    p = "1" if content.tipo == 0 else "3"
                    coluna.append(p)

            strTab.append(coluna)


    # for i in range(board.tamanho):
    #     for j in range(board.tamanho):
    #         print(strTab[i][j])

    return strTab

def EvalueteBoard(board):
    # print(board)
    num_pecas_brancas = 0
    num_pecas_pretas = 0
    num_damas_brancas = 0
    num_damas_pretas = 0

    for i in range(len(board)):
        for j in range(len(board)):

            content = board[i][j]

            if (content == "0"):
                continue

            if (content == "1" or content == "3"):
                num_pecas_pretas += 1
                
                if (content == "3"):
                    num_damas_pretas += 1

            if (content == "2" or content == "4"):
                num_pecas_brancas += 1
                
                if (content == "4"):
                    num_damas_brancas += 1


    return num_pecas_pretas - num_pecas_brancas + (num_damas_brancas * .5 - num_damas_pretas * .5)

            

def GetAllPecas(board, color:int):

    strPecas = []

    for i in range(len(board)):
        for j in range(len(board)):

            content = board[i][j]

            if (content == "0"):
                continue
            
            if (color == 0):
                if (content == "2" or content == "4"):
                    strPecas.append((content, i, j))
            else:
                if (content == "1" or content == "3"):
                    strPecas.append((content, i, j))
        

    return strPecas



def VerifyMoveStrDamas(board, linha:int, coluna:int, peca:Peca):
    
    if(peca == None):
        return {"canMove": False, "mensage":"Peca não atribuida"}

    orientacao_peca = -1 if peca.cor == 0 else 1
    dif_linha = linha - peca.start_linha
    dif_coluna = coluna - peca.start_coluna
    
    dif_linha_abs =  abs(dif_linha)
    dif_coluna_abs =  abs(dif_coluna)

    alguma_peca_capturada = None

    if (dif_linha == 0 and dif_coluna == 0):
        return {"canMove": False, "mensage":"Não movel"}
    
    content = board[linha][coluna]

    if (content != "0"):
            return {"canMove": False, "mensage":"Há uma peça no local"}
    
    # Peça normal
    if (peca.tipo == 0):

        if(dif_linha_abs != dif_coluna_abs):
            return {"canMove": False, "mensage":"Movimento invalido"}

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

            peca_between = board[linha_between][coluna_between]

            if ((peca_between == "1" or peca_between == "3") and peca.cor == 1):
                return {"canMove": False, "mensage":"Não pode se mover para essa casa"}
            
            if ((peca_between == "0" or peca_between == "2") and peca.cor == 0):
                return {"canMove": False, "mensage":"Não pode se mover para essa casa"}

            if (peca_between == "0"):
                return {"canMove": False, "mensage":"Não pode se mover para essa casa"}

            alguma_peca_capturada = [peca_between, linha_between, coluna_between]
        
        else: 

            canCapture = VerifyPecaCanCaptureStrBoard(board, peca)
            # print(canCapture)
            if (canCapture):
                return {"canMove": False, "mensage":"Voce deve capturar a peça adjacente"}


        # Peça Damas
    elif (peca.tipo == 1):
        
        if(dif_linha_abs != dif_coluna_abs):
            return {"canMove": False, "mensage":"Movimento invalido"}

        orientacao_coluna = -1 if dif_coluna < 0 else 1
        orientacao_linha = -1 if dif_linha < 0 else 1

        for dif in range(dif_coluna_abs - 1):

            ver_linha = peca.start_linha + (dif + 1) * orientacao_linha
            ver_coluna = peca.start_coluna + (dif + 1) * orientacao_coluna

            _content = board[ver_linha][ver_coluna]

            if (_content == "0"):
                continue
            
            if ((_content == "1" or _content == "3") and peca.cor == 1):
                return {"canMove": False, "mensage":"Não pode se mover para essa casa"}
            
            if ((_content == "0" or _content == "2") and peca.cor == 0):
                return {"canMove": False, "mensage":"Não pode se mover para essa casa"}
            
            # if (_content.cor == peca.cor):
            #     return {"canMove": False, "mensage":"Há peças da mesma cor da peça movida no caminho"}
            
            if (linha != (ver_linha + 1 * orientacao_linha) or coluna != (ver_coluna + 1 * orientacao_coluna)):
                return {"canMove": False, "mensage":"Não pode se mover para essa casa"}

            alguma_peca_capturada = [_content, ver_linha, ver_coluna]
            # _content.CapturarPeca(self)


        canCapture = VerifyPecaCanCaptureStrBoard(board, peca, True)
        
        if (canCapture and alguma_peca_capturada == None):
            return {"canMove": False, "mensage":"Voce deve capturar a peça adjacente"}
        

    return {"canMove": True, "mensage":"Sucess", "pecaCapturada":alguma_peca_capturada}



def VerifyPecaCanCaptureStrBoard(board, peca:Peca, mandatory_move:bool = False):

    orientacao_peca = -1 if peca.cor == 0 else 1

    boardTam = len(board)

    if (peca.tipo == 0):
        linha = peca.linha + orientacao_peca if peca.linha + orientacao_peca < boardTam and peca.linha + orientacao_peca >= 0 else None 
        peca_esquerda = board[linha][peca.coluna - 1] if (peca.coluna - 1 < boardTam and peca.coluna - 1 >= 0) and linha != None else None
        peca_direita = board[linha][peca.coluna + 1] if (peca.coluna + 1 < boardTam and peca.coluna + 1 >= 0) and linha != None else None

        canCaptureLeft = False
        canCaptureRight = False

        quad_vazio_linha = peca.linha + (2 * orientacao_peca) if peca.linha + (2 * orientacao_peca) < boardTam and peca.linha + (2 * orientacao_peca) >= 0 else None

        # Verificando a esquerda 
        if (peca_esquerda != None):
            
            quad_vazio_esquerda = board[quad_vazio_linha][peca.coluna - 2] if (peca.coluna - 2 < boardTam and peca.coluna - 2 >= 0) and quad_vazio_linha != None else -1
            
            if ((peca_esquerda == "1" or peca_esquerda == "3") and peca.cor == 1):
                
                canCaptureLeft = False
            
            elif ((peca_esquerda == "2" or peca_esquerda == "4") and peca.cor == 0):
                
                canCaptureLeft = False
            elif (quad_vazio_esquerda != None):

                canCaptureLeft = False
            else: 
                
                canCaptureLeft = True

        # Verificando a direita
        if (peca_direita != None):
            
            quad_vazio_direita = board[quad_vazio_linha][peca.coluna + 2] if (peca.coluna + 2 < boardTam and peca.coluna + 2 >= 0) and quad_vazio_linha != None else -1

            if ((peca_direita == "1" or peca_direita == "3") and peca.cor == 1):
                
                canCaptureLeft = False
            
            elif ((peca_direita == "2" or peca_direita == "4") and peca.cor == 0):

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
            
            for i in range(1, boardTam):

                if (mandatory_move and i > 1):
                    break

                linha = peca.start_linha + (i * 1) * orientacao_linha
                coluna = peca.start_coluna + (i * 1) * orientacao_coluna

                if (linha >= boardTam or linha < 0 or coluna >= boardTam or coluna < 0):
                    break

                content = board[linha][coluna]
                
                if (content == "0"):
                    continue
                
                if ((content == "1" or content == "3") and peca.cor == 1):
                    break

                if ((content == "2" or content == "4") and peca.cor == 0):
                    break
                
                next_linha = linha + 1 * orientacao_linha
                next_coluna = coluna + 1 * orientacao_coluna

                if (next_linha >= boardTam or next_linha < 0 or next_coluna >= boardTam or next_coluna < 0):
                    break

                next_content = board[next_linha][next_coluna]

                if (next_content == "0"):
                    return True
                
    
    return False



# TODO Adaptar essa função para um tabuleiro de string

def TryChangePecaPlaceStrBoard(board, strPeca:str, peca:Peca, game, linha:int, coluna:int):
    # print("TRTRTRT", id(self))
    # if (not linha or not coluna):
    #     closest = self.ClosePlace(peca.x,peca.y)
    #     # print(closest)
    #     response = self.VerifyMove(closest[1][0],closest[1][1],peca)
    # else:

    #     closest = [self.CalculateScreenPosition(linha,coluna), (linha,coluna)]
    #     # print("TRY: ", closest)
    #     response = self.VerifyMove(linha, coluna, peca)
    

    response = VerifyMoveStrDamas(board, linha, coluna, peca)

    
    if (not response["canMove"]):
        # peca.SetCoord(peca.start_x,peca.start_y,True)
        
        return response

    turn = False # Deve ou não transforma a peça em Dama

    turn = TurnStrPecaInToStrDamaVerification(strPeca, linha)

    if(turn):
        strPeca = "3" if strPeca == "1" else "4"

    # response["turnThisRound"] = turn

    if (response["pecaCapturada"]):
        board[response["pecaCapturada"][1]][response["pecaCapturada"][2]] = "0"
        # response["pecaCapturada"].CapturarPeca(self)

    board[peca.start_linha][peca.start_coluna] = "0"
    board[linha][coluna] = strPeca


    # print(response)
    return board


def TurnStrPecaInToStrDamaVerification(peca:str, linha:int):
        return (linha == 7 and peca == "1" ) or (linha == 0 and peca == "2" )