import pygame as PG
from Classes.SoundFXManager import SoundFXManager


class Button(PG.sprite.Sprite):

    x = 0
    y = 0

    image_height = 0
    image_width = 0

    normal_img = None
    bigger_img = None

    clicked = False
    pressed = False
    released = False

    SoundManager = SoundFXManager()
    played_hover_SFX = False

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

        x_size = int(self.image.get_width() * scale)
        y_size = int(self.image.get_height() * scale)
        
        self.image = PG.transform.scale(self.image, (x_size, y_size))

        # rect té um atributo da classe Sprite
        self.rect = self.image.get_rect(center=(self.x, self.y))

        self.image_height = self.image.get_height()
        self.image_width = self.image.get_width()
        
        self.normal_img = self.image

        x_size = int(self.image_width *  1.1)
        y_size = int(self.image_height *  1.1)

        self.bigger_img = PG.transform.scale(self.image, (x_size, y_size))


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

            if (self.released):
                self.SoundManager.PlaySoundFX("Main/Sounds/SoundFX/Select_1.wav", 0.3)

    def ButtonHover(self):
        if (not self.normal_img or not self.bigger_img):
            return
        
        mouse_pos = PG.mouse.get_pos()

        colidiu = self.rect.collidepoint(mouse_pos)

        # É preciso fazer deste jeito se não o escalonamento vai degradando a sprite
        self.image = self.bigger_img if colidiu else self.normal_img

        if (colidiu and not self.played_hover_SFX):

            self.SoundManager.PlaySoundFX("Main/Sounds/SoundFX/Cancel_1.wav", 0.3)
            
            self.played_hover_SFX = True

        elif (not colidiu):

            self.played_hover_SFX = False



        self.rect = self.image.get_rect(center=(self.x, self.y))




    def DisplayButton(self, window):
        self.Draw(window)
        self.UpdateClick()
        self.ButtonHover()
            
