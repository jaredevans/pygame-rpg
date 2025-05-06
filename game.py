#!/usr/bin/env python3
import pygame

pygame.init()

# ——— Window setup ———
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("My RPG Game")

# ——— Movement speed ———
player_speed = 5

# ——— Load & prepare background ———
background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, (width, height))

# ——— Load images and get rects ———
player_image = pygame.image.load("player.png").convert_alpha()
player_rect = player_image.get_rect(center=(width // 2, height // 2))

enemy_image = pygame.image.load("enemy.png").convert_alpha()
enemy_rect = enemy_image.get_rect(center=(width // 2, height // 2))

# ——— Fix #2: if they overlap on start, push enemy to the right ———
if player_rect.colliderect(enemy_rect):
    enemy_rect.x = player_rect.x + player_rect.width + 20

quest_complete = False

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)  # cap at 60 FPS

    # ——— Event handling ———
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # ——— Input & movement ———
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.move_ip(-player_speed, 0)
    if keys[pygame.K_RIGHT]:
        player_rect.move_ip(player_speed, 0)
    if keys[pygame.K_UP]:
        player_rect.move_ip(0, -player_speed)
    if keys[pygame.K_DOWN]:
        player_rect.move_ip(0, player_speed)

    # ——— Draw background ———
    screen.blit(background, (0, 0))

    # ——— Quest marker & completion ———
    if not quest_complete:
        quest_rect = pygame.Rect(width // 2 - 25, height // 2 - 25, 50, 50)
        pygame.draw.rect(screen, (255, 0, 0), quest_rect)
        if player_rect.colliderect(quest_rect):
            print("You completed the quest!")
            quest_complete = True

    # ——— Blit sprites ———
    screen.blit(player_image, player_rect)
    screen.blit(enemy_image, enemy_rect)

    # ——— Enemy collision check ———
    if player_rect.colliderect(enemy_rect):
        if not quest_complete:
            print("You must complete the quest before fighting the enemy!")
        else:
            print("You defeated the enemy!")
            running = False

    # ——— Update display ———
    pygame.display.flip()

pygame.quit()
