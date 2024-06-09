import pygame
import threading
import time
import random

class Bullet:
    def __init__(self, position, direction, speed=1000, radius=20):
        self.position = position
        self.direction = direction
        self.speed = speed
        self.radius = radius

    def move(self, dt):
        self.position += self.direction * self.speed * dt

    def check_collision(self, player):
        if player.immortality:
            return False  
        if (player.position.x - self.radius <= self.position.x <= player.position.x + self.radius) and \
           (player.position.y - self.radius <= self.position.y <= player.position.y + self.radius):
            return True
        return False

    def render(self, screen, camera_offset):
        pygame.draw.circle(screen, (255, 0, 255), (int(self.position.x + camera_offset.x), int(self.position.y + camera_offset.y)), self.radius)


class Enemy:
    def __init__(self, position, type, game):
        self.position = position
        self.type = type
        self.game = game
        self.alive = True
        self.set_attributes()
        if self.type == 3 and game.turn == 2:
            self.shoot_thread = threading.Thread(target=self.shoot_player)
            self.shoot_thread.daemon = True
            self.shoot_thread.start()

    def set_attributes(self):
        if self.type == 1:
            self.speed = 250
            self.hp = 10
        elif self.type == 2:
            self.speed = 50
            self.hp = 60
        elif self.type == 3:
            self.speed = 100
            self.hp = 30
        elif self.type == 4:
            self.speed = 300
            self.hp = 30
        elif self.type == 5:
            self.speed = 250
            self.hp = 20

    def move_towards_player(self, player, dt):
        direction = ((player.position - pygame.Vector2(30, 30)) - self.position).normalize() * self.speed * dt
        self.position += direction

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def shoot_player(self):
        while self.game.running and self.alive and self.game.turn == 2:
            time.sleep(2)
            if not self.game.running or not self.alive:
                break
            target_position = self.game.player.position + pygame.Vector2(random.uniform(-250, 250), random.uniform(-250, 250))
            direction = (target_position - self.position).normalize()
            bullet = Bullet(self.position.copy(), direction, speed=1000, radius=20)
            with self.game.bullets_lock:
              self.game.enemy_bullets.append(bullet)
