import pygame as PG



class Button(PG.sprite.Sprite):

    x = 0
    y = 0

    image_height = 0
    image_width = 0

    clicked = False
    pressed = False
    released = False

    def __init__(self, x:int, y:int, pathImage:str, scale:float):
        super().__init__()

        self.x = x
        self.y = y
        self.SetSprite(pathImage,scale)
        # image = PG.image.load(pathImage).convert_alpha()
        # self.image = PG.transform.scale(image, ( int(image.get_width() * scale),int(image.get_height() * scale) ))
        # self.rect = self.image.get_rect(center=(self.x, self.y))

    def SetSprite(self,path:str, scale:float):
        # image é um atributo da classe Sprite 
        self.image = PG.image.load(path).convert_alpha()

        new_size = int(self.image.get_width() * scale)
        
        self.image = PG.transform.scale(self.image, (new_size, new_size))

        # rect té um atributo da classe Sprite
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.image_height = self.image.get_height()
        self.image_width = self.image.get_width()

    def Draw(self, window):
        grupo_sprite = PG.sprite.Group(self)
        grupo_sprite.draw(window)
        # window.blit(self.image, (self.x,self.y))

    def UpdateClick(self):
        mouse_pos = PG.mouse.get_pos()

        if (self.rect.collidepoint(mouse_pos)):

            self.released = PG.mouse.get_pressed()[0] == 0 and self.pressed

            self.clicked = PG.mouse.get_pressed()[0] == 1 and self.pressed == False

            self.pressed = PG.mouse.get_pressed()[0] == 1

    def ButtonHover(self):
        mouse_pos = PG.mouse.get_pos()

        scale = 1.1 if self.rect.collidepoint(mouse_pos) else 1

        new_size = int(self.image_height *  scale)
    
        self.image = PG.transform.scale(self.image, (new_size, new_size))

        # rect té um atributo da classe Sprite
        self.rect = self.image.get_rect(center=(self.x, self.y))




    def DisplayButton(self, window):
        self.Draw(window)
        self.UpdateClick()
        self.ButtonHover()
            
