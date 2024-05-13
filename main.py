import math
import pygame
import random
import time
import threading

from classes.enemy import Enemy
from classes.player import Player
from classes.arrow import Arrow
from classes.game import Game
from classes.draw import draw_shields, draw_player, draw_arrow, draw_enemy, draw_screen, draw_menu, draw_ammo, draw_perk, draw_used_perk, draw_status_bar, draw_boss, draw_finish
from classes.music_loader import set_menu_music, set_map1_music, set_map2_music, set_outro_music

# Pygame setup
pygame.init()
exit = False
map = 1
player = 0

# Main
def main():
    global exit, music_play, map
    set_menu_music()
    while exit == False:
        game = Game(2560, 1440, (1600,900), map)
        if map == 1:
            player = Player(pygame.Vector2(game.screen_width / 2, game.screen_height / 2))
        game.isSpawn = False
        music_play = False
        if map == 3:
            while game.finish:
                if music_play == False:
                    set_outro_music()
                    music_play = True

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        music_play = False
                        game.running = False
                        game.finish = False
                        game.menu = False
                        exit = True
                        break
                    elif event.type == pygame.MOUSEBUTTONDOWN: # Mouse interaction
                        mouse_pos = pygame.mouse.get_pos()
                        if pygame.Rect(500, 700, 200, 50).collidepoint(mouse_pos):
                            game.finish = False
                            music_play = False
                            player = Player(pygame.Vector2(game.screen_width / 2, game.screen_height / 2))
                            map = 1
                            game.restart()
                        elif pygame.Rect(900, 700, 200, 50).collidepoint(mouse_pos):
                            music_play = False
                            game.running = False
                            game.finish = False
                            game.menu = False
                            exit = True
                draw_finish(game.screen, game.camera_offset, game.screen_width, game.screen_height)
                pygame.display.flip()
        while game.menu:
            if map == 2:
                break
            if music_play == False:
                set_menu_music()
                music_play = True
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game.running = False
                    exit = True
                    game.menu = False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN: # Mouse interaction
                    mouse_pos = pygame.mouse.get_pos()
                    if pygame.Rect(700, 100, 200, 50).collidepoint(mouse_pos):
                        game.menu = False
                        music_play = False
                    elif pygame.Rect(600, 700, 100, 100).collidepoint(mouse_pos):
                        player.set_classes('warrior')
                    elif pygame.Rect(750, 700, 100, 100).collidepoint(mouse_pos):
                        player.set_classes('wizard')
                    elif pygame.Rect(900, 700, 100, 100).collidepoint(mouse_pos):
                        player.set_classes('king')
                    elif pygame.Rect(700, 200, 200, 50).collidepoint(mouse_pos):
                        exit = True
                        game.running = False
                        music_play = False
                        game.menu = False

            if game.menu == True:
                draw_menu(game.screen, game.menu_map, game.camera_offset, player)
                pygame.display.flip()
                    

        while game.running:
            if music_play == False:
                if map == 1:
                    set_map1_music()
                    music_play = True
                else:
                    set_map2_music()
                    music_play = True
            if game.isSpawn == False:
                spawn_enemy_thread = threading.Thread(target=game.spawn_enemy, args=([player]))
                spawn_enemy_thread.start()
                spawn_enemy_thread = threading.Thread(target=game.spawn_perk)
                spawn_enemy_thread.start()
                game.isSpawn = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                    game.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if player.ammo == 0 or player.is_reload == True:
                        break
                    player.ammo -= 1
                    spawn_shoot_thread = threading.Thread(target=game.spawn_arrow, args=([player]))
                    spawn_shoot_thread.start()
                    draw_ammo(player, game.screen, game.window_size)
                    if player.ammo == 0:
                        reload_thread = threading.Thread(target=player.reload)
                        reload_thread.start()

            # Player move
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                player.position.y -= player.speed * game.dt
            if keys[pygame.K_s]:
                player.position.y += player.speed * game.dt
            if keys[pygame.K_a]:
                player.position.x -= player.speed * game.dt
            if keys[pygame.K_d]:
                player.position.x += player.speed * game.dt
            if keys[pygame.K_r]:
                reload_thread = threading.Thread(target=player.reload)
                reload_thread.start()

            # Board block
            player.position.x = max(min(player.position.x, game.screen_width - 40), 40)
            player.position.y = max(min(player.position.y, game.screen_height - 40), 40)

            game.update_camera_offset(player)

            draw_screen(game.screen,game.camera_offset,game.map)
            draw_shields(player, game.screen)
            draw_ammo(player, game.screen, game.window_size)
            game.move_enemies(player)  

            player.check_getHit(game.enemy_array, game)
            if game.running == False:
                music_play = False
                break
            player.check_perk(game.perk_array)
            draw_used_perk(game.screen, game.window_size, player)
            game.move_arrow()
            map = game.check_hit(player)
                
            draw_shields(player, game.screen)
            draw_enemy(game.enemy_array, game.camera_offset, game.screen, game.turn)
            draw_perk(game.perk_array, game.camera_offset, game.screen, player)
            draw_arrow(game.arrow_array, game.screen, player)
            draw_player(player, game.camera_offset, game.screen)
            draw_status_bar(game.screen, game.window_size, player, game)
            if game.bossIsSpawn:
                draw_boss(game.boss, game.camera_offset, game.screen, game.turn)
                if game.boss.ready:
                    if game.boss.rush < 6:
                        game.boss.attack(player,game)
                    else:
                        game.boss.attack2(game,game.enemy_array,game.screen_width, game.screen_height)
                        


            # Update the display
            pygame.display.flip()

            # Limit FPS to 60, and update dt
            game.dt = game.clock.tick(60) / 1000

    pygame.quit()

if __name__ == "__main__":
    main()
