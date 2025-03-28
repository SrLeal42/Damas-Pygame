import pygame as PG
import random

class SoundFXManager:

    def StartPlayMusic(self, volume:float):
        
        PG.mixer.music.stop()

        PG.mixer.music.load("Main/Sounds/Music/Musica_1.mp3")

        PG.mixer.music.set_volume(volume)

        PG.mixer.music.play(-1)

    def StartPlayerVictoryMusic(self, volume:float):

        PG.mixer.music.stop()

        PG.mixer.music.load("Main/Sounds/Music/Vitoria_1.mp3")

        PG.mixer.music.set_volume(volume)

        PG.mixer.music.play()

    def PlaySoundFX(self, path, volume:float):

        efeito = PG.mixer.Sound(path)

        efeito.set_volume(volume)

        efeito.play()

    
    def PlayRandomSoundFX(self, arrayPaths, volume:float):

        randPath = random.choice(arrayPaths)

        efeito = PG.mixer.Sound(randPath)

        efeito.set_volume(volume)

        efeito.play()


