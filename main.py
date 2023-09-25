import pygame
import glob_var


pygame.init()

screen_width = 1200
screen_height = 700

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Game Title")

# This is just to make it easier to read in the running loop.
mc = glob_var.mc


# Font for displaying text
font = pygame.font.Font(None, 36)
current_room = glob_var.room1
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    keys = pygame.key.get_pressed()
    if not game_over:

        mc.move(keys, 0.0005)
        if current_room == glob_var.room1:

            screen.blit(glob_var.room1.background, (0, 0)) # to draw background
            current_room.draw(screen) # draw everything in the room


            for enemy in current_room.enemies:
                enemy.draw(screen)
                enemy.move_towards_character()
                if mc.x < enemy.x + enemy.width - 10 and mc.x + mc.width > enemy.x \
                        and mc.y < enemy.y + enemy.height - 10 and mc.y + mc.height > enemy.y:
                    # Characters are colliding, character takes damage
                    mc.take_damage(10)

            mc.draw(screen)
            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                if mc.gun != 0:
                    mc.gun.attack()
                else:
                    print("You don't got a gun!")


            # Display the character's stats
            health_text = font.render(f"Health: {mc.health}", True, (255, 255, 255))
            screen.blit(health_text, (10, 10))
            ammo_text = font.render(f"Ammo: {mc.gun.mag_ammo}", True, (255, 255, 255))
            screen.blit(ammo_text, (10, 30))
            mag_text = font.render(f"Mags: {mc.gun.mag_count}", True, (255, 255, 255))
            screen.blit(mag_text, (10, 50))

        if mc.health == 0:
            ded_text = font.render(f"You Died.", True, (255, 0, 0))
            screen.blit(ded_text,
                        ((screen_width - ded_text.get_width()) // 2, (screen_height - ded_text.get_height()) // 2))
            game_over = True

            """if 1050 <= mc.x <= 1100 and 260 <= mc.y <= 360:
            mc.x, mc.y = 100, 100
            current_room = glob_var.room2"""

        elif current_room == glob_var.room2:
            screen.blit(glob_var.room1.background, (0, 0))  # to draw background
            current_room.draw(screen)  # draw everything in the room

            for enemy in current_room.enemies:
                enemy.draw(screen)
                enemy.move_towards_character()
                if mc.x < enemy.x + enemy.width - 10 and mc.x + mc.width > enemy.x \
                        and mc.y < enemy.y + enemy.height - 10 and mc.y + mc.height > enemy.y:
                    # Characters are colliding, character takes damage
                    mc.take_damage(10)

            mc.draw(screen)

            # Display the character's stats
            health_text = font.render(f"Health: {mc.health}", True, (255, 255, 255))
            screen.blit(health_text, (10, 10))
            ammo_text = font.render(f"Ammo: {mc.gun.mag_ammo}", True, (255, 255, 255))
            screen.blit(ammo_text, (10, 30))
            mag_text = font.render(f"Mags: {mc.gun.mag_count}", True, (255, 255, 255))
            screen.blit(mag_text, (10, 50))

        if mc.health == 0:
            ded_text = font.render(f"You Died.", True, (255, 0, 0))
            screen.blit(ded_text,
                        ((screen_width - ded_text.get_width()) // 2, (screen_height - ded_text.get_height()) // 2))
            game_over = True


    pygame.display.update()

pygame.quit()