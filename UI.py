import random
import pygame
import colors
import colors as c

# chooses random menu background
menu_background_options = ['images/menu_background' + str(i) + '.png' for i in range(1, 6)]
menu_background_selection = random.choice(menu_background_options)


def display_startup_menu(screen, screen_width, screen_height, font):
    """
    Display the startup menu with a random background.

    Args:
        screen (pygame.Surface): The game screen.
        screen_width (int): The width of the screen.
        screen_height (int): The height of the screen.
        font (pygame.font.Font): The font used for text rendering.
    """
    # loads menu background
    menu_background = pygame.image.load(menu_background_selection)
    menu_background.convert()

    # scales background image to screen size
    menu_background = pygame.transform.scale(menu_background, (screen_width, screen_height))

    # creates bounding box for the image
    img_rect = menu_background.get_rect()
    img_rect.center = screen_width // 2, screen_height // 2

    # relevant text for the menu
    game_title = font.render('CIS 350 Project', True, c.WHITE)
    new_game_text = font.render('Press N for New Game', True, c.WHITE)

    # centers game title on menu
    title_rect = game_title.get_rect()
    title_rect.center = img_rect.center

    # places new game text under game title
    new_game_rect = new_game_text.get_rect()
    new_game_rect.center = (screen_width // 2, title_rect.bottom + 20)

    # displays the menu
    screen.blit(menu_background, img_rect)
    screen.blit(game_title, title_rect)
    screen.blit(new_game_text, new_game_rect)

    # updates the display
    pygame.display.flip()


def display_death_menu(screen, screen_width, screen_height, font):
    """
        Display the death menu with the death screen background image.

        Args:
            screen (pygame.Surface): The game screen.
            screen_width (int): The width of the screen.
            screen_height (int): The height of the screen.
            font (pygame.font.Font): The font used for text rendering.
    """
    death_background = pygame.image.load("images/death_background.jpg")
    death_background.convert()

    # scales background image to screen size
    death_background = pygame.transform.scale(death_background, (screen_width, screen_height))

    # creates bounding box for the image
    img_rect = death_background.get_rect()
    img_rect.center = screen_width // 2, screen_height // 2

    # displays the death menu
    screen.blit(death_background, img_rect)

    # display new game text on death menu
    new_game_text = font.render("Press N to Start New Game", True, (255, 255, 255))
    screen.blit(new_game_text,
                ((screen_width - new_game_text.get_width()) // 2,
                 (screen_height - new_game_text.get_height()) // 2 + 150))

    # updates the display
    pygame.display.flip()

    print('You Died!')


def display_player_stats(screen, player, font):
    """
        Display the player's health and ammo stats on the screen.

        Args:
            screen (pygame.Surface): The game screen.
            player (Player): The player character with health and ammo information.
            font (pygame.font.Font): The font used for text rendering.
    """
    # create the red background rectangle for the health bar
    red_rect = pygame.Rect(10, 10, 200, 20)

    # calculate the width of the green bar over the red based on player health percentage
    health_percentage = (player.health / player.max_health)
    green_width = int(health_percentage * 200)  # 200 is the width of the red bar

    # create the green rectangle to go over the red rectangle based on amount of health remaining
    green_rect = pygame.Rect(10, 10, green_width, 20)

    # draw the health bar
    pygame.draw.rect(screen, colors.RED, red_rect)
    pygame.draw.rect(screen, colors.GREEN, green_rect)

    # Display the character's health text over the health bar
    health_text = font.render(f"Health: {player.health}", True, colors.BLACK)
    screen.blit(health_text, (11, 9))  # Adjust the vertical position as needed

    # create black background bar for bullet amount
    black_rect = pygame.Rect(10, 35, 200, 20)

    # calculate the width of the yellow bullet bar over the black based on bullet percentage
    ammo_percentage = (player.gun.mag_ammo / player.gun.mag_size)
    yellow_width = int(ammo_percentage * 200)  # 200 is the width of the black bar

    # create the yellow rectangle to go over the black rectangle based on amount of ammo remaining
    yellow_rect = pygame.Rect(10, 35, yellow_width, 20)

    # draw the ammo bar
    # pygame.draw.rect(screen, colors.BLACK, black_rect)
    pygame.draw.rect(screen, colors.YELLOW, yellow_rect)

    # display the character's ammo text over the ammo bar
    ammo_text = font.render(f"Ammo: {player.gun.mag_ammo}", True, colors.BLACK)
    screen.blit(ammo_text, (11, 34))

    # display the remaining mags in the gun
    mag_text = font.render(f"Mags: {player.gun.mag_count}", True, colors.BLACK)
    screen.blit(mag_text, (10, 58))  # Adjust the vertical position as needed

    # this is causing the game to run extremely slow, need to explore different options
    # also need a different picture, was thinking a cartoon looking magazine of an ak-47
    
    # load the magazine image
    # mag_image = pygame.image.load('images/ammo_storage.png')  # Replace 'magazine.png' with the actual image file path
    # mag_image = pygame.transform.scale(mag_image, (50, 50))  # Adjust the size as needed
    #
    # # Display the remaining mags in the gun using the magazine image
    # mag_count = player.gun.mag_count
    # screen.blit(mag_image, (50, 58))  # Adjust the horizontal position and spacing as needed
