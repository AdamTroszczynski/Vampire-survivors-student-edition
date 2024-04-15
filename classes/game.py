import pygame
import random
import math
import threading
import time
from classes.enemy import Enemy
from classes.arrow import Arrow
from classes.perk import Perk
from classes.boss import Boss
from classes.texture_loader import gif, map1, map1_dark
from classes.music_loader import set_map1_boss_music

class Game:
  def __init__(self, screen_width, screen_height, window_size): 
    self.menu = True
    self.exit = False
    self.isSpawn = False
    self.screen_width = screen_width
    self.screen_height = screen_height
    self.window_size = window_size
    self.screen = pygame.display.set_mode(window_size)
    self.camera_offset = pygame.Vector2(0, 0)
    self.clock = pygame.time.Clock()
    self.map = pygame.transform.scale(map1, (self.screen_width, self.screen_height))
    self.menu_map = pygame.transform.scale(gif, (self.screen_width / 1.5, self.screen_height /1.5))
    self.running = True
    self.isVictory = False
    self.boss = None
    self.bossIsSpawn = False
    self.dt = 0
    self.boss_fight = False
    self.enemy_array = []
    self.arrow_array = []
    self.perk_array = []

  # Move camera to player
  def update_camera_offset(self, player):
    self.camera_offset.x = min(max(self.window_size[0] / 2 - player.position.x, self.window_size[0] - self.screen_width), 0)
    self.camera_offset.y = min(max(self.window_size[1] / 2 - player.position.y, self.window_size[1] - self.screen_height), 0)


  def spawn_enemy(self, player):
    monsters = [1,3]
    chanses = [0.4, 0.2]
    while self.running and not self.boss_fight:
        if len(self.enemy_array) > 20:
            time.sleep(3)
            continue
        x = random.randint(30, self.screen_width - 30)
        y = random.randint(30, self.screen_height - 30)
        if player.position.distance_to(pygame.Vector2(x, y)) >= 700:
            enemy_type = random.choices(monsters, weights = chanses)[0]
            self.enemy_array.append(Enemy(pygame.Vector2(x, y), enemy_type))
        time.sleep(0.5)

  def spawn_perk(self):
     perks = [1,2,3]
     chanses = [0.4, 0.4, 0.2]
     while self.running:
        if len(self.perk_array) > 5:
           time.sleep(5)
           continue
        x = random.randint(40, self.screen_width - 40)
        y = random.randint(40, self.screen_height - 40)
        perk_type = random.choices(perks, weights = chanses)[0]
        self.perk_array.append(Perk(pygame.Vector2(x,y),perk_type))
        time.sleep(5)


  def move_enemies(self, player):
    for enemy in self.enemy_array:
        direction = ((player.position -pygame.Vector2(30,30)) - enemy.position).normalize() * enemy.speed * self.dt
        enemy.position += direction

  def spawn_arrow(self, player):
    if player.is_reload == True:
        return
    cursor = pygame.Vector2(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]).copy()
    starting_pos = (player.position.copy() + self.camera_offset) 
    direction = (cursor - starting_pos).normalize() * 200 * self.dt
    arrow = Arrow(starting_pos, cursor, direction)
    arrow.angle = math.atan2(direction.y, direction.x) 
    self.arrow_array.append(arrow)

  def move_arrow(self):
    for arrow in self.arrow_array:
        arrow.position += arrow.direction * 200 * self.dt
        if arrow.position.x > 2000 or arrow.position.y > 2000 or arrow.position.x < -2000 or arrow.position.y < -2000:
            self.arrow_array.remove(arrow)
        
  def check_hit(self, player):
    for arrow in self.arrow_array:
        if self.bossIsSpawn:
           if ((arrow.position.x >= self.boss.position.x + self.camera_offset.x - 20) and (arrow.position.x <= self.boss.position.x+ self.camera_offset.x + 180)) and ((arrow.position.y >= self.boss.position.y+ self.camera_offset.y -20) and (arrow.position.y <= self.boss.position.y+ self.camera_offset.y +180)):
              self.arrow_array.remove(arrow)
              self.boss.hp -= player.dmg
              if self.boss.hp <= 0:
                 self.running = False 
              continue
                 
        for enemy in self.enemy_array:
            if ((arrow.position.x >= enemy.position.x + self.camera_offset.x - 40) and (arrow.position.x <= enemy.position.x+ self.camera_offset.x + 40)) and ((arrow.position.y >= enemy.position.y+ self.camera_offset.y -40) and (arrow.position.y <= enemy.position.y+ self.camera_offset.y +40)):
                self.arrow_array.remove(arrow)
                enemy.hp -= player.dmg
                if enemy.hp <= 0:
                  self.enemy_array.remove(enemy)
                  player.pd += 10
                  if player.pd >= 400:
                    player.pd = -10000
                    self.start_boss_fight()
                    return
                break
            
  def start_boss_fight(self):
     self.enemy_array = []
     self.boss_fight = True
     self.map = pygame.transform.scale(map1_dark, (self.screen_width, self.screen_height))
     set_map1_boss_music()
     spawn_boss_thread = threading.Thread(target=self.spawn_boss)
     spawn_boss_thread.start()

  def spawn_boss(self):
     time.sleep(13)
     self.boss = Boss(pygame.Vector2(self.screen_width/2 , self.screen_height/2), 'boss1', 600, 600)
     self.bossIsSpawn = True

