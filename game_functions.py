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
            for i in self.current_room.objects:
                i.collision()

            # Calls the function that makes items bounce
            for i in self.current_room.items:
                i.bounce()
            self.player.pick_up(self.current_room)

            # Looks for medkits and uses them if found
            for i in self.player.inventory:
                if i.name == 'Medkit':
                    self.player.inventory.remove(i)
                    self.player.health += 25

            # Calls enemy move_toward_character function
            for enemy in self.current_room.enemies:
                enemy.move_towards_character(self.screen_width, self.screen_height)

            self.render_assets()

            if self.current_room.door:
                if self.current_room.door.collision() and keys[pygame.K_f] and glob_var.key in glob_var.player.inventory:
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

        # Draws the player and stats
        glob_var.player.draw(self.screen)
        self.user_interface.display_player_stats(self.player)
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
                    if len(self.current_room.enemies) == 1 and self.current_room != glob_var.r6:
                        glob_var.key.x = self.current_room.enemies[0].x
                        glob_var.key.original_y = self.current_room.enemies[0].y
                        glob_var.key.y = self.current_room.enemies[0].y
                        self.current_room.add_item(glob_var.key)
                        print("Key dropped!")
                    else:
                        luck = random.randint(0, 5)
                        if luck == 1:
                            glob_var.medkit.x = enemy.x
                            glob_var.medkit.original_y = enemy.y
                            glob_var.medkit.y = enemy.y
                            self.current_room.add_item(glob_var.medkit)
                            print("Medkit Dropped!")
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
