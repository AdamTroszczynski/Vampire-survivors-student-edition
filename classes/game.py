import pygame
import random
import math
import time
from classes.enemy import Enemy
from classes.arrow import Arrow
from classes.texture_loader import gif, map1

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
    self.dt = 0
    self.enemy_array = []
    self.arrow_array = []

  def update_camera_offset(self, player):
    self.camera_offset.x = min(max(self.window_size[0] / 2 - player.position.x, self.window_size[0] - self.screen_width), 0)
    self.camera_offset.y = min(max(self.window_size[1] / 2 - player.position.y, self.window_size[1] - self.screen_height), 0)

  # Function to spawn enemies
  def spawn_enemy(self, player):
    # Chance to spawn
    monsters = [1,3]
    chanses = [0.4, 0.2]
    while self.running:
        if len(self.enemy_array) > 50:
            continue
        x = random.randint(30, self.screen_width - 30)
        y = random.randint(30, self.screen_height - 30)
        if player.position.distance_to(pygame.Vector2(x, y)) >= 700:
            enemy_type = random.choices(monsters, weights = chanses)[0]
            self.enemy_array.append(Enemy(pygame.Vector2(x, y), enemy_type))
        time.sleep(0.5)  # Spawns every 0.5 second

  # Function to move enemies towards the player
  def move_enemies(self, player):
    for enemy in self.enemy_array:
        if enemy.hp <= 0:
            self.enemy_array.remove(enemy)
            return
        direction = ((player.position -pygame.Vector2(30,30)) - enemy.position).normalize() * enemy.speed * self.dt
        enemy.position += direction

  # Function to spawn arrow
  def spawn_arrow(self, player):
    if player.is_reload == True:
        return
    cursor = pygame.Vector2(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]).copy()
    starting_pos = (player.position.copy() + self.camera_offset) # Uwzględnienie przesunięcia kamery
    direction = (cursor - starting_pos).normalize() * 200 * self.dt
    arrow = Arrow(starting_pos, cursor, direction)
    arrow.angle = math.atan2(direction.y, direction.x)  # Obliczenie kąta dla obrotu
    self.arrow_array.append(arrow)

  def move_arrow(self):
    for arrow in self.arrow_array:
        arrow.position += arrow.direction * 200 * self.dt  # Ruch strzały
        if arrow.position.x > 2000 or arrow.position.y > 2000 or arrow.position.x < -2000 or arrow.position.y < -2000:
            self.arrow_array.remove(arrow)
        
  def check_hit(self, player):
    for arrow in self.arrow_array:
        for enemy in self.enemy_array:
            if ((arrow.position.x >= enemy.position.x + self.camera_offset.x - 40) and (arrow.position.x <= enemy.position.x+ self.camera_offset.x + 40)) and ((arrow.position.y >= enemy.position.y+ self.camera_offset.y -40) and (arrow.position.y <= enemy.position.y+ self.camera_offset.y +40)):
                self.arrow_array.remove(arrow)
                enemy.hp -= player.dmg
                break