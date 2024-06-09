import pygame
import math
import time
from classes.texture_loader import (
    shield, shield_dis, skull, enemy1_1, enemy3_1, enemy4_1, enemy5_1,
    map2_boss, victory, arrow, enemy4, enemy5, map1_boss, lighting, star,
    enemy1, status_bar, enemy3, boots, arrow_ammo, arrow_ammo_dis,
    lighting_ammo, lighting_ammo_dis, star_ammo, star_ammo_dis, knight,
    knight_hit, wizard, wizard_hit, king, king_hit
)

# Drawing active/inactive shields/ammo
def draw_shields(player, screen):
    for i in range(player.max_hp):
        player_center_screen = (30 + 60 * i, 30)
        screen.blit(shield_dis, player_center_screen)
    for i in range(player.hp):
        player_center_screen = (30 + 60 * i, 30)
        screen.blit(shield, player_center_screen)

def draw_ammo(player, screen, window_size):
    for i in range(player.max_ammo):
        player_center_screen = (window_size[0] - 30 - 40 * (i + 1), 30)
        if player.category == 'warrior':
            screen.blit(arrow_ammo_dis, player_center_screen)
        elif player.category == 'wizard':
            player_center_screen = (window_size[0] - 30 - 60 * (i + 1), 30)
            screen.blit(lighting_ammo_dis, player_center_screen)
        elif player.category == 'king':
            player_center_screen = (window_size[0] - 30 - 60 * (i + 1), 30)
            screen.blit(star_ammo_dis, player_center_screen)
    for i in range(player.ammo):
        player_center_screen = (window_size[0] - 30 - 40 * (i + 1), 30)
        if player.category == 'warrior':
            screen.blit(arrow_ammo, player_center_screen)
        elif player.category == 'wizard':
            player_center_screen = (window_size[0] - 30 - 60 * (i + 1), 30)
            screen.blit(lighting_ammo, player_center_screen)
        elif player.category == 'king':
            player_center_screen = (window_size[0] - 30 - 60 * (i + 1), 30)
            screen.blit(star_ammo, player_center_screen)

def draw_used_perk(screen, window_size, player):
    for i, perk in enumerate(player.perks, start=1):
        player_center_screen = (window_size[0] - 75 * i, 140)
        if perk.type == 2:
            screen.blit(boots, player_center_screen)
        elif perk.type == 3:
            if player.category == 'warrior':
                screen.blit(arrow_ammo, player_center_screen)
            elif player.category == 'wizard':
                screen.blit(lighting_ammo, player_center_screen)
            elif player.category == 'king':
                screen.blit(star_ammo, player_center_screen)

def draw_player(player, camera_offset, screen):
    player_center_screen = (int(player.position.x + camera_offset.x), int(player.position.y + camera_offset.y))
    mouse_pos = pygame.mouse.get_pos()
    angle = math.atan2(mouse_pos[1] - player_center_screen[1], mouse_pos[0] - player_center_screen[0]) - math.pi
    if player.category == 'warrior':
        awatar = knight_hit if player.immortality else knight
    elif player.category == 'wizard':
        awatar = wizard_hit if player.immortality else wizard
    elif player.category == 'king':
        awatar = king_hit if player.immortality else king
    rotated_knight = pygame.transform.rotate(awatar, math.degrees(-angle) + 90)
    rotated_rect = rotated_knight.get_rect(center=player_center_screen)
    screen.blit(rotated_knight, rotated_rect)

def draw_arrow(arrow_array, screen, player):
    for arrow_obj in arrow_array:
        screen_arrow_pos = (int(arrow_obj.position.x), int(arrow_obj.position.y))
        if player.category == 'warrior':
            arrow_rotated = pygame.transform.rotate(arrow, math.degrees(-arrow_obj.angle - math.pi) + 90)
        elif player.category == 'wizard':
            arrow_rotated = pygame.transform.rotate(lighting, math.degrees(-arrow_obj.angle - math.pi) + 90)
        elif player.category == 'king':
            arrow_rotated = pygame.transform.rotate(star, math.degrees(-arrow_obj.angle - math.pi) + 90)
        screen.blit(arrow_rotated, screen_arrow_pos)

def draw_enemy(enemy_array, camera_offset, screen, turn):
    for enemy in enemy_array:
        screen_enemy_pos = (int(enemy.position.x + camera_offset.x), int(enemy.position.y + camera_offset.y))
        if enemy.type == 1:
            screen.blit(enemy1_1 if turn == 2 else enemy1, screen_enemy_pos)
        elif enemy.type == 3:
            screen.blit(enemy3_1 if turn == 2 else enemy3, screen_enemy_pos)
        elif enemy.type == 4:
            screen.blit(enemy4_1 if turn == 2 else enemy4, screen_enemy_pos)
        elif enemy.type == 5:
            screen.blit(enemy5_1 if turn == 2 else enemy5, screen_enemy_pos)

def draw_boss(boss, camera_offset, screen, turn):
    screen_enemy_pos = (int(boss.position.x + camera_offset.x), int(boss.position.y + camera_offset.y))
    screen.blit(map1_boss if turn == 1 else map2_boss, screen_enemy_pos)

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
    screen.fill((0, 0, 0))
    screen.blit(map1, (camera_offset.x, camera_offset.y))

def draw_finish(screen, camera_offset, screen_width, screen_height):
    map = pygame.transform.scale(victory, (screen_width / 1.5, screen_height / 1.5))
    screen.blit(map, (camera_offset.x, camera_offset.y))
    font = pygame.font.Font(None, 36)

    button1 = pygame.Rect(700, 100, 200, 50)
    pygame.draw.rect(screen, (255, 255, 255), button1)
    button1_text = font.render("You win!", True, (0, 0, 0))
    button1_text_rect = button1_text.get_rect(center=button1.center)
    screen.blit(button1_text, button1_text_rect)

    button2 = pygame.Rect(500, 700, 200, 50)
    pygame.draw.rect(screen, (255, 255, 255), button2)
    button2_text = font.render("Play again", True, (0, 0, 0))
    button2_text_rect = button2_text.get_rect(center=button2.center)
    screen.blit(button2_text, button2_text_rect)

    button3 = pygame.Rect(900, 700, 200, 50)
    pygame.draw.rect(screen, (255, 255, 255), button3)
    button3_text = font.render("Exit", True, (0, 0, 0))
    button3_text_rect = button3_text.get_rect(center=button3.center)
    screen.blit(button3_text, button3_text_rect)

def draw_menu(screen, map1, camera_offset, player):
    screen.blit(map1, (camera_offset.x, camera_offset.y))
    font = pygame.font.Font(None, 36)

    draw_hero_selection(screen, player)
    draw_menu_buttons(screen, font)

def draw_hero_selection(screen, player):
    heroes = [
        (600, 'warrior', knight),
        (750, 'wizard', wizard),
        (900, 'king', king)
    ]
    for x, category, image in heroes:
        hero_rect = pygame.Rect(x, 700, 100, 100)
        darker_hero_rect = hero_rect.inflate(15, 15)
        color = (60, 0, 0) if player.category == category else (41, 0, 0)
        pygame.draw.rect(screen, color, hero_rect)
        if player.category == category:
            pygame.draw.rect(screen, (30, 0, 0), darker_hero_rect)
        hero_image_rect = image.get_rect(center=hero_rect.center)
        screen.blit(image, hero_image_rect)

def draw_menu_buttons(screen, font):
    buttons = [
        (700, 100, "Start"),
        (700, 200, "Exit")
    ]
    for x, y, text in buttons:
        button = pygame.Rect(x, y, 200, 50)
        pygame.draw.rect(screen, (255, 255, 255), button)
        button_text = font.render(text, True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=button.center)
        screen.blit(button_text, button_text_rect)

def draw_status_bar(screen, window_size, player, game):
    points = [
        (window_size[0] - 70, 350), (window_size[0] - 50, 355), (window_size[0] - 30, 350),
        (window_size[0] - 30, 325), (window_size[0] - 20, 315), (window_size[0] - 22, 285),
        (window_size[0] - 28, 280), (window_size[0] - 50, 275), (window_size[0] - 70, 280),
        (window_size[0] - 75, 285), (window_size[0] - 75, 315), (window_size[0] - 70, 325)
    ]
    player_center_screen = (window_size[0] - 100, 261)
    color = player.pd / 2
    if not game.boss_fight:
        pygame.draw.polygon(screen, (color, 0, 0), points)
        screen.blit(status_bar, player_center_screen)
    else:
        screen.blit(skull, player_center_screen)
