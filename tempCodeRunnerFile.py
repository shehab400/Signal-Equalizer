import pygame
import time

pygame.mixer.init()

pygame.mixer.music.load("ComposedSound.mp3")
pygame.mixer.music.play()

time.sleep(5)

pygame.mixer.music.unload()
pygame.mixer.music.load("ComposedSound.mp3")
pygame.mixer.music.play()

time.sleep(5)