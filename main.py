import os

import pygame
import UI
import game_functions
import pickle

import glob_var
from enemy import Default, Tank, Runner
from item import Item


def main():
    """
    The main function that initializes the game, opens the intro screen, and runs the game loop.

    It initializes the pygame library, creates the game screen, and sets up game-related objects.
    It manages the game's main loop.
    """

    # Initialize pygame
    pygame.init()

    # Create the screen
    screen_width = 1200
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    # Set game window title
    pygame.display.set_caption('CIS 350 DEMO')

    # Set the font for text
    font = pygame.font.Font(None, 36)

    # Flags for running the program and the game itself
    program_running = True
    game_in_progress = False

    # Initialize game
    game = None

    # Initialize user interface
    user_interface = UI.UI(screen, screen_width, screen_height, font)

    # File to store saved game
    save_file = 'game_save.pkl'

    # Core program loop
    while program_running:
        # Handles events within the game
        for event in pygame.event.get():
            # Terminates program if corner X is clicked
            if event.type == pygame.QUIT:
                program_running = False
            # Resizes screen to fill resized window
            elif event.type == pygame.VIDEORESIZE:
                user_interface.screen_width = event.w
                user_interface.screen_height = event.h
                if game is not None:
                    game.prev_screen_width = screen_width
                    game.prev_screen_height = screen_height
                    game.screen_width = event.w
                    game.screen_height = event.h
                    game.current_room.scale(game.prev_screen_width, game.prev_screen_height, game.screen_width, game.screen_height)
                else:
                    screen_width, screen_height = event.w, event.h
            # Handles keyboard input
            elif event.type == pygame.KEYDOWN:
                # Terminates program if esc is pressed
                if event.key == pygame.K_ESCAPE:
                    program_running = False
                    if game is not None:
                        game.save_game_state()
                # Starts new game if N is pressed
                elif event.key == pygame.K_n:
                    # Ensures a new game can be created only when game is None
                    if game is None:
                        game = game_functions.Game(screen, screen_width, screen_height, user_interface, font)
                    game_in_progress = True
                elif event.key == pygame.K_c and game is None:
                    if os.path.isfile(save_file):
                        with open('game_save.pkl', 'rb') as file:
                            game_state = pickle.load(file)

                        # Create a new Game object
                        game = game_functions.Game(screen, screen_width, screen_height, user_interface, font)

                        # Restore player state
                        game.player.x = game_state['player_x']
                        game.player.y = game_state['player_y']
                        game.player.health = game_state['player_health']
                        game.player.gun.mag_ammo = game_state['ammo_count']
                        game.player.gun.mag_count = game_state['mag_count']
                        room_items = []

                        for item_info in game_state['player_inventory']:
                            item = Item(item_info['name'], item_info['position'][0], item_info['position'][1], item_info['width'], item_info['height'], item_info['image_path'])
                            game.player.inventory.append(item)

                        for item_info in game_state['room_items']:
                            item = Item(item_info['name'], item_info['position'][0], item_info['position'][1], item_info['width'], item_info['height'], item_info['image_path'])
                            room_items.append(item)

                        room_enemies = []
                        for enemy_info in game_state['room_enemies']:
                            enemy = enemy_info['type'](enemy_info['name'], enemy_info['position'][0], enemy_info['position'][1])
                            enemy.health = enemy_info['health']

                            room_enemies.append(enemy)
                            glob_var.enemies.append(enemy)
                            glob_var.entities.append(enemy)

                        for obj_info in game_state['room_objects']:
                            obj = obj_info['type'](obj_info['position'][0], obj_info['position'][1],
                                                   obj_info['dimensions'][0],
                                                   obj_info['dimensions'][1], obj_info['health'],
                                                   obj_info['image_path'])
                            game.current_room.objects.append(obj)

                        game.current_room.items = room_items
                        game.current_room.enemies = room_enemies

                        game_in_progress = True

        if game_in_progress:
            # Run the game
            game.run_game()
        else:
            # Display the title menu
            user_interface.display_startup_menu()


if __name__ == '__main__':
    main()