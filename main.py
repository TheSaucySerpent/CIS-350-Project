import pygame
from character import Character
from enemy import Enemy
from object import Object
pygame.init()

screen_width = 1200
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Title")


running = True
mc = Character(100, 100, 50, 50, .5, 100, 50)
enemy = Enemy(500, 500, 50, 50, .25, 50, 10, mc)
obj = Object(200, 200, 50, 50, 1000)

enemies = [enemy]
objects = [obj]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    mc.move(keys)
    enemy.move_towards_character()
    # Check for collisions between character and enemies
    for enemy in enemies:
        if mc.x < enemy.x + enemy.width and mc.x + mc.width > enemy.x \
           and mc.y < enemy.y + enemy.height and mc.y + mc.height > enemy.y:
            # Characters are colliding, character takes damage
            mc.take_damage(10)
            enemy.take_damage(10)

    # Check for collisions between character and items
    #for item in objects:
    #    if mc.x < item.x + item.width and mc.x + mc.width > item.x \
    #       and mc.y < item.y + item.height and mc.y + mc.height > item.y:
            # Character is colliding, character takes item
    #        if item = smallHealth:
    #            mc.heal(25)
    #        elif item = bigHealth:
    #            mc.heal(100)
    #        elif item = key:
    #            key.pop
    #            print("Player Obtained Key")

    #Make sure objects can't be clipped
    for ob in objects:
        if mc.x < ob.x + ob.width and mc.x + mc.width > ob.x \
            and mc.y < ob.y + ob.height and mc.y + mc.height > ob.y:
            print("L bozo")

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the character
    pygame.draw.rect(screen, (0, 0, 255), (mc.x, mc.y, mc.width, mc.height))

    # Draw the enemy
    if enemy.health > 0:
        pygame.draw.rect(screen, (255, 0, 0), (enemy.x, enemy.y, enemy.width, enemy.height))

    #Draw the object
    pygame.draw.rect(screen, (0,255,0), (obj.x, obj.y, obj.width, obj.height))

    # Update the display
    pygame.display.update()

pygame.quit()
