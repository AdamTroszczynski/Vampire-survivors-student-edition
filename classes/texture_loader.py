import pygame

model_radius = 40

# Texture loading
knight = pygame.image.load('textures/knight.png')
knight = pygame.transform.scale(knight, (model_radius * 2, model_radius * 2))

knight_hit = pygame.image.load('textures/knight_hit.png')
knight_hit = pygame.transform.scale(knight_hit, (model_radius * 2, model_radius * 2))

shield = pygame.image.load('textures/shield.png')
shield = pygame.transform.scale(shield, (model_radius * 1.5, model_radius * 1.5))

enemy1 = pygame.image.load('textures/enemy1.png')
enemy1 = pygame.transform.scale(enemy1, (model_radius * 2, model_radius * 2))

enemy3 = pygame.image.load('textures/enemy3.png')
enemy3 = pygame.transform.scale(enemy3, (model_radius * 2, model_radius * 2))

arrow1 = pygame.image.load('textures/arrow.png')
arrow1 = pygame.transform.scale(arrow1, (model_radius, model_radius))
arrow1 = pygame.transform.rotate(arrow1, 45)

map1 = pygame.image.load('textures/map1.png')

gif = pygame.image.load('test.gif')

