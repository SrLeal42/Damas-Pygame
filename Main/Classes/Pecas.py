import pygame as PG
from Config import PATH_SPRITE_BRANCA,PATH_SPRITE_PRETA


class Peca(PG.sprite.Sprite): # Herdando a classe Sprite do Pygame

    cor = -1 # 0 = Branca 1 = Preto
    tipo = 0
    linha = -1
    coluna = -1
    start_linha = -1
    start_coluna = -1
    x = 0
    y = 0
    start_x = 0
    start_y = 0
    # tamanho = 20
    escala = 1.5
    capturada = False
    sendo_arrastada = False

    def __init__(self,cor:int,linha:int,coluna:int,x=0,y=0,tipo=0):
        self.cor = cor
        # Inicializa a classe Sprite
        super().__init__()
        # image é um atributo da classe Sprite 
        self.image = PG.image.load(PATH_SPRITE_PRETA).convert_alpha() if cor == 1 else PG.image.load(PATH_SPRITE_BRANCA).convert_alpha()
        
        new_size = int(self.image.get_width() * self.escala)
        
        self.image = PG.transform.scale(self.image, (new_size, new_size))

        # rect té um atributo da classe Sprite
        self.rect = self.image.get_rect(center=(x, y))

        self.linha = linha
        self.coluna = coluna
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.tipo = tipo


    def SetCoord(self,x:float, y:float,setStartCoord=False):
        self.x = x
        self.y = y

        self.rect = self.image.get_rect(center=(x, y))

        if setStartCoord:
            self.start_x = x
            self.start_y = y

    def SetTabCoord(self,linha:int, coluna:int,setStartCoord=False):
        self.linha = linha
        self.coluna = coluna
        
        if setStartCoord:
            self.start_coluna = coluna
            self.start_linha = linha


    def CapturarPeca(self, tabuleiro):
        self.capturada = True
        tabuleiro[self.linha][self.coluna] = None
        self.SetCoord(-1,-1,True)
        self.SetTabCoord(-1,-1,True)

    
    def TurnPecaInToDama(self):
        self.tipo = 1

