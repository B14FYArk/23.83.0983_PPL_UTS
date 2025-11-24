import os
import time
import random
import keyboard  # pip install keyboard

# GAME SETTINGS
width = 40
height = 20
player_x = width // 2
player_icon = "A"
enemy_icon = "V"
bullet_icon = "|"

bullets = []
enemies = []
score = 0
game_over = False

# CREATE RANDOM ENEMY
def spawn_enemy():
    x = random.randint(1, width - 2)
    enemies.append([x, 1])

# CLEAR SCREEN
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# DRAW GAME
def draw():
    clear()
    screen = [[" " for _ in range(width)] for _ in range(height)]

    # Draw player
    screen[height - 2][player_x] = player_icon

    # Draw enemies
    for ex, ey in enemies:
        if 0 <= ey < height:
            screen[ey][ex] = enemy_icon

    # Draw bullets
    for bx, by in bullets:
        if 0 <= by < height:
            screen[by][bx] = bullet_icon

    # Print screen
    for row in screen:
        print("".join(row))

    print(f"Score: {score}")

# UPDATE BULLETS
def update_bullets():
    global score
    for b in bullets[:]:
        b[1] -= 1
        # Remove bullet if off-screen
        if b[1] < 0:
            bullets.remove(b)
            continue

        # Bullet hits enemy
        for e in enemies[:]:
            if b[0] == e[0] and b[1] == e[1]:
                enemies.remove(e)
                bullets.remove(b)
                score += 10
                break

# UPDATE ENEMIES
def update_enemies():
    global game_over
    for e in enemies[:]:
        e[1] += 1

        # Check collision with player
        if e[1] == height - 2 and e[0] == player_x:
            game_over = True

        # remove if out of screen
        if e[1] >= height:
            enemies.remove(e)

# MAIN GAME LOOP
spawn_timer = 0
Try_SPAWN = 20  # enemy spawn speed

while not game_over:
    draw()

    # Player movement
    if keyboard.is_pressed("left"):
        player_x = max(0, player_x - 1)
    if keyboard.is_pressed("right"):
        player_x = min(width - 1, player_x + 1)

    # Shoot
    if keyboard.is_pressed("space"):
        bullets.append([player_x, height - 3])

    # Enemy spawn timer
    spawn_timer += 1
    if spawn_timer >= Try_SPAWN:
        spawn_enemy()
        spawn_timer = 0

    update_bullets()
    update_enemies()

    time.sleep(0.05)

clear()
print("💀 GAME OVER 💀")
print(f"Final Score: {score}")
          