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

    # Initialize game
    game = None

    # Initialize user interface
    user_interface = UI.UI(screen, screen_width, screen_height, font)

    # Core program loop
    while program_running:
        # Handles events within the game
        for event in pygame.event.get():
            # Terminates program if corner X is clicked
            if event.type == pygame.QUIT:
                program_running = False
            # Resizes screen to fill resized window
            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.size
            # Handles keyboard input
            elif event.type == pygame.KEYDOWN:
                # Terminates program if esc is pressed
                if event.key == pygame.K_ESCAPE:
                    program_running = False
                # Starts new game if N is pressed
                elif event.key == pygame.K_n:
                    # Ensures a new game can be created only when game is None
                    if game is None:
                        game = game_functions.Game(screen, screen_width, screen_height, user_interface, font)
                    game_in_progress = True

        if game_in_progress:
            # Run the game
            game.run_game()
        else:
            # Display the title menu
            user_interface.display_startup_menu()


if __name__ == '__main__':
    main()