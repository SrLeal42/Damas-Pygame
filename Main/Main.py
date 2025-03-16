import pygame as PG
from Config import LARGURA, ALTURA,GRAY,BLACK
from Classes.Pecas import Peca
from Classes.Tabuleiro import Tabuleiro
from Classes.Game import Game


PG.init()

running = True

window = PG.display.set_mode((LARGURA,ALTURA))
PG.display.set_caption("Damas")

current_game = None

peca_being_dragged = None

def CreateGame():
    global current_game 
    current_game = Game()



def HandlePecasClick():
    if current_game == None:
        return
    
    mouse_pos = PG.mouse.get_pos()
    global peca_being_dragged

    for linha in range(current_game.tabuleiro.tamanho):
        for coluna in range(current_game.tabuleiro.tamanho):
            p = current_game.tabuleiro.tabuleiro[linha][coluna]
            if p == None:
                continue
            x = p.x - p.tamanho
            y = p.y - p.tamanho
            ret = PG.Rect(x, y, p.tamanho*2, p.tamanho*2)
            colidiu = ret.collidepoint(mouse_pos)
            
            # PG.draw.rect(window, BLACK, ret)
            
            if colidiu and (peca_being_dragged == None or peca_being_dragged == p):
                peca_being_dragged = p
                p.SetCoord(mouse_pos[0],mouse_pos[1])
                break



def HandlePecasRelease():
    global peca_being_dragged

    if peca_being_dragged == None:
        return

    current_game.tabuleiro.TryChangePecaPlace(peca_being_dragged)

    peca_being_dragged = None



while(running):

    window.fill(GRAY)

    if (current_game == None):
         CreateGame()

    current_game.tabuleiro.DesenhaTabuleiro(window)

    mouse = PG.mouse.get_pressed()

    if mouse[0]:
        HandlePecasClick()
    elif peca_being_dragged:
        HandlePecasRelease()

    for evento in PG.event.get():
        if evento.type == PG.QUIT:
            running = False
            # for i in range(current_game.tabuleiro.tamanho):
            #     for j in range(current_game.tabuleiro.tamanho):
            #         if current_game.tabuleiro.tabuleiro[i][j]:
            #             print(current_game.tabuleiro.tabuleiro[i][j].capturada)
            #         else:
            #             print(None)

    PG.display.flip()



    