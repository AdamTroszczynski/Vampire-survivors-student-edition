import pygame
import threading
import time
from classes.texture_loader import knight, knight_hit

class Player:
  def __init__(self, position):
    self.position = position
    self.speed = 300
    self.hp = 3
    self.dmg = 10
    self.max_ammo = 1
    self.ammo = 1
    self.is_reload = False
    self.immortality = False
    self.awatar = knight

  def movement(self, dt, game):
    # Board block
    self.position.x = max(min(self.position.x, game.screen_width - 40), 40)
    self.position.y = max(min(self.position.y, game.screen_height - 40), 40)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
      self.position.y -= self.speed * dt
    if keys[pygame.K_s]:
      self.position.y += self.speed * dt
    if keys[pygame.K_a]:
      self.position.x -= self.speed * dt
    if keys[pygame.K_d]:
      self.position.x += self.speed * dt

  def check_getHit(self, enemy_array, game):
    if self.immortality == True:
        return
    for enemy in enemy_array:
        if ((self.position.x >= enemy.position.x - 40) and (self.position.x <= enemy.position.x  + 40)) and ((self.position.y >= enemy.position.y -40) and (self.position.y <= enemy.position.y +40)):
            self.hp -= 1
            if self.hp == 0:
              game.menu = True
              game.running = False
              return
            set_immortality_thread = threading.Thread(target=self.set_immortality)
            set_immortality_thread.start()
            break
        
  def set_immortality(self): 
    global knight
    self.immortality = True
    self.awatar = knight_hit
    time.sleep(3)
    self.immortality = False
    self.awatar = knight
    
  def reload(self):
    self.is_reload = True
    time.sleep(1)
    self.ammo = self.max_ammo
    self.is_reload = False
  
 
