import os
import pickle
import pygame
import glob_var
import colors
import UI
import random
from item import Item


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
        self.doors = None

        self.prev_screen_width = screen_width
        self.prev_screen_height = screen_height

        self.setup_game()
        self.crosshair = pygame.image.load("images/crosshair.png")

    def setup_game(self):
        '''
        Creates the starting variables of the game
        player = the main character used everywhere
        obj = the object class
        enemies = list of starting enemies
        room = Room class
        current_room = Starting room
        game_over = Boolean to determine if the game is over

        '''
        self.player = glob_var.player
        self.obj = glob_var.obj
        self.enemies = glob_var.enemies
        self.room = glob_var.Room
        self.current_room = glob_var.r1
        self.game_over = False

    def run_game(self):
        ''' Runs the game loop. '''

        # Make the cursor invisible so a custom cursor can be used
        pygame.mouse.set_visible(False)

        # Create a list of keys that are pressed
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

            # Call the collision function of every object
            for i in self.current_room.objects:
                i.collision()

            # Call the function that makes items bounce
            for i in self.current_room.items:
                i.bounce()
            # Weird function that goes through every item in the current room to see if there's collision with player
            self.player.pick_up(self.current_room)

            # Looks for medkits and uses them if found
            for i in self.player.inventory:
                if i.name == 'Medkit':
                    self.player.inventory.remove(i)
                    self.player.heal(25)

            # Calls enemy move_toward_character function
            for enemy in self.current_room.enemies:
                enemy.move_towards_character(self.screen_width, self.screen_height)

            # Call the render assets function to render all assets in correct positions
            self.render_assets()

            # If there's a door the player is colliding with and the player has a key and presses 'f':
            if self.current_room.door:
                if self.current_room.door.collision() and keys[pygame.K_f] and glob_var.key in glob_var.player.inventory:
                    # Go to the next room, teleport player to that room's starting location, and remove the key from player's inventory
                    self.current_room = self.current_room.next_room
                    glob_var.cur_room = self.current_room
                    glob_var.player.x = self.current_room.starting_x
                    glob_var.player.y = self.current_room.starting_y
                    glob_var.player.inventory.remove(glob_var.key)

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

        # Get current mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Adjust the position to center the crosshair
        crosshair_x = mouse_x - self.crosshair.get_width() // 2
        crosshair_y = mouse_y - self.crosshair.get_height() // 2
        # Draw crosshair on the screen
        self.screen.blit(self.crosshair, (crosshair_x, crosshair_y))

        # Draws the player and stats
        glob_var.player.draw(self.screen)
        self.user_interface.display_player_stats(self.player)

        # Draws the current room's door
        if self.current_room.door:
            self.screen.blit(self.current_room.door.image, (self.current_room.door.x, self.current_room.door.y))

        # Draws projectiles
        for g in glob_var.guns:
            for p in g.projectiles:
                p.move()
                pygame.draw.rect(self.screen, colors.YELLOW, (p.x, p.y, p.width, p.height))
            g.update_projectiles(self.screen_width, self.screen_height)

        # draws enemies and removes them from the room if they die
        if len(self.current_room.enemies) > 0:
            for enemy in self.current_room.enemies:
                if enemy.health > 0:
                    self.screen.blit(enemy.image, (enemy.x, enemy.y))
                else:
                    # When an enemy dies, if it's the last enemy and it's not on the final level:
                    if len(self.current_room.enemies) == 1 and self.current_room != glob_var.r6:
                        # Drop a key at the last enemy's death coords
                        glob_var.key.x = self.current_room.enemies[0].x
                        glob_var.key.original_y = self.current_room.enemies[0].y
                        glob_var.key.y = self.current_room.enemies[0].y
                        self.current_room.add_item(glob_var.key)
                        print("Key dropped!")
                    # Else, everytime any enemy besides the last enemy
                    else:
                        # Roll a die and
                        luck = random.randint(0, 5)
                        # If you roll lucky and not on last room:
                        if luck == 1 and self.current_room != glob_var.r6 and len(self.current_room.items) == 0:
                            # Drop a medkit at enemy death coords
                            glob_var.medkit.x = enemy.x
                            glob_var.medkit.original_y = enemy.y
                            glob_var.medkit.y = enemy.y
                            self.current_room.add_item(glob_var.medkit)
                            print("Medkit Dropped!")
                    # 'Kill' enemy
                    self.current_room.enemies.remove(enemy)

    def save_game_state(self):
        game_state = {
            'player_x': self.player.x,
            'player_y': self.player.y,
            'player_health': self.player.health,
            'ammo_count': self.player.gun.mag_ammo,
            'mag_count': self.player.gun.mag_count,
            'player_inventory': [],
            'room_items': [],
            'room_enemies': [],
            'room_objects': [],
        }

        for item in self.player.inventory:
            item_info = {
                'name': item.name,
                'position': (item.x, item.y),
                'width': item.width,
                'height': item.height,
                'image_path': item.image_path,
            }
            game_state['player_inventory'].append(item_info)

        for item in self.current_room.items:
            item_info = {
                'name': item.name,
                'position': (item.x, item.y),
                'width': item.width,
                'height': item.height,
                'image_path': item.image_path,
            }
            game_state['room_items'].append(item_info)

        for enemy in self.current_room.enemies:
            enemy_info = {
                'name': enemy.name,
                'type': type(enemy),
                'position': (enemy.x, enemy.y),
                'health': enemy.health,
            }
            game_state['room_enemies'].append(enemy_info)

        for obj in self.current_room.objects:
            obj_info = {
                'position': (obj.x, obj.y),
                'dimensions': (obj.width, obj.height),
                'health': obj.health,
                'image_path': [],
                'type': type(obj)
            }

            if obj_info['type'] == glob_var.Door:
                obj_info['image_path'] = obj.image_path

            game_state['room_objects'].append(obj_info)

        with open('game_save.pkl', 'wb') as file:
            pickle.dump(game_state, file)

        print('Game Saved')

    def load_game_state(self):
        if os.path.isfile('game_save.pkl'):
            with open('game_save.pkl', 'rb') as file:
                game_state = pickle.load(file)

        # Clear all preset objects of the game
        self.current_room.objects.clear()
        self.current_room.enemies.clear()
        self.current_room.items.clear()

        # Restore player state
        self.player.x = game_state['player_x']
        self.player.y = game_state['player_y']
        self.player.health = game_state['player_health']
        self.player.gun.mag_ammo = game_state['ammo_count']
        self.player.gun.mag_count = game_state['mag_count']
        room_items = []

        for item_info in game_state['player_inventory']:
            item = Item(item_info['name'], item_info['position'][0], item_info['position'][1],
                        item_info['width'], item_info['height'], item_info['image_path'])
            self.player.inventory.append(item)

        for item_info in game_state['room_items']:
            item = Item(item_info['name'], item_info['position'][0], item_info['position'][1],
                        item_info['width'], item_info['height'], item_info['image_path'])
            room_items.append(item)

        room_enemies = []
        for enemy_info in game_state['room_enemies']:
            enemy = enemy_info['type'](enemy_info['name'], enemy_info['position'][0],
                                       enemy_info['position'][1])
            enemy.health = enemy_info['health']

            room_enemies.append(enemy)
            glob_var.enemies.append(enemy)
            glob_var.entities.append(enemy)

        for obj_info in game_state['room_objects']:
            obj = obj_info['type'](obj_info['position'][0], obj_info['position'][1],
                                   obj_info['dimensions'][0],
                                   obj_info['dimensions'][1], obj_info['health'],
                                   obj_info['image_path'])
            self.current_room.objects.append(obj)

        self.current_room.items = room_items
        self.current_room.enemies = room_enemies
