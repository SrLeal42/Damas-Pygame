import pygame as PG
from Config import DICT_PATH_SPRITE


class Peca(PG.sprite.Sprite): # Herdando a classe Sprite do Pygame

    cor = -1 # 0 = Branca 1 = Preto
    tipo = 0 #  0 = Peça Comum / 1 = Peça Damas / 2 = Peão / 3 = Torres / 4 = Cavalos / 5 = Bispos / 6 = Rainhas / 7 = Reis   
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
    primeiro_movimento = True

    def __init__(self,cor:int,linha:int,coluna:int,x=0,y=0,tipo=0):
        self.cor = cor
        # Inicializa a classe Sprite
        super().__init__()
        self.linha = linha
        self.coluna = coluna
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.tipo = tipo
        self.SetSprite(DICT_PATH_SPRITE[tipo][cor])

    def SetSprite(self,path:str):
        # image é um atributo da classe Sprite 
        self.image = PG.image.load(path).convert_alpha()

        new_size = int(self.image.get_width() * self.escala)
        
        self.image = PG.transform.scale(self.image, (new_size, new_size))

        # rect té um atributo da classe Sprite
        self.rect = self.image.get_rect(center=(self.x, self.y))


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
        tabuleiro.tabuleiro[self.linha][self.coluna] = None
        self.SetCoord(-1,-1,True)
        self.SetTabCoord(-1,-1,True)
        if (self.cor == 0):
            tabuleiro.num_brancas_capturadas += 1
        else:
            tabuleiro.num_pretas_capturadas += 1

    
    def TurnPecaInToDama(self):
        self.tipo = 1
        self.SetSprite(DICT_PATH_SPRITE[self.tipo][self.cor])

    def TurnPecaInToRainha(self):
        self.tipo = 6
        self.SetSprite(DICT_PATH_SPRITE[self.tipo][self.cor])


