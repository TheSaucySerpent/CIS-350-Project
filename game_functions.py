import pygame
import glob_var
import colors
import UI


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

        # This is just to make it easier to read in the running loop.
        self.player = glob_var.player
        self.obj = glob_var.obj
        self.enemies = glob_var.enemies
        self.room = glob_var.Room
        self.current_room = glob_var.r1
        self.game_over = False

    def run_game(self):
        """
        Runs the game loop.
        """

        keys = pygame.key.get_pressed()
        if not self.game_over:
            # If 'r' is pressed, calls the reload function of the player's currently equipped gun.
            if keys[pygame.K_r]:
                self.player.gun.reload()
            # If the spacebar is pressed, makes sure enough time has passed since last dodge, then dodges if allowed.
            # Otherwise, calls the player's move function.
            if keys[pygame.K_SPACE]:
                current_time = pygame.time.get_ticks()
                if current_time - self.player.last_dodge > 1000:
                    self.player.move(keys, 200, True)
                    self.player.last_dodge = current_time
                else:
                    self.player.move(keys, 0)
            else:
                self.player.move(keys, 0)

            # If the left mouse button is clicked, calls the player's weapon's attack function.
            if pygame.mouse.get_pressed()[0]:
                if self.player.gun != 0:
                    self.player.gun.attack()
                else:
                    print("You don't got a gun!")

            # Calls the collision function of every object
            for i in glob_var.objs:
                i.collision()

            # Calls the function that makes items bounce
            for i in self.current_room.items:
                i.bounce()
            self.player.pick_up(self.current_room)

            # Calls enemy move_toward_character function
            for enemy in self.current_room.enemies:
                enemy.move_towards_character()

                # Death Message/Game Over
                if self.player.health == 0:
                    UI.display_death_menu(self.screen, self.screen_width, self.screen_height, self.font)
                    self.game_over = True

            self.render_assets()

            # update the display
            pygame.display.update()

    def render_assets(self):
        # draw background
        self.screen.blit(self.current_room.background, (0, 0))
        self.current_room.draw(self.screen)

        # Draws the player and stats
        glob_var.player.draw(self.screen)
        UI.display_player_stats(self.screen, self.player, self.font)

        # Draws projectiles
        for g in glob_var.guns:
            for p in g.projectiles:
                p.move()
                pygame.draw.rect(self.screen, colors.YELLOW, (p.x, p.y, p.width, p.height))
            g.update_projectiles()

        # draws enemies and removes them from the room if they die
        for enemy in self.current_room.enemies:
            if enemy.health > 0:
                self.screen.blit(enemy.image, (enemy.x, enemy.y))
            else:
                self.current_room.enemies.remove(enemy)

    def resize_assets(self, new_width, new_height):
        # Update the screen dimensions
        self.screen_width = new_width
        self.screen_height = new_height

        # Update the game screen with the new size
        self.screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)

        # Calculate scaling factors based on the new and original dimensions
        width_scale = new_width / self.screen_width
        height_scale = new_height / self.screen_height

        # Update positions, sizes, and scales of game elements
        # For example, update player position and size
        self.player.x *= width_scale
        self.player.y *= height_scale
        self.player.width *= width_scale
        self.player.height *= height_scale

        # Update enemy positions, sizes, and scales (if you have enemies)

        # Update UI elements like text and font size
        self.font = pygame.font.Font(None, int(36 * width_scale))

        # You may need to call other functions to adjust assets in your game.

