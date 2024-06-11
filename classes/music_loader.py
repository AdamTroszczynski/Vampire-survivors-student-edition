import pygame

def set_menu_music():
  pygame.mixer.music.stop()
  pygame.mixer.music.load('music/menu.mp3')
  pygame.mixer.music.play()

def set_map1_music():
  pygame.mixer.music.stop()
  pygame.mixer.music.load('music/map1.mp3')
  pygame.mixer.music.play()

def set_map1_boss_music():
  pygame.mixer.music.stop()
  pygame.mixer.music.load('music/map1_boss_fight.mp3')
  pygame.mixer.music.set_volume(0.5)
  pygame.mixer.music.play()

def set_map2_music():
  pygame.mixer.music.stop()
  pygame.mixer.music.load('music/map2.mp3')
  pygame.mixer.music.play()

def set_map2_boss_music():
  pygame.mixer.music.stop()
  pygame.mixer.music.load('music/map2_boss_fight.mp3')
  pygame.mixer.music.set_volume(0.5)
  pygame.mixer.music.play()

def set_outro_music():
  pygame.mixer.music.stop()
  pygame.mixer.music.set_volume(0.5)
  pygame.mixer.music.play()
