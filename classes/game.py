import pygame
import random
import math
import threading
import time
from classes.enemy import Enemy, Bullet
from classes.arrow import Arrow
from classes.perk import Perk
from classes.boss import Boss
from classes.texture_loader import gif, map1, map1_dark, map2
from classes.music_loader import set_map1_boss_music, set_map2_boss_music

class Game:
    def __init__(self, screen_width, screen_height, window_size, map):
        self.menu = True
        self.exit = False
        self.isSpawn = False
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.window_size = window_size
        self.screen = pygame.display.set_mode(window_size)
        self.camera_offset = pygame.Vector2(0, 0)
        self.clock = pygame.time.Clock()
        self.map = self._load_map(map)
        self.menu_map = pygame.transform.scale(gif, (self.screen_width / 1.5, self.screen_height / 1.5))
        self.running = True
        self.isVictory = False
        self.boss = None
        self.bossIsSpawn = False
        self.dt = 0
        self.boss_fight = False
        self.enemy_array = []
        self.arrow_array = []
        self.perk_array = []
        self.finish = True
        self.enemy_bullets = []
        self.player = None
        self.bullets_lock = threading.Lock()

    def _load_map(self, map):
        if map == 1:
            self.turn = 1
            return pygame.transform.scale(map1, (self.screen_width, self.screen_height))
        else:
            self.turn = 2
            return pygame.transform.scale(map2, (self.screen_width, self.screen_height))

    def update_camera_offset(self, player):
        self.camera_offset.x = min(max(self.window_size[0] / 2 - player.position.x, self.window_size[0] - self.screen_width), 0)
        self.camera_offset.y = min(max(self.window_size[1] / 2 - player.position.y, self.window_size[1] - self.screen_height), 0)

    def restart(self):
        self.map = pygame.transform.scale(map1, (self.screen_width, self.screen_height))
        self.turn = 1

    def spawn_enemy(self, player):
        self.player = player
        monsters = [1, 3]
        chances = [0.4, 0.2]
        while self.running and not self.boss_fight:
            if len(self.enemy_array) > 50:
                time.sleep(3)
                continue
            x, y = self._get_random_position(player, 30)
            enemy_type = random.choices(monsters, weights=chances)[0]
            self.enemy_array.append(Enemy(pygame.Vector2(x, y), enemy_type, self))
            time.sleep(0.5)

    def spawn_perk(self):
        perks = [1, 2, 3]
        chances = [0.4, 0.4, 0.2]
        while self.running:
            if len(self.perk_array) > 5:
                time.sleep(5)
                continue
            x, y = self._get_random_position(None, 40)
            perk_type = random.choices(perks, weights=chances)[0]
            self.perk_array.append(Perk(pygame.Vector2(x, y), perk_type))
            time.sleep(5)

    def _get_random_position(self, player, padding):
        while True:
            x = random.randint(padding, self.screen_width - padding)
            y = random.randint(padding, self.screen_height - padding)
            if player is None or player.position.distance_to(pygame.Vector2(x, y)) >= 700:
                return x, y

    def move_enemies(self, player):
        for enemy in self.enemy_array:
            enemy.move_towards_player(player, self.dt)

    def spawn_arrow(self, player):
        if player.is_reload:
            return
        cursor = pygame.Vector2(pygame.mouse.get_pos())
        starting_pos = player.position.copy() + self.camera_offset
        direction = (cursor - starting_pos).normalize() * 200 * self.dt
        arrow = Arrow(starting_pos, cursor, direction)
        arrow.angle = math.atan2(direction.y, direction.x)
        self.arrow_array.append(arrow)

    def move_arrow(self):
        for arrow in self.arrow_array[:]:
            arrow.position += arrow.direction * 200 * self.dt
            if not (-2000 <= arrow.position.x <= 2000 and -2000 <= arrow.position.y <= 2000):
                self.arrow_array.remove(arrow)
# critical 3
    def move_bullets(self):
        with self.bullets_lock:
            for bullet in self.enemy_bullets[:]:
                bullet.move(self.dt)
                if bullet.check_collision(self.player):
                    self.player.handle_hit(self)
                    self.enemy_bullets.remove(bullet)
                elif not (0 <= bullet.position.x <= self.screen_width and 0 <= bullet.position.y <= self.screen_height):
                    self.enemy_bullets.remove(bullet)

    def render(self):
        self.screen.blit(self.map, self.camera_offset)
        for enemy in self.enemy_array:
            pygame.draw.circle(self.screen, (255, 0, 0), (int(enemy.position.x + self.camera_offset.x), int(enemy.position.y + self.camera_offset.y)), 15)
        for arrow in self.arrow_array:
            pygame.draw.line(self.screen, (0, 255, 0), (arrow.position.x + self.camera_offset.x, arrow.position.y + self.camera_offset.y), (arrow.position.x + arrow.direction.x * 10 + self.camera_offset.x, arrow.position.y + arrow.direction.y * 10 + self.camera_offset.y), 3)
        for bullet in self.enemy_bullets:
            bullet.render(self.screen, self.camera_offset)
        pygame.display.flip()

    def check_hit(self, player):
        for arrow in self.arrow_array[:]:
            if self.bossIsSpawn and self._check_collision(arrow, self.boss, 20, 180):
                self._handle_boss_hit(arrow, player)
                if not self.running:
                    return 3 if self.turn == 2 else 2
            for enemy in self.enemy_array[:]:
                if self._check_collision(arrow, enemy, 40, 40):
                    self._handle_enemy_hit(arrow, enemy, player)
                    break

    def _check_collision(self, arrow, target, offset_x, offset_y):
        return ((target.position.x + self.camera_offset.x - offset_x <= arrow.position.x <= target.position.x + self.camera_offset.x + offset_x) and
                (target.position.y + self.camera_offset.y - offset_y <= arrow.position.y <= target.position.y + self.camera_offset.y + offset_y))

    def _handle_boss_hit(self, arrow, player):
        if arrow in self.arrow_array:
            self.arrow_array.remove(arrow)
        self.boss.hp -= player.dmg
        if self.boss.hp <= 0:
            self.running = False
            player.pd = 0

    def _handle_enemy_hit(self, arrow, enemy, player):
        if arrow in self.arrow_array:
            self.arrow_array.remove(arrow)
        if enemy.take_damage(player.dmg):
            self.enemy_array.remove(enemy)
            player.pd += 10
            if player.pd >= 10:
                player.pd = -10000
                self.start_boss_fight()

    def start_boss_fight(self):
        for enemy in self.enemy_array:
            enemy.alive = False
        self.enemy_array = []
        self.boss_fight = True
        self.map = pygame.transform.scale(map1_dark if self.turn == 1 else map2, (self.screen_width, self.screen_height))
        set_map1_boss_music() if self.turn == 1 else set_map2_boss_music()
        threading.Thread(target=self.spawn_boss).start()

    def spawn_boss(self):
        time.sleep(2)
        self.boss = Boss(pygame.Vector2(self.screen_width / 2, self.screen_height / 2), 'boss1', 10, 600)
        self.bossIsSpawn = True
