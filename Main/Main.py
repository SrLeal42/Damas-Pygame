import pygame as PG
from Config import LARGURA, ALTURA,GRAY,BLACK,FONTE_PRIN
from Classes.Pecas import Peca
from Classes.Tabuleiro import Tabuleiro
from Classes.Game import Game


PG.init()

running = True

window = PG.display.set_mode((LARGURA,ALTURA))
PG.display.set_caption("Damas")

state = "gaming"

current_game = None

peca_being_dragged = None
last_peca_moved = None

fonte_principal = PG.font.Font(FONTE_PRIN, 40)

fonte_win_text = PG.font.Font(FONTE_PRIN, 60)

def CreateGame(jogo:str):
    global current_game 
    current_game = Game(jogo)



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

            # x = p.x - p.tamanho
            # y = p.y - p.tamanho

            # ret = PG.Rect(x, y, p.tamanho*2, p.tamanho*2)
            
            ret = p.rect

            colidiu = ret.collidepoint(mouse_pos)
            
            # PG.draw.rect(window, BLACK, ret)
            
            if colidiu and (peca_being_dragged == None or peca_being_dragged == p):
                if (current_game.cor_rodada != p.cor):
                    break

                if (current_game.sequencia_captura and p != last_peca_moved):# Caso o player esteja em uma sequencia de captura e ele deve mover a apenas a ultima peça que ele moveu  
                    break

                peca_being_dragged = p
                p.SetCoord(mouse_pos[0],mouse_pos[1])
                p.sendo_arrastada = True
                break





def HandlePecasRelease():
    global peca_being_dragged, current_game, last_peca_moved, state

    if peca_being_dragged == None:
        return

    response = current_game.tabuleiro.TryChangePecaPlace(peca_being_dragged,current_game)
    last_peca_moved = peca_being_dragged

    peca_being_dragged.sendo_arrastada = False
    peca_being_dragged = None

    if (not response["canMove"]):
        return

    if (not response["turnThisRound"] and (response["pecaCapturada"] or current_game.sequencia_captura)):
        canCapture = current_game.tabuleiro.VerifyPecaCanCapture(last_peca_moved)
        
        current_game.sequencia_captura = canCapture
        # print(canCapture)

    winnigResponse = current_game.WinningUpdate()

    if (winnigResponse["gameEnd"]):
        state = "winScreen"
        print(winnigResponse)

    current_game.EndTurn()





def DrawCorRodada():
    global current_game
    global window

    if current_game == None:
        return
    
    text = "Preto" if current_game.cor_rodada == 1 else "Branco"
    
    text_render = fonte_principal.render(text, True, BLACK)  # Atualiza o texto

    window.blit(text_render, (LARGURA/2 - 50, 10))

def DrawWinScreen():
    global current_game,window
 
    if current_game == None:
        return
    
    text = "As Pretas ganharam" if current_game.colorWinner == 1 else "As Brancas ganharam"
    
    text_render = fonte_win_text.render(text, True, BLACK)  # Atualiza o texto

    window.blit(text_render, (LARGURA/2 - 230, ALTURA/2 - 60))





while(running):

    window.fill(GRAY)



    if (state == "gaming"):

        if (current_game == None):
            CreateGame("damas")

        current_game.tabuleiro.DesenhaTabuleiro(window)

        DrawCorRodada()

        mouse = PG.mouse.get_pressed()

        if mouse[0]:
            HandlePecasClick()
        elif peca_being_dragged:
            HandlePecasRelease()
    
    elif (state == "winScreen"):

        if (current_game != None):
            current_game.tabuleiro.DesenhaTabuleiro(window)
            DrawCorRodada()

        DrawWinScreen()




    for evento in PG.event.get():
        if evento.type == PG.QUIT:
            running = False



            # for i in range(current_game.tabuleiro.tamanho):
            #     for j in range(current_game.tabuleiro.tamanho):
            #         if (current_game.tabuleiro.tabuleiro[i][j] != None):
            #             print(current_game.tabuleiro.tabuleiro[i][j])
            #         else:
            #             print(None)

    PG.display.flip()



    