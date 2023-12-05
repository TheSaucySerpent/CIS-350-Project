import random
import pygame
import colors
import colors as c

# chooses random menu background
menu_background_options = ['images/menu_background' + str(i) + '.png' for i in range(1, 6)]
menu_background_selection = random.choice(menu_background_options)


class UI:
    """Class for the game's user interface and relevant menus that are displayed throughout the game."""

    def __init__(self, screen, screen_width, screen_height, font):
        """
        constructor for the user interface.

        Args:
            screen (pygame.display): The game screen itself.
            screen_width (int): The width of the game screen
            screen_height (int): The height of the game screen
            font (pygame.font.Font): The font we wish to use for relevant text.
        """
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font

    def display_startup_menu(self):
        """
        Display the startup menu with a random background.
        """
        # loads menu background
        menu_background = pygame.image.load(menu_background_selection)
        menu_background.convert()

        # scales background image to screen size
        menu_background = pygame.transform.scale(menu_background, (self.screen_width, self.screen_height))

        # creates bounding box for the image
        img_rect = menu_background.get_rect()
        img_rect.center = self.screen_width // 2, self.screen_height // 2

        # relevant text for the menu
        game_title = self.font.render('CIS 350 Project', True, c.WHITE)
        new_game_text = self.font.render('Press N for New Game', True, c.WHITE)
        continue_game_text = self.font.render('Press C to Load Saved Game', True, c.WHITE)

        # centers game title on menu
        title_rect = game_title.get_rect()
        title_rect.center = img_rect.center

        # places new game text under game title
        new_game_rect = new_game_text.get_rect()
        new_game_rect.center = (self.screen_width // 2, title_rect.bottom + 20)

        # places continue game text under new game text
        continue_game_rect = continue_game_text.get_rect()
        continue_game_rect.center = (self.screen_width // 2, new_game_rect.bottom + 20)

        # displays the menu
        self.screen.blit(menu_background, img_rect)
        self.screen.blit(game_title, title_rect)
        self.screen.blit(new_game_text, new_game_rect)
        self.screen.blit(continue_game_text, continue_game_rect)

        # updates the display
        pygame.display.flip()

    def display_death_menu(self):
        """
            Display the death menu with the death screen background image.
        """
        death_background = pygame.image.load("images/death_background.jpg")
        death_background.convert()

        # scales background image to screen size
        death_background = pygame.transform.scale(death_background, (self.screen_width, self.screen_height))

        # creates bounding box for the image
        img_rect = death_background.get_rect()
        img_rect.center = self.screen_width // 2, self.screen_height // 2

        # displays the death menu
        self.screen.blit(death_background, img_rect)

        # display new game text on death menu
        new_game_text = self.font.render("Press N to Start New Game", True, (255, 255, 255))
        self.screen.blit(new_game_text,
                         ((self.screen_width - new_game_text.get_width()) // 2,
                          (self.screen_height - new_game_text.get_height()) // 2 + 150))

        # updates the display
        pygame.display.flip()

        print('You Died!')

    def display_player_stats(self, player):
        """
            Display the player's health and ammo stats on the screen.
        """
        # create the red background rectangle for the health bar
        red_rect = pygame.Rect(10, 10, 200, 20)

        # calculate the width of the green bar over the red based on player health percentage
        health_percentage = (player.health / player.max_health)
        green_width = int(health_percentage * 200)  # 200 is the width of the red bar

        # create the green rectangle to go over the red rectangle based on amount of health remaining
        green_rect = pygame.Rect(10, 10, green_width, 20)

        # draw the health bar
        pygame.draw.rect(self.screen, colors.RED, red_rect)
        pygame.draw.rect(self.screen, colors.GREEN, green_rect)

        # Display the character's health text over the health bar
        health_text = self.font.render(f"Health: {player.health}", True, colors.BLACK)
        self.screen.blit(health_text, (11, 9))  # Adjust the vertical position as needed

        # create black background bar for bullet amount
        black_rect = pygame.Rect(10, 35, 200, 20)

        # calculate the width of the yellow bullet bar over the black based on bullet percentage
        if player.gun != 0:
            ammo_percentage = (player.gun.mag_ammo / player.gun.mag_size)
            yellow_width = int(ammo_percentage * 200)  # 200 is the width of the black bar
            player_gun_mag_ammo = player.gun.mag_ammo
            player_gun_mag_count = player.gun.mag_count
        else:
            yellow_width = 0
            player_gun_mag_ammo = 0
            player_gun_mag_count = 0

        # create the yellow rectangle to go over the black rectangle based on amount of ammo remaining
        yellow_rect = pygame.Rect(10, 35, yellow_width, 20)

        # draw the ammo bar
        # pygame.draw.rect(screen, colors.BLACK, black_rect)
        pygame.draw.rect(self.screen, colors.YELLOW, yellow_rect)

        # display the character's ammo text over the ammo bar
        ammo_text = self.font.render(f"Ammo: {player_gun_mag_ammo}", True, colors.BLACK)
        self.screen.blit(ammo_text, (11, 34))

        # display the remaining mags in the gun
        mag_text = self.font.render(f"Mags: {player_gun_mag_count}", True, colors.BLACK)
        self.screen.blit(mag_text, (10, 58))  # Adjust the vertical position as needed

        # this is causing the game to run extremely slow, need to explore different options
        # also need a different picture, was thinking a cartoon looking magazine of an ak-47

        # load the magazine image
        # mag_image = pygame.image.load('images/ammo_storage.png')  # Replace 'magazine.png' with the actual image file path
        # mag_image = pygame.transform.scale(mag_image, (50, 50))  # Adjust the size as needed
        #
        # # Display the remaining mags in the gun using the magazine image
        # mag_count = player.gun.mag_count
        # screen.blit(mag_image, (50, 58))  # Adjust the horizontal position and spacing as needed
    def display_player_inventory(self, player):
        # inventory_hotbar = pygame.image.load("images/inventory_hotbar.png")
        # inventory_hotbar.convert()
        #
        # inventory_hotbar = pygame.transform.scale(inventory_hotbar, (
        # inventory_hotbar.get_width() * .5, inventory_hotbar.get_height() * .5))
        #
        # img_rect = inventory_hotbar.get_rect()
        # img_rect.center = self.screen_width // 2, self.screen_height - 25
        #
        # # displays the inventory_hotbar
        # self.screen.blit(inventory_hotbar, img_rect)

        # Display inventory title
        # inventory_title = self.font.render("Player Inventory", True, colors.WHITE)
        # self.screen.blit(inventory_title, (self.screen_width // 2, self.screen_height - 25))

        # starting x-coordinate
        x_coordinate = 10
        y_coordinate = 85

        gun_image = pygame.transform.scale(player.gun.image, (player.gun.image.get_width() / 2,
                                                              player.gun.image.get_height() / 2))
        self.screen.blit(gun_image, (x_coordinate, y_coordinate))
        x_coordinate += 35

        # Display each item in the inventory
        for item in player.inventory:
            item_image = pygame.transform.scale(item.image, (item.image.get_width(),
                                                             item.image.get_height() * .7))

            self.screen.blit(item_image, (x_coordinate, y_coordinate - 10))

            x_coordinate += 40

        # Update the display
        pygame.display.flip()
