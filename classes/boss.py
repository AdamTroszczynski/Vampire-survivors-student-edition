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

  # Attack that moves Boss to player
    def attack(self, player, game):
        self.speed = 1300
        if self.player_pos is None:
            self.player_pos = player.position.copy()
        direction = (self.player_pos - pygame.Vector2(30, 30) - self.position).normalize() * self.speed * game.dt
        self.position += direction
        if self._is_near_player():
            self.player_pos = None
            threading.Thread(target=self.wait, args=(1,)).start()

  # Special attack that generates additional enemies
    def attack2(self, game, enemy_array, screen_width, screen_height):
        self.speed = 600
        center_screen = pygame.Vector2(screen_width / 2, screen_height / 2)
        direction = (center_screen - self.position).normalize() * self.speed * game.dt
        self.position += direction
        if self._is_at_center(center_screen):
            self._spawn_enemies(enemy_array, screen_width, screen_height)
            self.turn += 1
            threading.Thread(target=self.wait, args=(1,)).start()

    def _is_near_player(self):
        return (self.player_pos.x - 50 <= self.position.x <= self.player_pos.x + 50 and
                self.player_pos.y - 50 <= self.position.y <= self.player_pos.y + 50)

    def _is_at_center(self, center):
        return (center.x - 50 <= self.position.x <= center.x + 50 and
                center.y - 50 <= self.position.y <= center.y + 50)

    def _spawn_enemies(self, enemy_array, screen_width, screen_height):
        enemy_type = 4 if random.random() > 0.5 else 5
        for _ in range(4 * self.turn):
            x = random.randint(int(screen_width / 2 - 300 * self.turn / 3), int(screen_width / 2 + 300 * self.turn / 3))
            y = random.randint(int(screen_height / 2 - 300 * self.turn / 3), int(screen_height / 2 + 300 * self.turn / 3))
            enemy_array.append(Enemy(pygame.Vector2(x, y), enemy_type))

    def wait(self, time_s):
        self.ready = False
        time.sleep(time_s)
        self.rush = (self.rush + 1) % 7  
        self.ready = True
