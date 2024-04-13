import pygame
import random
import time
import threading

# Pygame setup
pygame.init()
screen_width, screen_height = 2560, 1440 # Board Size
window_size = (1600, 900)  # Window size
screen = pygame.display.set_mode(window_size) 
clock = pygame.time.Clock()
running = True
dt = 0

# Player setup
player_pos = pygame.Vector2(screen_width / 2, screen_height / 2)
player_speed = 300
player_radius = 40


camera_offset = pygame.Vector2(0, 0)

# List to hold enemies
enemy = []
enemy_speed = 100  

# Function to update the camera offset based on player position
def update_camera_offset():
    camera_offset.x = window_size[0] / 2 - player_pos.x
    camera_offset.y = window_size[1] / 2 - player_pos.y

# Draw Board
def draw_border():
    boundary_rect = pygame.Rect(
        camera_offset.x,
        camera_offset.y,
        screen_width,
        screen_height
    )
    pygame.draw.rect(screen, 'red', boundary_rect, 5) 

# Function to spawn enemies
def spawn_enemy():
    while running:
        time.sleep(0.5)  # Spawns every 0.5 second
        x = random.randint(30, screen_width - 30)
        y = random.randint(30, screen_height - 30)

        if player_pos.distance_to(pygame.Vector2(x, y)) >= 700:
            enemy.append(pygame.Vector2(x, y))

# Function to move enemies towards the player
def move_enemies():
    for e in enemy:
        direction = (player_pos - e).normalize() * enemy_speed * dt
        e += direction

# Main
def main():
    global dt, running

    # Spawn enemy thread
    spawn_enemy_thread = threading.Thread(target=spawn_enemy)
    spawn_enemy_thread.start()

    while running:
        # Poll for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        # Get key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            player_pos.y -= player_speed * dt
        if keys[pygame.K_s]:
            player_pos.y += player_speed * dt
        if keys[pygame.K_a]:
            player_pos.x -= player_speed * dt
        if keys[pygame.K_d]:
            player_pos.x += player_speed * dt

        # Board block
        player_pos.x = max(min(player_pos.x, screen_width - player_radius), player_radius)
        player_pos.y = max(min(player_pos.y, screen_height - player_radius), player_radius)

        update_camera_offset()
        draw_border()
        move_enemies()  

        # Draw enemies
        for circle_pos in enemy:
            screen_circle_pos = (int(circle_pos.x + camera_offset.x), int(circle_pos.y + camera_offset.y))
            pygame.draw.circle(screen, "blue", screen_circle_pos, 20)

        # Draw the player
        player_center_screen = (int(player_pos.x + camera_offset.x), int(player_pos.y + camera_offset.y))
        pygame.draw.circle(screen, "white", player_center_screen, player_radius)

        # Update the display
        pygame.display.flip()

        # Limit FPS to 60, and update dt
        dt = clock.tick(60) / 1000

    pygame.quit()

if __name__ == "__main__":
    main()
