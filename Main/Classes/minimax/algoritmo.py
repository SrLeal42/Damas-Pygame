import pygame as PG
from copy import deepcopy, copy
from Config import NUM_PECAS_DAMAS
from Classes.Tabuleiro import Tabuleiro
from Classes.Pecas import Peca


def minimax(position, depth, max_player, game):
    
    if depth == 0 or (position.num_pretas_capturadas >= NUM_PECAS_DAMAS or position.num_brancas_capturadas >= NUM_PECAS_DAMAS):
        return position.EvalueteBoard(), position

    # print(GetAllMoves(position, 1, game))

    # return 0,0,0

    if max_player:
        maxEval = float('-inf')
        best_move = None
        peca_to_move = None

        for move in GetAllMoves(position, 1, game):
            evaluation = minimax(move[0], depth-1, False, game)[0]
            maxEval = max(maxEval, evaluation)

            if (maxEval == evaluation):
                best_move = move[1]
                peca_to_move = move[2]


        return maxEval, best_move, peca_to_move

    else:
        minEval = float('inf')
        best_move = None
        peca_to_move = None

        for move in GetAllMoves(position, 0, game):
            evaluation = minimax(move[0], depth-1, True, game)[0]
            minEval = min(minEval, evaluation)

            if (minEval == evaluation):
                best_move = move[1]
                peca_to_move = move[2]
                


        return minEval, best_move, peca_to_move



def SimulateMove(peca, move, tabuleiro, game):
    tabuleiro.TryChangePecaPlace(peca, game, move[0], move[1])
    # print(peca)
    # tabuleiro.tabuleiro[peca.start_linha][peca.start_coluna] = None

    return tabuleiro


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



def GetAllMoves(tabuleiro, color, game):

    moves = []

    for peca in tabuleiro.GetAllPecas(color):

        valid_moves = []

        for i in range(tabuleiro.tamanho):
            for j in range(tabuleiro.tamanho):

                response = tabuleiro.VerifyMove( i, j, peca)

                if (response["canMove"]):
                    # print(response["canMove"], i, j)
                    valid_moves.append((i,j))
        
        for move in valid_moves:
            # print(id(tabuleiro))
            temp_tabu = CopyBoard(tabuleiro)
            # print(id(temp_tabu))
            temp_peca = temp_tabu.tabuleiro[peca.start_linha][peca.start_coluna]
            # print(id(temp_peca))
            # print(tabuleiro.tabuleiro[peca.start_linha][peca.start_coluna])
            new_tabu = SimulateMove(temp_peca, move, temp_tabu, game)
            # print(tabuleiro.tabuleiro[peca.start_linha][peca.start_coluna])
            # print(peca.linha, peca.coluna)
            # print(temp_peca.linha, temp_peca.coluna)
            moves.append([new_tabu, move, peca])
        
        # if (len(moves) > 0 ):
        #     return moves

    return moves






