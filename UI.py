import pygame

import colors
import colors as c


def display_menu(screen, screen_width, screen_height, font):
    # loads menu background
    menu_img = pygame.image.load('images/menu_background2.jpg')
    menu_img.convert()

    # relevant text for the menu
    game_title = font.render('Example Game Title', True, c.WHITE)

    # creates bounding box for the image
    img_rect = menu_img.get_rect()
    img_rect.center = screen_width // 2, screen_height // 2

    # calculate the position to center the text on the image
    text_rect = game_title.get_rect()
    text_rect.center = img_rect.center

    # displays the menu image with the text
    screen.blit(menu_img, img_rect)
    screen.blit(game_title, text_rect)

    pygame.display.update()


def display_player_stats(screen, player, font):
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
    pygame.draw.rect(screen, colors.BLACK, black_rect)
    pygame.draw.rect(screen, colors.YELLOW, yellow_rect)

    # display the character's ammo text over the ammo bar
    ammo_text = font.render(f"Ammo: {player.gun.mag_ammo}", True, colors.BLACK)
    screen.blit(ammo_text, (11, 34))

    # display the remaining mags in the gun
    mag_text = font.render(f"Mags: {player.gun.mag_count}", True, (255, 255, 255))
    screen.blit(mag_text, (10, 58))  # Adjust the vertical position as needed

    # this is causing the game to run extremely slow, need to explore different options
    # also need a different picture, was thinking a cartoon looking magazine of an ak-47
    
    # load the magazine image
    # mag_image = pygame.image.load('ammo_storage.png')  # Replace 'magazine.png' with the actual image file path
    # mag_image = pygame.transform.scale(mag_image, (50, 50))  # Adjust the size as needed
    #
    # # Display the remaining mags in the gun using the magazine image
    # mag_count = player.gun.mag_count
    # screen.blit(mag_image, (50, 58))  # Adjust the horizontal position and spacing as needed
