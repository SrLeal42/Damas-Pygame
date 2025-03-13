import pygame as PG

LARGURA = 1000
ALTURA = 800

PG.init()

running = True

window = PG.display.set_mode((LARGURA,ALTURA))

PG.display.set_caption("Damas")

while(running):
    for evento in PG.event.get():
            if evento.type == PG.QUIT:
                running = False

    