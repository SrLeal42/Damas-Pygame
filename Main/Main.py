import pygame as PG
from Config import LARGURA, ALTURA,GRAY,BLACK,BLACK50,WHITE,WHITE50,FONTE_PRIN, PATH_SPRITE_PECA_BRANCA, PATH_SPRITE_PECA_PRETA, PATH_SPRITE_DAMAS_BRANCA, PATH_TRANSICAO, DEPTH
from Classes.Pecas import Peca
from Classes.Tabuleiro import Tabuleiro
from Classes.Game import Game
from Classes.Button import Button
from Classes.WaveText import WaveText
from Classes.SoundFXManager import SoundFXManager
from Classes.minimax.algoritmo import minimax
from resource_path import resource_path

PG.init()
PG.mixer.init()

SoundManager = SoundFXManager()
volume_music = 0.3

running = True

window = PG.display.set_mode((LARGURA,ALTURA))
PG.display.set_caption("Damas")
PG.display.set_icon(PG.image.load(resource_path(PATH_SPRITE_DAMAS_BRANCA)))


state = "initialmenu"

damas_text = WaveText("DAMAS", LARGURA//2, 150, WHITE, 75, 20, 2)
paused_text = WaveText("PAUSADO", LARGURA//2, 100, WHITE, 50, 20, 2)
# select_text = WaveText("SELECIONE:", LARGURA//2, 100, WHITE, 50, 20, 2)
select_mode_text = WaveText("MODO DE JOGO:", LARGURA//2, 100, WHITE, 50, 20, 2)
rules_text = WaveText("Regras:", LARGURA//2, 100, WHITE, 50, 10, 2)

start_button = Button(LARGURA//2, ALTURA//2 -60, "Main/Sprites/Buttons/start-button.png", 3)
quit_button = Button(LARGURA//2, ALTURA//2 + 60, "Main/Sprites/Buttons/quit-button.png", 3)

# damas_button = Button(LARGURA//2 - 100, ALTURA//2 , "Main/Sprites/Damas/damas-branco.png", 4)
# xadrez_button = Button(LARGURA//2 + 100, ALTURA//2 , "Main/Sprites/Xadrez/rei-branco.png", 7)

PVB_button = Button(LARGURA//2 , ALTURA//2 - 80, "Main/Sprites/Buttons/pvb-button.png", 4)
PVP_button = Button(LARGURA//2 , ALTURA//2 + 80, "Main/Sprites/Buttons/pvp-button.png", 4)

pause_button = Button(40,40,"Main/Sprites/Buttons/pause-button.png", 2)
rules_button = Button(LARGURA-40,40,"Main/Sprites/Buttons/rules-button.png", 2)

resume_button = Button(LARGURA//2, ALTURA//2 -120, "Main/Sprites/Buttons/resume-button.png", 3)
initial_menu_button = Button(LARGURA//2, ALTURA//2 , "Main/Sprites/Buttons/menu-button.png", 3)
reset_button = Button(LARGURA//2, ALTURA//2 + 120, "Main/Sprites/Buttons/reset-button.png", 3)

win_initial_menu_button = Button(LARGURA//2 - 115, ALTURA//2 + 180, "Main/Sprites/Buttons/menu-button.png", 3)
win_reset_button = Button(LARGURA//2 + 115, ALTURA//2 + 180, "Main/Sprites/Buttons/reset-button.png", 3)


selected_game = ""

game_mode = ""

current_game = None

peca_being_dragged = None
last_peca_moved = None
peca_mandatory_move = []

fonte_principal = PG.font.Font(resource_path(FONTE_PRIN), 40)

def Lerp(a, b, t):
    return a + (b - a) * t


def CreateGame(jogo:str):
    global current_game, peca_being_dragged, last_peca_moved, peca_mandatory_move

    if (current_game != None):
        
        current_game.ResetGame(jogo)
        
        peca_being_dragged = None
        
        last_peca_moved = None
        
        peca_mandatory_move = []

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
                
                if (len(peca_mandatory_move) != 0):
                    if (p not in peca_mandatory_move):
                        break

                peca_being_dragged = p
                p.SetCoord(mouse_pos[0],mouse_pos[1])
                p.sendo_arrastada = True
                break





def HandlePecasRelease():
    global peca_being_dragged, current_game, last_peca_moved, state, peca_mandatory_move, SoundManager

    if peca_being_dragged == None:
        return
    
    response = current_game.tabuleiro.TryChangePecaPlace(peca_being_dragged,current_game)
    last_peca_moved = peca_being_dragged

    peca_being_dragged.sendo_arrastada = False
    peca_being_dragged = None

    if (not response["canMove"]):
        return

    SoundManager.PlayRandomSoundFX([resource_path("Main/Sounds/SoundFX/pecaSFX_1.mp3"), resource_path("Main/Sounds/SoundFX/pecaSFX_2.mp3"), resource_path("Main/Sounds/SoundFX/pecaSFX_3.mp3")], 0.5)

    if (not response["turnThisRound"] and (response["pecaCapturada"] or current_game.sequencia_captura)):
        canCapture = current_game.tabuleiro.VerifyPecaCanCapture(last_peca_moved)
        
        current_game.sequencia_captura = canCapture
        # print(canCapture)
    elif (response["turnThisRound"]):
        # Se ele estava em uma sequencia de captura e se tornou dama então sai da sequencia de captura
        current_game.sequencia_captura = False


    winnigResponse = current_game.WinningUpdate()

    if (winnigResponse["gameEnd"]):
        state = "winScreen"
        SoundManager.StartPlayerVictoryMusic(0.4)
        # print(winnigResponse)

    current_game.EndTurn()

    if (current_game != None and current_game.jogo == "damas"):
        peca_mandatory_move = current_game.SomePecaCanCapture()



def HandleIAMove(peca:Peca, move):
    global current_game, state, peca_mandatory_move, SoundManager, last_peca_moved

    response = current_game.tabuleiro.TryChangePecaPlace(peca, current_game, move[0], move[1])

    if (not response["canMove"]):
        return

    SoundManager.PlayRandomSoundFX([resource_path("Main/Sounds/SoundFX/pecaSFX_1.mp3"), resource_path("Main/Sounds/SoundFX/pecaSFX_2.mp3"), resource_path("Main/Sounds/SoundFX/pecaSFX_3.mp3")], 0.5)

    winnigResponse = current_game.WinningUpdate()

    if (winnigResponse["gameEnd"]):
        state = "winScreen"
        SoundManager.StartPlayerVictoryMusic(0.4)

    current_game.EndTurn()
    
    peca_mandatory_move = current_game.SomePecaCanCapture()

    return 



def DrawText(text:str, x:int, y:int, color, size:int):
    global window

    fonte = PG.font.Font(resource_path(FONTE_PRIN), size)

    text_render = fonte.render(text, False, color)

    text_size = fonte.size(text)

    window.blit(text_render, (x - (text_size[0] // 2), y - (text_size[1] // 2)))


def DrawCorRodada():
    global current_game
    global window

    if current_game == None:
        return
    
    painel = PG.image.load(resource_path("Main/Sprites/painel.png")).convert_alpha()

    x_size = int(painel.get_width() * 8)
    y_size = int(painel.get_height() * 8)

    painel = PG.transform.scale(painel, (x_size, y_size))

    window.blit(painel, (LARGURA // 2 + 230, ALTURA // 2 - 285))

    text = "Preto" if current_game.cor_rodada == 1 else "Branco"
    # color = BLACK if current_game.cor_rodada == 1 else WHITE

    DrawText(text,LARGURA // 2 + 358, ALTURA // 2 -130, WHITE, 35) # Desenhando a cor da rodada
    
    DrawText(str(current_game.num_rodadas),LARGURA // 2 + 350, ALTURA // 2, WHITE, 40) # Desenhando o numero da rodada




def DrawCapturePeca(jogo:str):
    global current_game, window

    if current_game == None:
        return
    
    if (jogo == "damas"):

        # PEÇAS CAPTURADAS BRANCAS
        image = PG.image.load(resource_path(PATH_SPRITE_PECA_BRANCA)).convert_alpha()

        new_size = int(image.get_width() * 1.5)

        image = PG.transform.scale(image, (new_size, new_size))

        window.blit(image, (LARGURA // 2 - 450, ALTURA // 2 - 210))

        DrawText( f"x{current_game.tabuleiro.num_brancas_capturadas}", LARGURA // 2 - 373, ALTURA // 2 - 175, BLACK, 30)


        # PEÇAS CAPTURADAS PRETAS
        image = PG.image.load(resource_path(PATH_SPRITE_PECA_PRETA)).convert_alpha()

        new_size = int(image.get_width() * 1.5)

        image = PG.transform.scale(image, (new_size, new_size))

        window.blit(image, (LARGURA // 2 - 450, ALTURA // 2 + 110))

        DrawText( f"x{current_game.tabuleiro.num_pretas_capturadas}", LARGURA // 2 - 373, ALTURA // 2 + 140, BLACK, 30)
    
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
    
    # Retangulo transparente preto de fundo
    rect_surf = PG.Surface((LARGURA, ALTURA),PG.SRCALPHA)
    rect_surf.fill(BLACK50)
    
    window.blit(rect_surf,(0,0))

    # Painel com as informações e botões
    painel = PG.image.load(resource_path("Main/Sprites/painel_64.png")).convert_alpha()

    x_size = int(painel.get_width() * 9)
    y_size = int(painel.get_height() * 9)

    painel = PG.transform.scale(painel, (x_size, y_size))

    window.blit(painel, (LARGURA // 2 - (painel.get_width() // 2), ALTURA // 2 - (painel.get_height() // 2 )))

    DrawText("COR VENCEDORA", LARGURA//2,ALTURA//2 - 200, WHITE, 30)

    text = "PRETA" if current_game.colorWinner == 1 else "BRANCA"
    
    DrawText(text, LARGURA//2,ALTURA//2 - 115, WHITE, 55)

    DrawText("RODADAS", LARGURA//2,ALTURA//2 - 20, WHITE, 30)

    DrawText(str(current_game.num_rodadas), LARGURA//2,ALTURA//2 + 50, WHITE, 55)



def Transition(next_state:str):
    global window, state
    
    image = PG.image.load(resource_path(PATH_TRANSICAO)).convert_alpha()

    timer = 0
    duration = 1

    margin_error = 0.05

    while(timer < duration):
        t = timer / duration

        x = Lerp(image.get_width()-200, -image.get_width(), t)
        
        window.fill(GRAY)

        if (t <= 0.5 + margin_error and t >= 0.5 - margin_error):
            state = next_state

        GameState()

        window.blit(image, (x, 0))
        
        PG.display.update()

        timer += 0.01

        PG.time.delay(10)



def GameState():
    global running, state, window, current_game, peca_being_dragged, selected_game, game_mode
    global start_button, quit_button, pause_button, rules_button, resume_button, initial_menu_button, reset_button, damas_button, xadrez_button, PVB_button, PVP_button
    global damas_text, rules_text

    if (state == "initialmenu"):
        
        damas_text.Wave(window)

        start_button.DisplayButton(window)
        quit_button.DisplayButton(window)

        if (start_button.released):
            selected_game = "damas"
            CreateGame(selected_game)
            Transition("menumodeselection")
            # state = "menuselection"
            start_button.UpdateClick()
            

        if (quit_button.released):
            running = False
            quit_button.UpdateClick()
            

    # elif (state == "menuselection"):

    #     select_text.Wave(window)

    #     damas_button.DisplayButton(window)
    #     xadrez_button.DisplayButton(window)

    #     if (damas_button.released):
    #         selected_game = "damas"
    #         CreateGame(selected_game)
    #         Transition("menumodeselection")
    #         # state = "gaming"
    #         damas_button.UpdateClick()

    #     if (xadrez_button.released):
    #         selected_game = "xadrez"
    #         game_mode = "PVP"
    #         CreateGame(selected_game)
    #         Transition("gaming")
    #         # state = "gaming"
    #         xadrez_button.UpdateClick()

    elif (state == "menumodeselection"):

        select_mode_text.Wave(window)

        PVB_button.DisplayButton(window)
        PVP_button.DisplayButton(window)

        if (PVB_button.released):
            game_mode = "PVB"
            Transition("gaming")
            PVB_button.UpdateClick()

        if (PVP_button.released):
            game_mode = "PVP"
            Transition("gaming")
            PVP_button.UpdateClick()

    elif (state == "gaming"):

        if (current_game == None):
            CreateGame(selected_game)

        pause_button.DisplayButton(window)
        
        if (pause_button.released):
            state = "paused"
            pause_button.UpdateClick()

        if (current_game.jogo == "damas"):
            rules_button.DisplayButton(window)

            if (rules_button.released):
                state = "rulesScreen"
                rules_button.UpdateClick()

        current_game.tabuleiro.DesenhaTabuleiro(window,peca_being_dragged,peca_mandatory_move)
        
        DrawCorRodada()
        
        DrawCapturePeca(selected_game)

        mouse = PG.mouse.get_pressed()

        if (game_mode == "PVB"):
            if (current_game.cor_rodada == 1):
                value, move, cordPeca = minimax(current_game.tabuleiro, DEPTH, True, current_game, False)
                # print(value, move, cordPeca)
                peca = current_game.tabuleiro.tabuleiro[cordPeca[0]][cordPeca[1]]
                HandleIAMove(peca, move)

        if mouse[0]:
            HandlePecasClick()
        elif peca_being_dragged:
            HandlePecasRelease()

    elif (state == "rulesScreen"):
        rules = PG.image.load(resource_path("Main/Sprites/regras.png")).convert_alpha()

        window.blit(rules, (0, 0))

        rules_button.DisplayButton(window)

        rules_text.Wave(window)

        if (rules_button.released):
            state = "gaming"
            rules_button.UpdateClick()

    
    elif (state == "paused"):
        
        paused_text.Wave(window)

        resume_button.DisplayButton(window)
        initial_menu_button.DisplayButton(window)
        reset_button.DisplayButton(window)
        
        if (resume_button.released):
            state = "gaming"
            resume_button.UpdateClick()

        if (initial_menu_button.released):
            Transition("initialmenu")
            # state = "initialmenu"
            initial_menu_button.UpdateClick()

        if (reset_button.released):
            CreateGame(selected_game)
            Transition("gaming")
            # state = "gaming"
            reset_button.UpdateClick()

    elif (state == "winScreen"):

        if (current_game != None):
            current_game.tabuleiro.DesenhaTabuleiro(window)
            DrawCorRodada()

        pause_button.Draw(window)
        rules_button.Draw(window)

        DrawWinScreen()

        win_initial_menu_button.DisplayButton(window)
        win_reset_button.DisplayButton(window)

        if (win_initial_menu_button.released):
            Transition("initialmenu")
            initial_menu_button.UpdateClick()
            SoundManager.StartPlayMusic(volume_music)

        if (win_reset_button.released):
            CreateGame(selected_game)
            Transition("gaming")
            reset_button.UpdateClick()
            SoundManager.StartPlayMusic(volume_music)


SoundManager.StartPlayMusic(volume_music)

while(running):

    window.fill(GRAY)

    GameState()

    for evento in PG.event.get():
        if evento.type == PG.QUIT:
            running = False



            # for i in range(current_game.tabuleiro.tamanho):
            #     for j in range(current_game.tabuleiro.tamanho):
            #         if (current_game.tabuleiro.tabuleiro[i][j] != None):
            #             print(current_game.tabuleiro.tabuleiro[i][j].cor)
            #         else:
            #             print(None)

    PG.display.flip()



    