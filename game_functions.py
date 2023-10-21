import pygame
import glob_var
import colors
import UI

# This is just to make it easier to read in the running loop.
player = glob_var.player
obj = glob_var.obj
enemies = glob_var.enemies
room = glob_var.Room

current_room = glob_var.r1


class Game:
    """
    Class used for all game functions. run_game function called in main.
    """
    def __init__(self, screen, screen_width, screen_height, font):
        """
        Initialize the game.

        Args:
            screen: The game screen.
            screen_width (int): The width of the screen.
            screen_height (int): The height of the screen.
            font: The font used for text.
        """
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = font

    def run_game(self):
        """
        Runs the game loop.
        """
        game_over = False
        self.screen.blit(current_room.background, (0, 0))  # to draw background
        current_room.draw(self.screen)

        keys = pygame.key.get_pressed()
        if not game_over:
            #If 'r' is pressed, calls the reload function of the player's currently equipped gun.
            if keys[pygame.K_r]:
                player.gun.reload()
            #If the spacebar is pressed, makes sure enough time has passed since last dodge, then dodges if allowed.
            #Otherwise, calls the player's move function.
            if keys[pygame.K_SPACE]:
                current_time = pygame.time.get_ticks()
                if current_time - player.last_dodge > 1000:
                    player.move(keys, 200, True)
                    player.last_dodge = current_time
                else:
                    player.move(keys, 0)
            else:
                player.move(keys, 0)

            # If the left mouse button is clicked, calls the player's weapon's attack function.
            if pygame.mouse.get_pressed()[0]:
                if player.gun != 0:
                    player.gun.attack()
                else:
                    print("You don't got a gun!")

        # Draws the player and stats
        glob_var.player.draw(self.screen)
        UI.display_player_stats(self.screen, player, self.font)

        # Calls the collision function of every object
        for i in glob_var.objs:
            i.collision()

        # Calls the function that makes items bounce
        for i in current_room.items:
            i.bounce()
        player.pick_up(current_room)

        # Draws projectiles
        for g in glob_var.guns:
            for p in g.projectiles:
                p.move()
                pygame.draw.rect(self.screen, colors.YELLOW, (p.x, p.y, p.width, p.height))
            g.update_projectiles()

        # Calls enemy move_toward_character function, draws enemies, and removes them if they die
        for enemy in current_room.enemies:
            enemy.move_towards_character()

            if enemy.health > 0:
                self.screen.blit(enemy.image, (enemy.x, enemy.y))
            else:
                current_room.enemies.remove(enemy)

            # Death Message/Game Over
            if player.health == 0:
                ded_text = self.font.render(f"You Died.", True, (255, 0, 0))
                self.screen.blit(ded_text,
                                 ((self.screen_width - ded_text.get_width()) // 2,
                                  (self.screen_height - ded_text.get_height()) // 2))
                game_over = True

        # update the display
        pygame.display.update()
