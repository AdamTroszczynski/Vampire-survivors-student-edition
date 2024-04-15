import pygame
import math
import time
from classes.texture_loader import shield, shield_dis, skull, arrow, enemy4, enemy5, map1_boss, lighting, star, enemy1, status_bar, enemy3, boots, arrow_ammo, arrow_ammo_dis, lighting_ammo, lighting_ammo_dis, star_ammo, star_ammo_dis, knight, knight_hit, wizard, wizard_hit, king, king_hit


def draw_shields(player, screen):
    for i in range(player.max_hp):
        player_center_screen = (int(0 + 30 + 60 * i ), int(0 + 30))
        screen.blit(shield_dis, player_center_screen)
    for i in range(player.hp):
        player_center_screen = (int(0 + 30 + 60 * i ), int(0 + 30))
        screen.blit(shield, player_center_screen)

def draw_ammo(player, screen, window_size):
    for i in range(player.max_ammo):
        if player.category == 'warrior':
            player_center_screen = (int(window_size[0]- 30 - 40 * (i + 1)),int(0 + 30))
            screen.blit(arrow_ammo_dis, player_center_screen)
        elif player.category == 'wizard':
            player_center_screen = (int(window_size[0]- 30 - 60 * (i + 1)),int(0 + 30))
            screen.blit(lighting_ammo_dis, player_center_screen)
        elif player.category == 'king':
            player_center_screen = (int(window_size[0]- 30 - 60 * (i + 1)),int(0 + 30))
            screen.blit(star_ammo_dis, player_center_screen)
    for i in range(player.ammo):
        if player.category == 'warrior':
            player_center_screen = (int(window_size[0]- 30 - 40 * (i + 1)),int(0 + 30))
            screen.blit(arrow_ammo, player_center_screen)
        elif player.category == 'wizard':
            player_center_screen = (int(window_size[0]- 30 - 60 * (i + 1)),int(0 + 30))
            screen.blit(lighting_ammo, player_center_screen)
        elif player.category == 'king':
            player_center_screen = (int(window_size[0]- 30 - 60 * (i + 1)),int(0 + 30))
            screen.blit(star_ammo, player_center_screen)

def draw_used_perk(screen, window_size, player):
    i = 1
    for perk in player.perks:
        player_center_screen = (int(window_size[0] - 75 * i ),int(0 + 140))
        if perk.type == 2:
            screen.blit(boots, player_center_screen)
        elif perk.type == 3:
            if player.category == 'warrior':
                screen.blit(arrow_ammo, player_center_screen)
            elif player.category == 'wizard':
                screen.blit(lighting_ammo, player_center_screen)
            elif player.category == 'king':
                screen.blit(star_ammo, player_center_screen)
        i += 1


def draw_player(player,camera_offset, screen):
    # Draw the player with rotation towards the mouse cursor
    player_center_screen = (int(player.position.x + camera_offset.x), int(player.position.y + camera_offset.y))
    mouse_pos = pygame.mouse.get_pos()
    angle = math.atan2(mouse_pos[1] - player_center_screen[1], mouse_pos[0] - player_center_screen[0])
    # Odwrócenie kąta o 180 stopni, aby postać patrzyła się w górę
    angle -= math.pi
    awatar = ''
    if player.category == 'warrior':
        if player.immortality == True:
            awatar = knight_hit
        else:
            awatar = knight
    elif player.category == 'wizard':
        if player.immortality == True:
            awatar = wizard_hit
        else:
            awatar = wizard
    elif player.category == 'king':
        if player.immortality == True:
            awatar = king_hit
        else:
            awatar = king
    rotated_knight = pygame.transform.rotate(awatar, math.degrees(-angle) + 90)
    rotated_rect = rotated_knight.get_rect(center=player_center_screen)
    screen.blit(rotated_knight, rotated_rect)

def draw_arrow(arrow_array, screen, player):
        for arrow_obj in arrow_array:
            screen_arrow_pos = (int(arrow_obj.position.x), int(arrow_obj.position.y))
            if player.category == 'warrior':
                arrow_rotated = pygame.transform.rotate(arrow, (math.degrees(-arrow_obj.angle - math.pi) + 90))  # Użycie obliczonego kąta
            elif player.category == 'wizard': 
                arrow_rotated = pygame.transform.rotate(lighting, (math.degrees(-arrow_obj.angle - math.pi) + 90))  # Użycie obliczonego kąta
            elif player.category == 'king':
                arrow_rotated = pygame.transform.rotate(star, (math.degrees(-arrow_obj.angle - math.pi) + 90))
            screen.blit(arrow_rotated, screen_arrow_pos)
    
def draw_enemy(enemy_array, camera_offset, screen):
     for enemy in enemy_array:
            screen_enemy_pos = (int(enemy.position.x + camera_offset.x), int(enemy.position.y + camera_offset.y))
            if enemy.type == 1:
                screen.blit(enemy1, screen_enemy_pos)
            if enemy.type == 3:
                screen.blit(enemy3, screen_enemy_pos)
            if enemy.type == 4:
                screen.blit(enemy4, screen_enemy_pos)
            if enemy.type == 5:
                screen.blit(enemy5, screen_enemy_pos)

def draw_boss(boss, camera_offset, screen):
    screen_enemy_pos = (int(boss.position.x + camera_offset.x), int(boss.position.y + camera_offset.y))
    screen.blit(map1_boss, screen_enemy_pos)

def draw_perk(perk_array, camera_offset, screen, player):
    for perk in perk_array:
        screen_perk_pos = (int(perk.position.x + camera_offset.x), int(perk.position.y + camera_offset.y))
        if perk.type == 1:
            screen.blit(shield, screen_perk_pos)
        elif perk.type == 2:
            screen.blit(boots, screen_perk_pos)
        elif perk.type == 3:
            if player.category == 'warrior':
                screen.blit(arrow_ammo, screen_perk_pos)
            elif player.category == 'wizard':
                screen.blit(lighting_ammo, screen_perk_pos)
            elif player.category == 'king':
                screen.blit(star_ammo, screen_perk_pos)


def draw_screen(screen, camera_offset, map1):
    screen.fill((0,0,0))
    screen.blit(map1, (camera_offset.x, camera_offset.y))

def draw_menu(screen, map1, camera_offset, player):

    screen.blit(map1, (camera_offset.x, camera_offset.y))
    font = pygame.font.Font(None, 36)


    # Wybór postaci
    hero1 = pygame.Rect(600, 700, 100, 100)
    darker_hero1 = hero1.inflate(15, 15)  # Rozszerzenie prostokąta o 5 pikseli w każdym kierunku
    if player.category == 'warrior':
        pygame.draw.rect(screen, (30,0,0), darker_hero1)
        pygame.draw.rect(screen, (60,0,0), hero1)
    else:
        pygame.draw.rect(screen, (41,0,0), hero1)
    hero1_rect = knight.get_rect(center=hero1.center)
    screen.blit(knight, hero1_rect)

    hero2 = pygame.Rect(750, 700, 100, 100)
    darker_hero2 = hero2.inflate(15, 15)  # Rozszerzenie prostokąta o 5 pikseli w każdym kierunku
    if player.category == 'wizard':
        pygame.draw.rect(screen, (30,0,0), darker_hero2)
        pygame.draw.rect(screen, (60,0,0), hero2)
    else:
        pygame.draw.rect(screen, (41,0,0), hero2)
    hero2_rect = wizard.get_rect(center=hero2.center)
    screen.blit(wizard, hero2_rect)

    hero3 = pygame.Rect(900, 700, 100, 100)
    darker_hero3 = hero3.inflate(15, 15)  # Rozszerzenie prostokąta o 5 pikseli w każdym kierunku
    if player.category == 'king':
        pygame.draw.rect(screen, (30,0,0), darker_hero3)
        pygame.draw.rect(screen, (60,0,0), hero3)
    else:
        pygame.draw.rect(screen, (41,0,0), hero3)
    hero3_rect = king.get_rect(center=hero3.center)
    screen.blit(king, hero3_rect)

    # Przyciski menu
    button1 = pygame.Rect(700, 100, 200, 50)
    pygame.draw.rect(screen, (255,255,255), button1)
    button1_text = font.render("Start", True, (0,0,0))
    button1_text_rect = button1_text.get_rect(center=button1.center)
    screen.blit(button1_text, button1_text_rect)

    button2 = pygame.Rect(700, 200, 200, 50)
    pygame.draw.rect(screen, (255,255,255), button2)
    button2_text = font.render("Exit", True, (0,0,0))
    button2_text_rect = button2_text.get_rect(center=button2.center)
    screen.blit(button2_text, button2_text_rect)

def draw_status_bar(screen, window_size, player, game):
    points = [(window_size[0]- 70, 350), (window_size[0]- 50,355), (window_size[0]- 30,350), (window_size[0]- 30,325), (window_size[0]- 20,315), (window_size[0]- 22, 285), (window_size[0]- 28,280), (window_size[0]- 50,275), (window_size[0]- 70,280), (window_size[0]- 75,285), (window_size[0]- 75,315), (window_size[0]- 70,325)]
    player_center_screen = (int(window_size[0]- 100),int(0 + 261))
    color = player.pd / 2
    if not game.boss_fight:
        pygame.draw.polygon(screen, (color,0 ,0), points)
        screen.blit(status_bar, player_center_screen)
    if game.boss_fight:
        screen.blit(skull, player_center_screen)
    
    
