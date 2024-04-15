import pygame

model_radius = 40

# Texture loading
knight = pygame.image.load('textures/knight.png')
knight = pygame.transform.scale(knight, (model_radius * 2, model_radius * 2))

knight_hit = pygame.image.load('textures/knight_hit.png')
knight_hit = pygame.transform.scale(knight_hit, (model_radius * 2, model_radius * 2))

wizard = pygame.image.load('textures/wizard.png')
wizard = pygame.transform.scale(wizard, (model_radius * 2, model_radius * 2))

wizard_hit = pygame.image.load('textures/wizard_hit.png')
wizard_hit = pygame.transform.scale(wizard_hit, (model_radius * 2, model_radius * 2))

king = pygame.image.load('textures/king.png')
king = pygame.transform.scale(king, (model_radius * 2, model_radius * 2))

king_hit = pygame.image.load('textures/king_hit.png')
king_hit = pygame.transform.scale(king_hit, (model_radius * 2, model_radius * 2))

shield = pygame.image.load('textures/shield.png')
shield = pygame.transform.scale(shield, (model_radius * 1.7, model_radius * 1.7))

boots = pygame.image.load('textures/boots.png')
boots = pygame.transform.scale(boots, (model_radius * 1.7, model_radius * 1.7))

shield_dis = pygame.image.load('textures/shield_dis.png')
shield_dis = pygame.transform.scale(shield_dis, (model_radius * 1.7, model_radius * 1.7))

enemy1 = pygame.image.load('textures/enemy1.png')
enemy1 = pygame.transform.scale(enemy1, (model_radius * 2, model_radius * 2))

enemy3 = pygame.image.load('textures/enemy3.png')
enemy3 = pygame.transform.scale(enemy3, (model_radius * 2, model_radius * 2))

enemy4 = pygame.image.load('textures/enemy4.png')
enemy4 = pygame.transform.scale(enemy4, (model_radius * 2, model_radius * 2))

enemy5 = pygame.image.load('textures/enemy5.png')
enemy5 = pygame.transform.scale(enemy5, (model_radius * 2, model_radius * 2))

map1_boss = pygame.image.load('textures/map1_boss.png')
map1_boss = pygame.transform.scale(map1_boss, (model_radius * 4, model_radius * 4))

arrow = pygame.image.load('textures/arrow.png')
arrow = pygame.transform.scale(arrow, (model_radius, model_radius))
arrow = pygame.transform.rotate(arrow, 45)

lighting = pygame.image.load('textures/lighting.png')
lighting = pygame.transform.scale(lighting, (model_radius, model_radius))
lighting = pygame.transform.rotate(lighting, 45)

star = pygame.image.load('textures/holy-star.png')
star = pygame.transform.scale(star, (model_radius, model_radius))

arrow_ammo = pygame.image.load('textures/ammo_arrow.png')
arrow_ammo = pygame.transform.scale(arrow_ammo, (model_radius * 2, model_radius * 2))

arrow_ammo_dis = pygame.image.load('textures/ammo_arrow_dis.png')
arrow_ammo_dis = pygame.transform.scale(arrow_ammo_dis, (model_radius * 2, model_radius * 2))

lighting_ammo = pygame.image.load('textures/ammo_lighting.png')
lighting_ammo = pygame.transform.scale(lighting_ammo, (model_radius * 2, model_radius * 2))

lighting_ammo_dis = pygame.image.load('textures/ammo_lighting_dis.png')
lighting_ammo_dis = pygame.transform.scale(lighting_ammo_dis, (model_radius * 2, model_radius * 2))

star_ammo = pygame.image.load('textures/ammo_star.png')
star_ammo = pygame.transform.scale(star_ammo, (model_radius * 2, model_radius * 2))

star_ammo_dis = pygame.image.load('textures/ammo_star_dis.png')
star_ammo_dis = pygame.transform.scale(star_ammo_dis, (model_radius * 2, model_radius * 2))

status_bar = pygame.image.load('textures/status_bar.png')
status_bar = pygame.transform.scale(status_bar, (100, 100))

skull = pygame.image.load('textures/skull.png')
skull = pygame.transform.scale(skull, (100, 100))

map1 = pygame.image.load('textures/map1.png')

map1_dark = pygame.image.load('textures/map1_dark.png')

gif = pygame.image.load('textures/menu.gif')

