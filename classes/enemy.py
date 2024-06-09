import pygame

class Enemy:
    def __init__(self, position, type):
        self.position = position
        self.type = type
        self.set_attributes()

    def set_attributes(self):
        if self.type == 1:
            self.speed = 100
            self.hp = 30
        elif self.type == 2:
            self.speed = 50
            self.hp = 60
        elif self.type == 3:
            self.speed = 250
            self.hp = 10
        elif self.type == 4:
            self.speed = 200
            self.hp = 30
        elif self.type == 5:
            self.speed = 250
            self.hp = 20

    def move_towards_player(self, player, dt):
        direction = ((player.position - pygame.Vector2(30, 30)) - self.position).normalize() * self.speed * dt
        self.position += direction

    def take_damage(self, damage):
        self.hp -= damage
        return self.hp <= 0 

    def deal_damage_to_player(self, player):
        # Implement logic for enemy to deal damage to the player
        pass
