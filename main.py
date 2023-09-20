import pygame
import glob_var
pygame.init()

screen_width = 1200
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Title")

#This is just to make it easier to read in the running loop.
mc = glob_var.mc
enemy = glob_var.enemy
obj = glob_var.obj
enemies = glob_var.enemies

# Create a font object for displaying text
font = pygame.font.Font(None, 36)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    mc.move(keys)

    if pygame.mouse.get_pressed()[0]:  # Left mouse button
        if mc.gun != 0:
            mc.gun.attack()
        else:
            print("You don't got a gun!")



    # Check for collisions between character and enemies
    for enemy in enemies:
        enemy.move_towards_character()
        if mc.x < enemy.x + enemy.width and mc.x + mc.width > enemy.x \
           and mc.y < enemy.y + enemy.height and mc.y + mc.height > enemy.y:
            # Characters are colliding, character takes damage
            mc.take_damage(10)

    #Checks if character is in object, should keep them out instead of saying L bozo.
    for ob in glob_var.objs:
        if mc.x < ob.x + ob.width and mc.x + mc.width > ob.x \
            and mc.y < ob.y + ob.height and mc.y + mc.height > ob.y:
            print("L bozo")

    screen.fill((0, 0, 0))

    # Draw the character
    pygame.draw.rect(screen, (0, 0, 255), (mc.x, mc.y, mc.width, mc.height))


    #Draw projectiles
    for g in glob_var.guns:
        for p in g.projectiles:
            p.move()
            pygame.draw.rect(screen, (0, 0, 255), (p.x, p.y, p.width, p.height))
        g.update_projectiles()

    # Draw/kill the enemy
    for enemy in enemies:
        if enemy.health > 0:
            pygame.draw.rect(screen, (255, 0, 0), (enemy.x, enemy.y, enemy.width, enemy.height))
        else:
            enemies.remove(enemy)

    #Draw the object
    pygame.draw.rect(screen, (0,255,0), (obj.x, obj.y, obj.width, obj.height))

    # Display the character's health
    health_text = font.render(f"Health: {mc.health}", True, (255, 255, 255))
    screen.blit(health_text, (10, 10))
    ammo_text = font.render(f"Ammo: {mc.gun.ammo}", True, (255, 255, 255))
    screen.blit(ammo_text, (10, 30))

    # Update the display
    pygame.display.update()

pygame.quit()
