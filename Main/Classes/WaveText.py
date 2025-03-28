import pygame as PG
import math
from Config import FONTE_PRIN

class WaveText:

    text = ""

    color = (0,0,0)

    size = 1

    start_x = 0
    start_y = 0

    start_angle = 0

    x = 0
    y = 0

    angle = 0

    margin = 0

    margin_angle = 0

    wave_angle = 0

    text_angle = 0

    ultimo_tempo = PG.time.get_ticks()
    
    def __init__(self, text:str, x:int, y:int, color, size:int, margin:int, margin_angle:int):
        
        self.text = text

        self.color = color
        
        self.size = size

        self.start_x = x
        self.start_y = y

        self.x = x
        self.y = y

        self.margin = margin

        self.margin_angle = margin_angle
        

    def Wave(self, window):

        tempo_atual = PG.time.get_ticks()

        if tempo_atual - self.ultimo_tempo >= 10:
            
            self.ultimo_tempo = tempo_atual


            # ALTERANDO O ANGULO DO TEXTO
            if (self.text_angle >= 360):
                self.text_angle = 0
            else:
                self.text_angle += 1

            seno_graus = math.sin(math.radians(self.text_angle))

            seno_graus = round(seno_graus, 2)

            new_angle = self.start_angle + (self.margin_angle * seno_graus)

            self.angle = new_angle


            # ALTERANDO A POSIÇÃO DO TEXTO
            if (self.wave_angle >= 360):
                self.wave_angle = 0
            else:
                self.wave_angle += 1

            seno_graus = math.sin(math.radians(self.wave_angle))

            seno_graus = round(seno_graus, 2)
            # print(seno_graus)

            new_y = self.start_y + (self.margin * seno_graus)

            self.y = new_y
        
        self.DrawText(window)


        

    def DrawText(self, window):

        fonte = PG.font.Font(FONTE_PRIN, self.size)

        text_render = fonte.render(self.text, False, self.color)

        text_size = fonte.size(self.text)

        text_render = PG.transform.rotate(text_render, self.angle)

        window.blit(text_render, (self.x - (text_size[0] // 2), self.y - (text_size[1] // 2)))
