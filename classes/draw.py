import pygame
import math
from classes.texture_loader import shield, arrow1, enemy1, enemy3


def draw_shields(player, screen):
    for i in range(player.hp):
        player_center_screen = (int(0 + 30 + 80 * i ), int(0 + 30))
        screen.blit(shield, player_center_screen)

def draw_player(player,camera_offset, screen):
    # Draw the player with rotation towards the mouse cursor
    player_center_screen = (int(player.position.x + camera_offset.x), int(player.position.y + camera_offset.y))
    mouse_pos = pygame.mouse.get_pos()
    angle = math.atan2(mouse_pos[1] - player_center_screen[1], mouse_pos[0] - player_center_screen[0])
    # Odwrócenie kąta o 180 stopni, aby postać patrzyła się w górę
    angle -= math.pi
    rotated_knight = pygame.transform.rotate(player.awatar, math.degrees(-angle) + 90)
    rotated_rect = rotated_knight.get_rect(center=player_center_screen)
    screen.blit(rotated_knight, rotated_rect)

def draw_arrow(arrow_array, screen):
        for arrow in arrow_array:
            screen_arrow_pos = (int(arrow.position.x), int(arrow.position.y))
            arrow_rotated = pygame.transform.rotate(arrow1, (math.degrees(-arrow.angle - math.pi) + 90))  # Użycie obliczonego kąta
            screen.blit(arrow_rotated, screen_arrow_pos)
    
def draw_enemy(enemy_array, camera_offset, screen):
     for enemy in enemy_array:
            screen_enemy_pos = (int(enemy.position.x + camera_offset.x), int(enemy.position.y + camera_offset.y))
            if enemy.type == 1:
                screen.blit(enemy1, screen_enemy_pos)
            if enemy.type == 3:
                screen.blit(enemy3, screen_enemy_pos)

def draw_screen(screen, camera_offset, map1):
    screen.fill((0,0,0))
    screen.blit(map1, (camera_offset.x, camera_offset.y))

def draw_menu(screen, map1, camera_offset):

    screen.blit(map1, (camera_offset.x, camera_offset.y))
    font = pygame.font.Font(None, 36)

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