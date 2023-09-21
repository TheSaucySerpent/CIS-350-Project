import pygame
import glob_var

pygame.init()

screen_width = 1200
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Title")

# This is just to make it easier to read in the running loop.
mc = glob_var.mc
obj = glob_var.obj
enemies = glob_var.enemies

# Font for displaying text
font = pygame.font.Font(None, 36)

running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #If r is press, calls weapon reload function
    #If space is pressed and its been 1 second, does a dodge/teleport with invulnerability
    #wasd to move
    keys = pygame.key.get_pressed()
    if not game_over:
        if keys[pygame.K_r]:
            mc.gun.reload()
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - mc.last_dodge > 1000:
                mc.move(keys, 150, True)
                mc.last_dodge = current_time + 100
            else:
                mc.move(keys, 0)
        else:
            mc.move(keys, 0)

        if pygame.mouse.get_pressed()[0]:  # Left mouse button
            if mc.gun != 0:
                mc.gun.attack()
            else:
                print("You don't got a gun!")

        # Check for collisions between character and enemies
        for enemy in enemies:
            enemy.move_towards_character()
            if mc.x < enemy.x + enemy.width - 10 and mc.x + mc.width > enemy.x \
                    and mc.y < enemy.y + enemy.height - 10 and mc.y + mc.height > enemy.y:
                # Characters are colliding, character takes damage
                mc.take_damage(10)

        # Set boundaries on objects
        # Currently only works for main character, and only works properly with square objects.
        for ob in glob_var.objs:


            # Left Border
            if mc.x + mc.width == ob.x and ob.y + ob.height >= mc.y >= ob.y - ob.height:
                while mc.x + mc.width == ob.x and ob.y + ob.height >= mc.y >= ob.y - ob.height:
                    mc.x -= 1

            # Right Border
            if mc.x == ob.x + ob.width and ob.y + ob.height >= mc.y >= ob.y - ob.height:
                while mc.x == ob.x + ob.width and ob.y + ob.height >= mc.y >= ob.y - ob.height:
                    mc.x += 1

            # Lower
            if mc.y == ob.y + ob.height and ob.x + ob.width >= mc.x >= ob.x - ob.width:
                while mc.y == ob.y + ob.height and ob.x + ob.width >= mc.x >= ob.x - ob.width:
                    mc.y += 1

            # Upper
            if mc.y == ob.y - ob.height and ob.x + ob.width >= mc.x >= ob.x - ob.width:
                while mc.y == ob.y - ob.height and ob.x + ob.width >= mc.x >= ob.x - ob.width:
                    mc.y -= 1

    screen.fill((0, 0, 0))

    # Draw the character
    pygame.draw.rect(screen, (0, 0, 255), (mc.x, mc.y, mc.width, mc.height))

    # Draw projectiles
    for g in glob_var.guns:
        for p in g.projectiles:
            p.move()
            pygame.draw.rect(screen, (255, 255, 0), (p.x, p.y, p.width, p.height))
        g.update_projectiles()

    # Draw/kill the enemy
    for enemy in enemies:
        if enemy.health > 0:
            pygame.draw.rect(screen, (255, 0, 0), (enemy.x, enemy.y, enemy.width, enemy.height))
        else:
            enemies.remove(enemy)

    # Draw objects
    for ob in glob_var.objs:
        pygame.draw.rect(screen, (0, 255, 0), (ob.x, ob.y, ob.width, ob.height))

    # Display the character's stats
    health_text = font.render(f"Health: {mc.health}", True, (255, 255, 255))
    screen.blit(health_text, (10, 10))
    ammo_text = font.render(f"Ammo: {mc.gun.mag_ammo}", True, (255, 255, 255))
    screen.blit(ammo_text, (10, 30))
    mag_text = font.render(f"Mags: {mc.gun.mag_count}", True, (255, 255, 255))
    screen.blit(mag_text, (10, 50))

    # Death Message/Game Over
    if mc.health == 0:
        ded_text = font.render(f"You Died.", True, (255, 0, 0))
        screen.blit(ded_text,
                    ((screen_width - ded_text.get_width()) // 2, (screen_height - ded_text.get_height()) // 2))
        game_over = True

    pygame.display.update()

pygame.quit()
