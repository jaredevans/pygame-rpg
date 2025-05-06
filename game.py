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

# ——— If they overlap on start, push enemy to the right ———
if player_rect.colliderect(enemy_rect):
    enemy_rect.x = player_rect.x + player_rect.width + 20

# ——— Game states ———
quest_complete = False
game_state = "playing"   # can be "playing" or "dialogue"

# ——— Dialogue definitions ———
pre_quest_text = """
[The Rustborn's mismatched eyes flicker, gears whining softly under strain. Its rusted jaw shifts with a smug creak as it leans against a bent antenna pole.]

Rustborn NPC:

"Well, look what the sandstorm dragged in. Another self-righteous relic hunter with a shiny gun and a hero complex. Let me guess—you’re here to 'make things right'?

Careful, 'Protector.' Folks out here got a funny way of thanking saviors—especially the ones that don't bleed. You tracking me, or just lost on your moral high road?

[It pauses, scanning Arin's drone with suspicion.]

"Nice toy. Hope it ain’t listening for them. They’re always listening. Always."
"""

post_quest_text = """
[With the quest complete, you confront the Rustborn once more. It whirs nervously, metal plates rattling as you approach.]

You:

"It’s over. Step aside or face the consequences."

[The Rustborn’s gears grind as it steps back, sparks flying.]

"…Fine. You win this time, Protector. But the desert never forgets—"
"""

# common footer
footer = "-- Press SPACE or ENTER to continue --"

active_text = ""
# ——— Font & styling ———
font = pygame.font.Font(None, 24)
padding = 10
box_w = 420
line_spacing = 4  # extra px between wrapped lines

def wrap_text(text, font, max_width):
    """Takes a block of text, returns a list of lines wrapped to max_width."""
    lines = []
    for paragraph in text.strip().split("\n"):
        words = paragraph.split(" ")
        if not words:
            lines.append("")
            continue
        cur_line = words[0]
        for word in words[1:]:
            test = cur_line + " " + word
            if font.size(test)[0] <= max_width:
                cur_line = test
            else:
                lines.append(cur_line)
                cur_line = word
        lines.append(cur_line)
    return lines

def draw_dialogue(surface, text):
    # wrap the block + footer
    wrapped = wrap_text(text, font, box_w - 2 * padding)
    wrapped.append("")  # blank line before footer
    wrapped.append(footer)

    # compute box height
    line_h = font.get_linesize() + line_spacing
    box_h = line_h * len(wrapped) + padding * 2
    x = width - box_w - 20
    y = 40

    # draw translucent box
    box = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
    box.fill((0, 0, 0, 200))
    surface.blit(box, (x, y))

    # blit each line
    for idx, line in enumerate(wrapped):
        txt_surf = font.render(line, True, (255, 255, 255))
        surface.blit(txt_surf, (x + padding, y + padding + idx * line_h))


clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    # ——— Event handling ———
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif game_state == "dialogue" and event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                if active_text is post_quest_text:
                    running = False
                else:
                    game_state = "playing"

    # ——— Movement (playing only) ———
    if game_state == "playing":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.move_ip(-player_speed, 0)
        if keys[pygame.K_RIGHT]:
            player_rect.move_ip(player_speed, 0)
        if keys[pygame.K_UP]:
            player_rect.move_ip(0, -player_speed)
        if keys[pygame.K_DOWN]:
            player_rect.move_ip(0, player_speed)

    # ——— Draw scene ———
    screen.blit(background, (0, 0))
    screen.blit(player_image, player_rect)
    screen.blit(enemy_image, enemy_rect)

    # ——— Quest marker ———
    if game_state == "playing" and not quest_complete:
        quest_rect = pygame.Rect(width//2-25, height//2-25, 50, 50)
        pygame.draw.rect(screen, (255, 0, 0), quest_rect)
        if player_rect.colliderect(quest_rect):
            quest_complete = True

    # ——— Enemy collision ———
    if game_state == "playing" and player_rect.colliderect(enemy_rect):
        active_text = post_quest_text if quest_complete else pre_quest_text
        game_state = "dialogue"

    # ——— Dialogue overlay ———
    if game_state == "dialogue":
        draw_dialogue(screen, active_text)

    pygame.display.flip()

pygame.quit()
