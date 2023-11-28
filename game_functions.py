import pickle
import pygame
import glob_var
import colors
import UI


class Game:
    """
    Class used for all game functions. run_game function called in main.
    """

    def __init__(self, screen, screen_width, screen_height, user_interface, font):
        """
        Initialize the game.

        Args:
            screen: The game screen.
            screen_width (int): The width of the screen.
            screen_height (int): The height of the screen.
            user_interface (UI): The user interface of the game.
            font: The font used for text.
        """
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.user_interface = user_interface
        self.font = font

        self.player = None
        self.obj = None
        self.enemies = None
        self.room = None
        self.current_room = None
        self.game_over = True

        self.prev_screen_width = screen_width
        self.prev_screen_height = screen_height

        self.setup_game()

    def setup_game(self):
        self.player = glob_var.player
        self.obj = glob_var.obj
        self.enemies = glob_var.enemies
        self.room = glob_var.Room
        self.current_room = glob_var.r1
        self.game_over = False

    def run_game(self):
        ''' Runs the game loop. '''

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
                    self.player.move(self.screen_width, self.screen_height, keys, 200, True)
                    self.player.last_dodge = current_time
                else:
                    self.player.move(self.screen_width, self.screen_height, keys, 0)
            else:
                self.player.move(self.screen_width, self.screen_height, keys, 0)

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
                enemy.move_towards_character(self.screen_width, self.screen_height)

            self.render_assets()

            # Death Message/Game Over
            if self.player.health == 0:
                self.user_interface.display_death_menu()
                self.game_over = True

            # update the display
            pygame.display.update()

    def render_assets(self):
        self.screen.blit(self.current_room.background, (0, 0))
        # draw background
        self.current_room.draw(self.screen)

        # Draws the player and stats
        glob_var.player.draw(self.screen)
        self.user_interface.display_player_stats(self.player)

        # Draws projectiles
        for g in glob_var.guns:
            for p in g.projectiles:
                p.move()
                pygame.draw.rect(self.screen, colors.YELLOW, (p.x, p.y, p.width, p.height))
            g.update_projectiles(self.screen_width, self.screen_height)

        # draws enemies and removes them from the room if they die
        for enemy in self.current_room.enemies:
            if enemy.health > 0:
                self.screen.blit(enemy.image, (enemy.x, enemy.y))
            else:
                self.current_room.enemies.remove(enemy)

    def save_game_state(self):
        game_state = {
            'player_x': self.player.x,
            'player_y': self.player.y,
            'player_health': self.player.health,
            'ammo_count': self.player.gun.mag_ammo,
            'mag_count': self.player.gun.mag_count,
            'room_items': [],
            'room_enemies': [],
        }

        for item in self.current_room.items:
            item_info = {
                'position': (item.x, item.y),
                'width': item.width,
                'height': item.height,
                'image_path': item.image_path,
            }
            game_state['room_items'].append(item_info)

            # Extract necessary information about enemies in the room
        for enemy in self.current_room.enemies:
            enemy_info = {
                'name': enemy.name,
                'type': type(enemy),
                'position': (enemy.x, enemy.y),
                'health': enemy.health,
                # Add other essential information...
            }
            game_state['room_enemies'].append(enemy_info)

        with open('game_save.pkl', 'wb') as file:
            pickle.dump(game_state, file)

        print('Game Saved')
