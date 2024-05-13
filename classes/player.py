import pygame
import threading
import time
from classes.texture_loader import knight, knight_hit

class Player:
  def __init__(self, position):
    self.position = position
    self.category = 'warrior'
    self.speed = 300
    self.max_hp = 5
    self.hp = 5
    self.dmg = 10
    self.max_ammo = 2
    self.ammo = 2
    self.reload_time = 1
    self.perks = []
    self.pd = 0
    self.is_reload = False
    self.immortality = False
    self.lock_hit = threading.Lock()

  def set_classes(self, name):
    if name == 'warrior':
      self.category = 'warrior'
      self.speed = 300
      self.max_hp = 5
      self.hp = 5
      self.dmg = 10
      self.max_ammo = 2
      self.ammo = 2
      self.reload_time = 1
    elif name == 'wizard':
      self.category = 'wizard'
      self.speed = 400
      self.hp = 3
      self.max_hp = 3
      self.dmg = 20
      self.max_ammo = 3
      self.ammo = 3
      self.reload_time = 1.5
    elif name == 'king':
      self.category = 'king'
      self.speed = 400
      self.hp = 5
      self.max_hp = 5
      self.dmg = 600
      self.max_ammo = 6
      self.ammo = 6
      self.reload_time = 1

  # Set immortality if player gets hit
  def check_getHit(self, enemy_array, game):
    with self.lock_hit:
        if self.immortality:
            return
        if game.bossIsSpawn:
            boss = game.boss
            if (boss.position.x - 20 <= self.position.x <= boss.position.x + 180) \
                    and (boss.position.y - 20 <= self.position.y <= boss.position.y + 180):
                self.handle_hit(game)
        else:
            for enemy in enemy_array:
                if (enemy.position.x - 40 <= self.position.x <= enemy.position.x + 40) \
                        and (enemy.position.y - 40 <= self.position.y <= enemy.position.y + 40):
                    self.handle_hit(game)
                    break

  def handle_hit(self, game):
      self.hp -= 1
      if self.hp == 0:
          game.menu = True
          game.running = False
          self.hp = self.max_hp
          self.ammo = self.max_ammo
          return
      threading.Thread(target=self.set_immortality).start()

  def set_immortality(self): 
      self.immortality = True
      time.sleep(1)
      self.immortality = False


  # Add a bonus in stats based on perk
  def check_perk(self, perk_array):
    for perk in perk_array:
      if ((self.position.x >= perk.position.x - 30) and (self.position.x <= perk.position.x  + 70)) and ((self.position.y >= perk.position.y -40) and (self.position.y <= perk.position.y +40)):
        if perk.type == 1:
          if self.hp == self.max_hp:
            return
          else:
            self.hp += 1
            perk_array.remove(perk)
        elif perk.type == 2:
          set_speed_boost_thread = threading.Thread(target=self.speed_boost, args=([perk]))
          set_speed_boost_thread.start()
          perk_array.remove(perk)
        elif perk.type == 3:
          set_reload_boost_thread = threading.Thread(target=self.reload_boost, args=([perk]))
          set_reload_boost_thread.start()
          perk_array.remove(perk)


  def reload_boost(self, perk):
    self.perks.append(perk)
    self.reload_time = self.reload_time / 2
    time.sleep(3)
    self.reload_time = self.reload_time * 2
    self.perks.remove(perk)

  def speed_boost(self, perk):
    self.perks.append(perk)
    self.speed = self.speed * 1.3
    time.sleep(3)
    self.speed = self.speed / 1.3
    self.perks.remove(perk)
        
  def set_immortality(self): 
    self.immortality = True
    time.sleep(1)
    self.immortality = False
    
  def reload(self):
    self.is_reload = True
    time.sleep(self.reload_time)
    self.ammo = self.max_ammo
    self.is_reload = False
  
 
