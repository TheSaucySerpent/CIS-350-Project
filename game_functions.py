import os
import pickle
import pygame
import colors
import UI
import random

from character import Character
from enemy import Default, Tank, Runner, Enemy
from item import Item
from object import Object, Door
from room import Room
from weapons import Weapon, Shotgun


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
        self.current_room = None
        self.game_over = False
        self.doors = None
        self.room = None
        self.guns = None
        self.key = None
        self.medkit = None
        self.items = None
        self.r6 = None
        self.rooms = None

        self.prev_screen_width = screen_width
        self.prev_screen_height = screen_height

        self.setup_game()
        self.crosshair = pygame.image.load("images/crosshair.png")

    def setup_game(self):
        """
        Creates the starting variables of the game
        player = the main character used everywhere
        obj = the object class
        enemies = list of starting enemies
        room = Room class
        current_room = Starting room
        game_over = Boolean to determine if the game is over

        """
        self.player = Character(name="Player", x=100, y=100, width=50, height=50, speed=1, health=100, armor=50, gun=0,
                                image_path="images/white_square.png")

        # Weapon Instances
        pistol = Weapon(name="Pistol", damage=10, proj_speed=1, attack_speed=3, mag_size=9, mag_count=5,
                        reload_speed=10,
                        owner=self.player, x=50, y=50, width=50, height=50, screen_width=self.screen_width,
                        screen_height=self.screen_height, image_path='images/pistol.png')
        ar = Weapon(name="Assault Rifle", damage=15, proj_speed=1.25, attack_speed=5, mag_size=30, mag_count=2,
                    reload_speed=20, owner=self.player, x=600, y=350, width=100, height=50,
                    screen_width=self.screen_width,
                    screen_height=self.screen_height, image_path='images/ar.png')
        dev_gun = Weapon("God's Draco", 10, 2, 100, 10000, 1, 10, self.player, x=200, y=300, width=100, height=50,
                         screen_width=self.screen_width, screen_height=self.screen_height,
                         image_path='images/minigun.png')
        # Shotgun Instances
        shotgun = Shotgun(name="Pump Shotgun", damage=10, proj_speed=1, attack_speed=2, mag_size=8, mag_count=2,
                          reload_speed=15, owner=self.player, spread=25, proj_number=8, x=1050, y=600, width=100,
                          height=50, screen_width=self.screen_width, screen_height=self.screen_height,
                          image_path='images/shotgun.png')
        dev_shotgun = Shotgun("God's Sawed-Off", 50, 5, 10, 1000, 1, 10, self.player, 20, 30, x=50, y=50, width=50,
                              height=50, screen_width=self.screen_width, screen_height=self.screen_height,
                              image_path=None)

        self.guns = [pistol, ar, dev_gun, shotgun, dev_shotgun]

        self.player.gun = pistol

        enemy1 = Default(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600), player=self.player)
        enemy2 = Default(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600), player=self.player)
        enemy3 = Default(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600), player=self.player)
        enemy4 = Tank(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600), player=self.player)
        enemy5 = Runner(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600), player=self.player)
        enemy6 = Runner(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600), player=self.player)
        # List of all enemies for drawing and player tracking
        enemies = [enemy1, enemy2, enemy3, enemy4, enemy5, enemy6]

        obj = Object(x=200, y=100, width=50, height=150, health=1000)
        obj2 = Object(x=200, y=100, width=700, height=50, health=1000)
        obj3 = Object(x=850, y=100, width=50, height=150, health=1000)
        obj4 = Object(x=200, y=550, width=700, height=50, health=1000)
        obj5 = Object(x=200, y=500, width=50, height=100, health=1000)
        obj6 = Object(x=850, y=500, width=50, height=100, health=1000)
        r1door1 = Door(x=1100, y=300, width=100, height=100, health=1000, image_path='images/door.png')
        # Object list, used for drawing and collision
        r1objs = [obj, obj2, obj3, obj4, obj5, obj6, r1door1]

        r1 = Room('r1', background_path="images/Tile Resized.jpg", screen_width=self.screen_width,
                  screen_height=self.screen_height)

        self.current_room = r1

        # Separate list including all enemies and main character, used for object collision
        self.current_room.entities = [self.player] + enemies

        # Adds all enemies/entities to the room
        for i in enemies:
            self.current_room.add_enemy(i)

        # Adds all objects to the room
        for i in r1objs:
            self.current_room.add_object(i)

        # Adds door to room
        self.current_room.door = r1door1

        # Adds gun to room
        self.current_room.add_item(ar)

        # Items are universal, meaning there's only one instance of them that is reused and reset when called.
        self.key = Item("Key", 950, 100, 75, 75, self.screen_width, self.screen_height, "images/golden key.png")
        self.medkit = Item("Medkit", 950, 100, 50, 50, self.screen_width, self.screen_height, "images/medkit.png")

        self.items = [self.key, self.medkit]

        self.current_room.enemies = enemies
        self.room = self.current_room

        self.game_over = False

        '''
        Here is everything added to Room 2:
        6 enemies
        5 objects
        Door
        '''

        r2enemy1 = Default(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600), player=self.player)
        r2enemy2 = Default(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600), player=self.player)
        r2enemy3 = Default(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600), player=self.player)
        r2enemy4 = Tank(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600), player=self.player)
        r2enemy5 = Runner(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600), player=self.player)
        r2enemy6 = Runner(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600), player=self.player)
        r2enemies = [r2enemy1, r2enemy2, r2enemy3, r2enemy4, r2enemy5, r2enemy6]
        r2entities = [self.player]

        for i in r2enemies:
            r2entities.append(i)

        r2obj = Object(x=150, y=100, width=50, height=500, health=1000)
        r2obj2 = Object(x=150, y=600, width=700, height=50, health=1000)
        r2obj3 = Object(x=350, y=50, width=600, height=50, health=1000)
        r2obj4 = Object(x=950, y=50, width=50, height=500, health=1000)
        r2obj5 = Object(x=500, y=300, width=100, height=100, health=1000)
        r2objs = [r2obj, r2obj2, r2obj3, r2obj4, r2obj5]
        r2door = Door(x=1100, y=300, width=100, height=100, health=1000, image_path='images/door.png')

        r2 = Room('r2', background_path="images/Tile Resized.jpg", screen_width=self.screen_width,
                  screen_height=self.screen_height)

        # Determines where the player spawns in the next level
        r2.starting_x = 100
        r2.starting_y = 100
        r2.enemies = r2enemies
        r2.entities = r2entities
        r2.objects = r2objs
        r2.door = r2door
        # Make the previous room's door lead to this room
        self.current_room.next_room = r2

        '''
        Here is everything added to Room 3:
        6 enemies
        6 objects
        Door
        Shotgun
        '''
        r3enemy1 = Default(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600), player=self.player)
        r3enemy2 = Default(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600), player=self.player)
        r3enemy3 = Default(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600), player=self.player)
        r3enemy4 = Tank(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600), player=self.player)
        r3enemy5 = Runner(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600), player=self.player)
        r3enemy6 = Runner(name='enemy', x=random.randint(400, 800), y=random.randint(200, 600), player=self.player)
        r3enemies = [r3enemy1, r3enemy2, r3enemy3, r3enemy4, r3enemy5, r3enemy6]
        r3entities = [self.player]
        for i in r3enemies:
            r3entities.append(i)

        r3obj = Object(x=1000, y=150, width=50, height=400, health=1000)
        r3obj2 = Object(x=200, y=150, width=800, height=50, health=1000)
        r3obj3 = Object(x=250, y=300, width=75, height=75, health=1000)
        r3obj4 = Object(x=150, y=550, width=75, height=75, health=1000)
        r3obj5 = Object(x=500, y=450, width=75, height=75, health=1000)
        r3obj6 = Object(x=700, y=550, width=75, height=75, health=1000)
        r3objs = [r3obj, r3obj2, r3obj3, r3obj4, r3obj5, r3obj6]
        r3door = Door(x=1100, y=300, width=100, height=100, health=1000, image_path='images/door.png')

        r3 = Room('r3', background_path="images/Tile Resized.jpg", screen_width=self.screen_width,
                  screen_height=self.screen_height)
        r3.starting_x = 100
        r3.starting_y = 100
        r3.enemies = r3enemies
        r3.entities = r3entities
        r3.objects = r3objs
        r3.add_item(shotgun)
        r3.door = r3door
        r2.next_room = r3

        '''
        Here is everything added to Room 4:
        Boss Enemy
        2 Minions
        Door
        '''
        # r4enemy1 = Enemy(name='enemy', x=450, y=700, width=50, height=75, speed=.5, health=50, armor=0, gun=0,
        # character=player, damage=20, image_path='images/waterEnemy1.png')
        r4enemy2 = Enemy(name='enemy', x=450, y=400, width=50, height=75, speed=.5, health=50, armor=0, gun=0,
                         character=self.player,
                         damage=20, image_path='images/waterEnemy1.png')
        r4enemy3 = Enemy(name='enemy', x=450, y=500, width=50, height=75, speed=.5, health=50, armor=0, gun=0,
                         character=self.player,
                         damage=20, image_path='images/waterEnemy1.png')
        boss = Enemy(name='Boss', x=550, y=300, width=200, height=200, speed=.07, health=1000, armor=0, gun=0,
                     character=self.player,
                     damage=50, image_path='images/bossGolem.png')

        r4 = Room('r4', background_path="images/ocean.png", screen_width=self.screen_width, screen_height=self.screen_height)
        r4.starting_x = 100
        r4.starting_y = 300
        r4enemies = [boss, r4enemy2, r4enemy3]
        r4entities = [self.player]
        for i in r4enemies:
            r4entities.append(i)
        r4.entities = r4entities
        r4.enemies = r4enemies

        r4door = Door(x=1100, y=300, width=100, height=100, health=1000, image_path='images/door.png')
        r4.door = r4door
        r3.next_room = r4

        '''
        Here is everything added to Room 5:
        A little guy. Self Explanatory
        A minigun. Self Explanatory
        Door
        '''
        r5 = Room('r5', background_path="images/darkness.png", screen_width=self.screen_width,
                  screen_height=self.screen_height)
        little_guy = Enemy(name='enemy', x=800, y=500, width=50, height=50, speed=.001, health=10, armor=0, gun=0,
                           character=self.player, damage=20, image_path='images/little_guy.png')
        r5.starting_y = 300
        r5.starting_x = 100
        r5enemies = [little_guy]
        r5entities = [self.player, little_guy]
        r5.enemies = r5enemies
        r5entities = r5entities
        r5.add_item(dev_gun)
        r5.door = Door(x=1100, y=300, width=100, height=100, health=1000, image_path='images/door.png')
        r4.next_room = r5

        '''
        Here is everything added to Room 6:
        24 enemies for minigun practice
        '''
        self.r6 = Room('r6', background_path="images/darkness.png", screen_width=self.screen_width,
                       screen_height=self.screen_height)
        self.r6.starting_y = 50
        self.r6.starting_x = 600

        r6enemy1 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemy2 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemy3 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemy4 = Tank(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemy5 = Runner(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemy6 = Runner(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemy7 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemy8 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemy9 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemy10 = Tank(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemy11 = Runner(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemy12 = Runner(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemy13 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemy14 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemy15 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemy16 = Tank(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemy17 = Runner(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemy18 = Runner(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemy19 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemy20 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemy21 = Default(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemy22 = Tank(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemy23 = Runner(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemy24 = Runner(name='enemy', x=random.randint(100, 1000), y=random.randint(200, 600), player=self.player)
        r6enemies = [r6enemy1, r6enemy2, r6enemy3, r6enemy4, r6enemy5, r6enemy6, r6enemy7, r6enemy8, r6enemy9,
                     r6enemy10,
                     r6enemy11, r6enemy12,
                     r6enemy13, r6enemy14, r6enemy15, r6enemy16, r6enemy17, r6enemy24, r6enemy23, r6enemy18, r6enemy19,
                     r6enemy20, r6enemy21, r6enemy22]
        r6entities = [self.player]
        for i in r6enemies:
            r6entities.append(i)
        self.r6.enemies = r6enemies
        self.r6.entities = r6entities
        r5.next_room = self.r6

        self.rooms = [r1, r2, r3, r4, r5, self.r6,]

    def run_game(self):
        """ Runs the game loop. """

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
                    self.player.gun.attack(self.player)
                else:
                    print("You don't got a gun!")

            # Call the collision function of every object
            for i in self.current_room.objects:
                i.collision(self.player, self.current_room.entities)

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
                enemy.move_towards_character(self.player, self.screen_width, self.screen_height)

            # If there's a door the player is colliding with and the player has a key and presses 'f':
            if self.current_room.door:
                if self.current_room.door.collision(self.player, self.current_room.entities) and keys[pygame.K_f] and \
                        self.key in self.player.inventory:
                    # Go to the next room, teleport player to that room's starting location, and remove the key from
                    # player's inventory
                    self.current_room = self.current_room.next_room
                    self.current_room = self.current_room
                    self.player.x = self.current_room.starting_x
                    self.player.y = self.current_room.starting_y
                    self.player.inventory.remove(self.key)

            # Call the render assets function to render all assets in correct positions
            self.render_assets()

            # Death Message/Game Over
            if self.player.health == 0:
                self.user_interface.display_death_menu()
                self.game_over = True

    def render_assets(self):
        self.screen.blit(self.current_room.background, (0, 0))
        # draw background
        self.current_room.draw(self.screen)

        # Draws the current room's door
        if self.current_room.door:
            self.screen.blit(self.current_room.door.image, (self.current_room.door.x, self.current_room.door.y))

        # Draws the player and stats
        self.player.draw(self.screen)
        self.user_interface.display_player_stats(self.player)

        # Draws projectiles
        for g in self.guns:
            for p in g.projectiles:
                p.move()
                pygame.draw.rect(self.screen, colors.YELLOW, (p.x, p.y, p.width, p.height))
            g.update_projectiles(self.player, self.current_room, self.screen_width, self.screen_height)

        # draws enemies and removes them from the room if they die
        if len(self.current_room.enemies) > 0:
            for enemy in self.current_room.enemies:
                if enemy.health > 0:
                    self.screen.blit(enemy.image, (enemy.x, enemy.y))
                else:
                    # When an enemy dies, if it's the last enemy and it's not on the final level:
                    if len(self.current_room.enemies) == 1 and self.current_room != self.r6:
                        # Drop a key at the last enemy's death coords
                        self.key.x = self.current_room.enemies[0].x
                        self.key.original_y = self.current_room.enemies[0].y
                        self.key.y = self.current_room.enemies[0].y
                        self.current_room.add_item(self.key)
                        print("Key dropped!")
                    # Else, everytime any enemy besides the last enemy
                    else:
                        # Roll a die and
                        luck = random.randint(0, 5)
                        # If you roll lucky and not on last room:
                        if luck == 1 and self.current_room != self.r6 and len(self.current_room.items) == 0:
                            # Drop a medkit at enemy death coords
                            self.medkit.x = enemy.x
                            self.medkit.original_y = enemy.y
                            self.medkit.y = enemy.y
                            self.current_room.add_item(self.medkit)
                            print("Medkit Dropped!")
                    # 'Kill' enemy
                    self.current_room.enemies.remove(enemy)

        # draws player inventory
        self.user_interface.display_player_inventory(self.player)

        # Get current mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()
        # Adjust the position to center the crosshair
        crosshair_x = mouse_x - self.crosshair.get_width() // 2
        crosshair_y = mouse_y - self.crosshair.get_height() // 2
        # Draw crosshair on the screen
        self.screen.blit(self.crosshair, (crosshair_x, crosshair_y))

        # update the display
        pygame.display.flip()

    def save_game_state(self):
        game_state = {
            'player_x': self.player.x,
            'player_y': self.player.y,
            'player_health': self.player.health,
            'player_gun_name': self.player.gun.name,
            'ammo_count': self.player.gun.mag_ammo,
            'mag_size': self.player.gun.mag_size,
            'mag_count': self.player.gun.mag_count,
            'player_inventory': [],
            'room_items': {},
            'room_enemies': [],
            'room_objects': [],
            'current_room': self.current_room.name
        }

        for item in self.player.inventory:
            game_state['player_inventory'].append(item.name)

        for item in self.current_room.items:
            game_state['room_items'][item.name] = (item.x, item.y)

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

            if obj_info['type'] == Door:
                obj_info['image_path'] = obj.image_path
            else:
                obj_info['image_path'] = None

            game_state['room_objects'].append(obj_info)

        with open('game_save.pkl', 'wb') as file:
            pickle.dump(game_state, file)

        print('Game Saved')

    def load_game_state(self):
        if os.path.isfile('game_save.pkl'):
            with open('game_save.pkl', 'rb') as file:
                game_state = pickle.load(file)

        for room in self.rooms:
            if room.name == game_state['current_room']:
                self.current_room = room

        # Clear all preset objects of the game
        self.current_room.objects.clear()
        self.current_room.enemies.clear()
        self.current_room.items.clear()

        # Restore player state
        self.player.x = game_state['player_x']
        self.player.y = game_state['player_y']
        self.player.health = game_state['player_health']
        for gun in self.guns:
            if gun.name == game_state['player_gun_name']:
                self.player.gun = gun
        self.player.gun.mag_ammo = game_state['ammo_count']
        self.player.gun.mag_size = game_state['mag_size']
        self.player.gun.mag_count = game_state['mag_count']

        for item in self.items:
            if item.name in game_state['player_inventory']:
                self.player.inventory.append(item)

        for item in self.items + self.guns:
            if item.name in game_state['room_items'].keys():
                self.current_room.items.append(item)
                item.x, item.y = game_state['room_items'][item.name]

        room_enemies = []
        for enemy_info in game_state['room_enemies']:
            enemy = enemy_info['type'](enemy_info['name'], enemy_info['position'][0],
                                       enemy_info['position'][1], self.player)
            enemy.health = enemy_info['health']

            room_enemies.append(enemy)
            self.current_room.enemies.append(enemy)
            self.current_room.entities.append(enemy)

        for obj_info in game_state['room_objects']:
            obj = obj_info['type'](obj_info['position'][0], obj_info['position'][1],
                                   obj_info['dimensions'][0],
                                   obj_info['dimensions'][1], obj_info['health'],
                                   obj_info['image_path'])
            self.current_room.objects.append(obj)

        self.current_room.enemies = room_enemies
