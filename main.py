import math
import pygame
import random
import time
import threading

from classes.enemy import Enemy
from classes.player import Player
from classes.arrow import Arrow
from classes.game import Game
from classes.draw import draw_shields, draw_player, draw_arrow, draw_enemy, draw_screen, draw_menu
from classes.music_loader import set_menu_music, set_map1_music

# Pygame setup
pygame.init()
exit = False
music_play = False
# Main
def main():
    global exit, music_play
    set_menu_music()
    while exit == False:
        game = Game(2560, 1440, (1600,900))
        player = Player(pygame.Vector2(game.screen_width / 2, game.screen_height / 2))
        game.isSpawn = False
        while game.menu:
            if music_play == False:
                set_menu_music()
                music_play = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.running = False
                    exit = True
                    game.menu = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if pygame.Rect(700, 100, 200, 50).collidepoint(mouse_pos):
                        game.menu = False
                        music_play = False
                    elif pygame.Rect(700, 200, 200, 50).collidepoint(mouse_pos):
                        exit = True
                        game.running = False
                        music_play = False
                        game.menu = False

            if game.menu == True:
                draw_menu(game.screen, game.menu_map, game.camera_offset)
                pygame.display.flip()
        

        while game.running:
            if music_play == False:
                set_map1_music()
                music_play = True
            if game.isSpawn == False:
                spawn_enemy_thread = threading.Thread(target=game.spawn_enemy, args=([player]))
                spawn_enemy_thread.start()
                game.isSpawn = True

            # Poll for events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                    game.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    player.ammo -= 1
                    spawn_shoot_thread = threading.Thread(target=game.spawn_arrow, args=([player]))
                    spawn_shoot_thread.start()
                    if player.ammo == 0:
                        reload_thread = threading.Thread(target=player.reload)
                        reload_thread.start()

            # Get key presses
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player.position.y -= player.speed * game.dt
            if keys[pygame.K_s]:
                player.position.y += player.speed * game.dt
            if keys[pygame.K_a]:
                player.position.x -= player.speed * game.dt
            if keys[pygame.K_d]:
                player.position.x += player.speed * game.dt

            # Board block
            player.position.x = max(min(player.position.x, game.screen_width - 40), 40)
            player.position.y = max(min(player.position.y, game.screen_height - 40), 40)

            game.update_camera_offset(player)

            draw_screen(game.screen,game.camera_offset,game.map)

            draw_shields(player, game.screen)
            game.move_enemies(player)  
            player.check_getHit(game.enemy_array, game)
            if game.running == False:
                music_play = False
                break
            game.move_arrow()
            game.check_hit(player)
                
            draw_shields(player, game.screen)
            draw_enemy(game.enemy_array, game.camera_offset, game.screen)
            draw_arrow(game.arrow_array, game.screen)
            draw_player(player, game.camera_offset, game.screen)

            # Update the display
            pygame.display.flip()

            # Limit FPS to 60, and update dt
            game.dt = game.clock.tick(60) / 1000

    pygame.quit()

if __name__ == "__main__":
    main()
