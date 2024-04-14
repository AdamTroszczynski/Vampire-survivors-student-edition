import pygame

def set_menu_music():
  pygame.mixer.music.stop()
  pygame.mixer.music.load('music/menu.mp3')
  pygame.mixer.music.play()

def set_map1_music():
  pygame.mixer.music.stop()
  pygame.mixer.music.load('music/map1.mp3')
  pygame.mixer.music.play()