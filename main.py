import pygame
import UI
import game_functions


def main():
    # initialize pygame
    pygame.init()

    # create the screen
    screen_width = 1200
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height))

    # set font for text
    font = pygame.font.Font(None, 36)

    # flags for running the program and the game itself
    program_running = True
    game_in_progress = False

    game = game_functions.Game(screen, screen_width, screen_height, font)

    # display the title menu
    UI.display_menu(screen, screen_width, screen_height, font)

    while program_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                program_running = False
            # elif event.type == pygame.FULLSCREEN:
            #     size = pygame.display.Info()
            #     w,h = size.current_w,size.current_h
            #     UI.display_menu(screen, w, h, font)

            # to register key presses
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    program_running = False
                elif event.key == pygame.K_n:
                    # starts the game
                    game_in_progress = True

        if game_in_progress:
            game.run_game()


if __name__ == '__main__':
    main()