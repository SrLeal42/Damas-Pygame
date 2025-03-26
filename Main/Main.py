import pygame as PG
from Config import LARGURA, ALTURA,GRAY,BLACK,WHITE,FONTE_PRIN, PATH_SPRITE_PECA_BRANCA, PATH_SPRITE_PECA_PRETA
from Classes.Pecas import Peca
from Classes.Tabuleiro import Tabuleiro
from Classes.Game import Game
from Classes.Button import Button


PG.init()

running = True

window = PG.display.set_mode((LARGURA,ALTURA))
PG.display.set_caption("Damas")

state = "initialmenu"

start_button = Button(LARGURA//2, ALTURA//2 -50, "Main/Sprites/Torre.png", 4)
quit_button = Button(LARGURA//2, ALTURA//2 + 100, "Main/Sprites/Peao.png", 4)

damas_button = Button(LARGURA//2 - 100, ALTURA//2 , "Main/Sprites/PECA_BRANCA.png", 4)
xadrez_button = Button(LARGURA//2 + 100, ALTURA//2 , "Main/Sprites/PECA_PRETA.png", 4)

pause_button = Button(40,40,"Main/Sprites/Cavalo.png", 2)

resume_button = Button(LARGURA//2, ALTURA//2 -120, "Main/Sprites/Bispo.png", 3)
initial_menu_button = Button(LARGURA//2, ALTURA//2 , "Main/Sprites/Rainha.png", 3)
reset_button = Button(LARGURA//2, ALTURA//2 + 120, "Main/Sprites/Rei.png", 3)

selected_game = ""

current_game = None

peca_being_dragged = None
last_peca_moved = None

fonte_principal = PG.font.Font(FONTE_PRIN, 40)

fonte_win_text = PG.font.Font(FONTE_PRIN, 60)

def CreateGame(jogo:str):
    global current_game

    if (current_game != None):
        current_game.ResetGame(jogo)
        return

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


def DrawText(text:str, x:int, y:int, color, size:int):
    global window

    fonte = PG.font.Font(FONTE_PRIN, size)

    text_render = fonte.render(text, False, color)

    text_size = fonte.size(text)

    window.blit(text_render, (x - (text_size[0] // 2), y - (text_size[1] // 2)))


def DrawCorRodada():
    global current_game
    global window

    if current_game == None:
        return
    
    text = "Preto" if current_game.cor_rodada == 1 else "Branco"
    color = BLACK if current_game.cor_rodada == 1 else WHITE

    DrawText(text,LARGURA // 2 + 358, ALTURA // 2 -130, color, 40) # Desenhando a cor da rodada
    
    DrawText(str(current_game.num_rodadas),LARGURA // 2 + 350, ALTURA // 2, BLACK, 40) # Desenhando o numero da rodada




def DrawCapturePeca(jogo:str):
    global current_game, window

    if current_game == None:
        return
    
    if (jogo == "damas"):

        # PEÇAS CAPTURADAS BRANCAS
        image = PG.image.load(PATH_SPRITE_PECA_BRANCA).convert_alpha()

        new_size = int(image.get_width() * 1.5)

        image = PG.transform.scale(image, (new_size, new_size))

        window.blit(image, (LARGURA // 2 - 450, ALTURA // 2 - 210))

        DrawText( f"x{current_game.tabuleiro.num_brancas_capturadas}", LARGURA // 2 - 373, ALTURA // 2 - 175, BLACK, 30)


        # PEÇAS CAPTURADAS PRETAS
        image = PG.image.load(PATH_SPRITE_PECA_PRETA).convert_alpha()

        new_size = int(image.get_width() * 1.5)

        image = PG.transform.scale(image, (new_size, new_size))

        window.blit(image, (LARGURA // 2 - 450, ALTURA // 2 + 110))

        DrawText( f"x{current_game.tabuleiro.num_pretas_capturadas}", LARGURA // 2 - 373, ALTURA // 2 + 140, BLACK, 35)
    
    elif (jogo == "xadrez"):
        
        index_brancas = 0

        for p in current_game.PecasBrancas:

            if (p.capturada):
                
                x = LARGURA // 2 - 350 + (45 * index_brancas)

                y = 50

                window.blit(p.image, (x,y))
                
                index_brancas += 1

        index_pretas = 0

        for p in current_game.PecasPretas:

            if (p.capturada):
                
                x = LARGURA // 2 - 350 + (45 * index_pretas)

                y = ALTURA // 2 + 250

                window.blit(p.image, (x,y))
                
                index_pretas += 1




def DrawWinScreen():
    global current_game,window
 
    if current_game == None:
        return
    
    text = "As Pretas ganharam" if current_game.colorWinner == 1 else "As Brancas ganharam"
    
    text_render = fonte_win_text.render(text, True, BLACK)  # Atualiza o texto

    window.blit(text_render, (LARGURA/2 - 230, ALTURA/2 - 60))


def GameState():
    global running, state, window, current_game, peca_being_dragged, selected_game
    global start_button, quit_button, pause_button, resume_button, initial_menu_button, reset_button, damas_button, xadrez_button

    if (state == "initialmenu"):

        start_button.DisplayButton(window)
        quit_button.DisplayButton(window)

        if (start_button.released):
            # CreateGame(selected_game)
            state = "menuselection"
            start_button.UpdateClick()

        if (quit_button.released):
            running = False
            quit_button.UpdateClick()

    elif (state == "menuselection"):

        damas_button.DisplayButton(window)
        xadrez_button.DisplayButton(window)

        if (damas_button.released):
            selected_game = "damas"
            CreateGame(selected_game)
            state = "gaming"
            damas_button.UpdateClick()

        if (xadrez_button.released):
            selected_game = "xadrez"
            CreateGame(selected_game)
            state = "gaming"
            xadrez_button.UpdateClick()



    elif (state == "gaming"):

        if (current_game == None):
            CreateGame(selected_game)

        pause_button.DisplayButton(window)

        if (pause_button.released):
            state = "paused"
            pause_button.UpdateClick()

        current_game.tabuleiro.DesenhaTabuleiro(window,peca_being_dragged)
        
        DrawCorRodada()
        
        DrawCapturePeca(selected_game)

        mouse = PG.mouse.get_pressed()

        if mouse[0]:
            HandlePecasClick()
        elif peca_being_dragged:
            HandlePecasRelease()
    
    elif (state == "paused"):

        resume_button.DisplayButton(window)
        initial_menu_button.DisplayButton(window)
        reset_button.DisplayButton(window)
        
        if (resume_button.released):
            state = "gaming"
            resume_button.UpdateClick()

        if (initial_menu_button.released):
            state = "initialmenu"
            initial_menu_button.UpdateClick()

        if (reset_button.released):
            current_game.ResetGame()
            state = "gaming"
            reset_button.UpdateClick()

    elif (state == "winScreen"):

        if (current_game != None):
            current_game.tabuleiro.DesenhaTabuleiro(window)
            DrawCorRodada()

        DrawWinScreen()





while(running):

    window.fill(GRAY)

    GameState()

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



    