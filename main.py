import pygame
import UI
import game_functions


def main():
    pygame.init()

    screen_width = 1200
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

    font = pygame.font.Font(None, 36)

    program_running = True
    game_in_progress = False

    game = game_functions.Game(screen, screen_width, screen_height, font)

    UI.display_menu(screen, screen_width, screen_height, font)

    while program_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                program_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    program_running = False
                elif event.key == pygame.K_n:
                    game_in_progress = True
            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.size
                if not game_in_progress:
                    UI.display_menu(screen, screen_width, screen_height, font)
                else:
                    # need to change this so that resizing the game itself works
                    print('Game should expand')

        if game_in_progress:
            game.run_game()


if __name__ == '__main__':
    main()
