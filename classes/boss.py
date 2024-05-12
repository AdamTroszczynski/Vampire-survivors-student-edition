import math
import pygame
import time
import threading
import random
from classes.arrow import Arrow
from classes.enemy import Enemy

class Boss:
  def __init__(self, position, type, hp, speed):
    self.position = position
    self.type = type
    self.hp = hp
    self.speed = speed
    self.player_pos = None
    self.rush = 0
    self.turn = 1
    self.spawn_arrow = False
    self.ready = True

  # Attack that move Boss to player
  def attack(self, player, game):
    self.speed = 1300
    if self.player_pos == None:
      self.player_pos = player.position.copy()
    direction = ((self.player_pos -pygame.Vector2(30,30)) - self.position).normalize() * self.speed * game.dt
    self.position += direction
    if ((self.position.x >= self.player_pos.x - 50 and self.position.x <= self.player_pos.x + 50) and (self.position.y >= self.player_pos.y - 50 and self.position.y <= self.player_pos.y + 50)):
      self.player_pos = None
      wait_thread = threading.Thread(target=self.wait, args=([1]))
      wait_thread.start()

  # Special attack that generates additional enemeis
  def attack2(self, game, enemy_array, screen_width, screen_height):
    self.speed = 600
    direction = (pygame.Vector2(screen_width/2, screen_height/2) - self.position).normalize() * self.speed * game.dt
    self.position += direction
    if ((self.position.x >= screen_width/2 - 50 and self.position.x <= screen_width/2 + 50) and (self.position.y >= screen_height/2 - 50 and self.position.y <= screen_height/2 + 50)):
      if random.random() > 0.5:
        for i in range(4 * self.turn):
          x = random.randint(int(screen_width/2 - 300 * self.turn/3), int(screen_width/2 + 300 * self.turn/3))
          y = random.randint(int(screen_height/2 - 300 * self.turn/3), int(screen_height/2 + 300 * self.turn/3))
          enemy_array.append(Enemy(pygame.Vector2(x,y), 4))
      else:
        for i in range(4 * self.turn):
          x = random.randint(int(screen_width/2 - 300 * self.turn/3), int(screen_width/2 + 300 * self.turn/3))
          y = random.randint(int(screen_height/2 - 300 * self.turn/3), int(screen_height/2 + 300 * self.turn/3))
          enemy_array.append(Enemy(pygame.Vector2(x,y), 5))
      self.turn += 1
      wait_thread = threading.Thread(target=self.wait, args=([1]))
      wait_thread.start()

  def wait(self,time_s):
    self.ready = False
    time.sleep(time_s)
    self.rush += 1
    if self.rush > 6:
      self.rush = 0
    self.ready = True