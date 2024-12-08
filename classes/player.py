import pygame
import threading
import time
from classes.texture_loader import knight, knight_hit

class Player:
    def __init__(self, position):
        self.position = position
        self.set_classes('warrior') 
        self.immortality = False
        self.is_reload = False
        self.perk_cooldown = False
        self.perks = []
        self.lock_hit = threading.Lock()
        self.lock_perk = threading.Lock()
        self.pd = 0

    def set_classes(self, name):
        classes = {
            'warrior': {'speed': 300, 'hp': 7, 'dmg': 15, 'ammo': 2, 'reload_time': 1},
            'wizard': {'speed': 350, 'hp': 4, 'dmg': 25, 'ammo': 3, 'reload_time': 1.5},
            'king': {'speed': 300, 'hp': 2, 'dmg': 35, 'ammo': 5, 'reload_time': 1}
        }
        
        if name in classes:
            self.category = name
            attributes = classes[name]
            self.speed = attributes['speed']
            self.hp = self.max_hp = attributes['hp']
            self.dmg = attributes['dmg']
            self.ammo = self.max_ammo = attributes['ammo']
            self.reload_time = attributes['reload_time']

# critical 1
    def check_getHit(self, enemy_array, game):
        with self.lock_hit:
            if self.immortality:
                return
            
            if game.bossIsSpawn:
                self.check_collision_with_boss(game)
            else:
                self.check_collision_with_enemies(enemy_array, game)

    def check_collision_with_boss(self, game):
        boss = game.boss
        if (boss.position.x - 20 <= self.position.x <= boss.position.x + 180) and \
           (boss.position.y - 20 <= self.position.y <= boss.position.y + 180):
            self.handle_hit(game)

    def check_collision_with_enemies(self, enemy_array, game):
        for enemy in enemy_array:
            if (enemy.position.x - 40 <= self.position.x <= enemy.position.x + 40) and \
               (enemy.position.y - 40 <= self.position.y <= enemy.position.y + 40):
                self.handle_hit(game)
                break

    def handle_hit(self, game):
        self.hp -= 1
        if self.hp == 0:
            game.menu = True
            game.running = False
            self.reset_player()
        else:
            threading.Thread(target=self.set_immortality).start()

    def reset_player(self):
        self.hp = self.max_hp
        self.ammo = self.max_ammo

    def set_immortality(self):
        self.immortality = True
        time.sleep(1)
        self.immortality = False

    def check_perk(self, perk_array):
        for perk in perk_array:
            if self.is_colliding_with_perk(perk):
                self.apply_perk(perk, perk_array)

    def is_colliding_with_perk(self, perk):
        return ((self.position.x >= perk.position.x - 30) and (self.position.x <= perk.position.x + 70)) and \
               ((self.position.y >= perk.position.y - 40) and (self.position.y <= perk.position.y + 40))

    def apply_perk(self, perk, perk_array):
        if perk.type == 1:
            self.apply_health_perk(perk, perk_array)
        elif perk.type in (2, 3):
            self.apply_boost_perk(perk)
            perk_array.remove(perk)

    def apply_health_perk(self, perk, perk_array):
        if self.hp < self.max_hp:
            self.hp += 1
            perk_array.remove(perk)

    def apply_boost_perk(self, perk):
        boost_thread = threading.Thread(target=self.activate_perk, args=(perk,))
        boost_thread.start()

# critical 2 
    def activate_perk(self, perk):
        with self.lock_perk:
            if perk.type == 2:
                self.speed_boost(perk)
            elif perk.type == 3:
                self.reload_boost(perk)

    def speed_boost(self, perk):
        self.perks.append(perk)
        self.speed *= 1.3
        time.sleep(3)
        self.speed /= 1.3
        self.perks.remove(perk)

    def reload_boost(self, perk):
        self.perks.append(perk)
        self.reload_time /= 2
        time.sleep(3)
        self.reload_time *= 2
        self.perks.remove(perk)

    def reload(self):
        self.is_reload = True
        time.sleep(self.reload_time)
        self.ammo = self.max_ammo
        self.is_reload = False
