import pygame
import UI
import game_functions


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

    game = game_functions.Game(screen, screen_width, screen_height, font)

    # Display the title menu
    UI.display_startup_menu(screen, screen_width, screen_height, font)

    while program_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                program_running = False
            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.size
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                if game is not None:
                    game.resize_assets(screen_width, screen_height)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    program_running = False
                elif event.key == pygame.K_n:
                    # Create the game instance only once
                    if game is None:
                        game = game_functions.Game(screen, screen_width, screen_height, font)
                    game_in_progress = True

        if game_in_progress:
            # Run the game
            game.run_game()
        else:
            # Display the title menu
            UI.display_startup_menu(screen, screen_width, screen_height, font)


if __name__ == '__main__':
    main()
