

class Peca:

    cor = -1
    tipo = 0
    linha = -1
    coluna = -1
    start_linha = -1
    start_coluna = -1
    x = 0
    y = 0
    start_x = 0
    start_y = 0
    tamanho = 15
    comida = False

    def __init__(self,cor:int,linha:int,coluna:int,x=0,y=0,tipo=0):
        self.cor = cor
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

        if setStartCoord:
            self.start_x = x
            self.start_y = y

    def SetTabCoord(self,linha:int, coluna:int,setStartCoord=False):
        self.linha = linha
        self.coluna = coluna
        
        if setStartCoord:
            self.start_coluna = coluna
            self.start_linha = linha


    def ComerPeca(self, tabuleiro):
        self.comida = True
        tabuleiro[self.linha][self.coluna] = None
        self.linha = -1
        self.coluna = -1
        self.start_coluna = 0
        self.start_linha = 0

