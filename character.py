import pygame
import weapons


class Character:
    """ Class used for all moving entities, including the player and enemies. """

    def __init__(self, name, x, y, width, height, speed, health, armor, gun, image_path=None):
        """
        Initializes the character

        Args:
        name (str): The name of the character.
        x (int): The x-coordinate of the character's position.
        y (int): The y-coordinate of the character's position.
        width (int): The width of the character.
        height (int): The height of the character.
        speed (int): The movement speed of the character.
        health (int): The current health of the character.
        armor (int): The armor rating of the character.
        gun (Weapon): The type of gun the character wields.
        image_path (str, optional): Path to the image for the character (If none is given, uses a color instead.
        """
        # Validate input values
        if not isinstance(name, str) or not name:
            raise ValueError("Name must be a non-empty string.")

        if not isinstance(x, (int, float)) or 0 > x > 1200:
            raise ValueError("X-coordinate must be a numeric value.")

        if not isinstance(y, (int, float)) or 0 > y > 700:
            raise ValueError("Y-coordinate must be a numeric value.")

        if not isinstance(width, (int, float)) or width <= 0:
            raise ValueError("Width must be a positive numeric value.")

        if not isinstance(height, (int, float)) or height <= 0:
            raise ValueError("Height must be a positive numeric value.")

        if not isinstance(speed, (int, float)) or speed <= 0:
            raise ValueError("Speed must be a positive numeric value.")

        if not isinstance(health, int) or health < 0:
            raise ValueError("Health must be a non-negative integer.")

        if not isinstance(armor, int) or armor < 0:
            raise ValueError("Armor must be a non-negative integer.")

        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.health = health
        self.max_health = 100
        self.armor = armor
        self.gun = gun
        self.last_hurt = 0
        self.last_dodge = 0
        self.invulnerable = False
        self.image_index = 0
        self.image = None
        self.picked_up = False
        self.inventory = []

        '''self.image_path = {
            'up': ['images/Up standing.png', 'images/Up running.png'],
            'down': ['images/Down standing.png', 'images/Down running.png'],
            'left': ['images/Left standing.png', 'images/Left running .png'],
            'right': ['images/1.png', 'images/BackgroundEraser_image.png']
            }'''
        self.image_path = {
            'left': ['images/player_assets/standing_left.png', 'images/player_assets/walking_left.png'],
            'right': ['images/player_assets/standing_right.png', 'images/player_assets/walking_right.png']

        }

        self.direction = 'right'
        self.image_change_delay = 100  # Delay between frame changes
        self.frame_count = 0

        if self.image_path:
            self.load_images()
            # Load the initial image
            self.image = self.images[self.direction][0]
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def load_images(self):
        """
        Load character images for different directions.

        Loads images for character animations in different directions.
        """
        self.images = {}
        for direction, paths in self.image_path.items():
            self.images[direction] = [pygame.image.load(path) for path in paths]

    def set_image(self, direction):

        """
        Set the character's image based on the current direction and animation frame.

        Args:
            direction (str): The direction in which the character is facing.
        """

        if direction in self.images:
            # Check the timer
            if self.frame_count >= self.image_change_delay:
                self.image_index = (self.image_index + 1) % len(self.images[direction])
                self.frame_count = 0  # Reset frame_count
                self.image = self.images[direction][self.image_index]
                self.image = pygame.transform.scale(self.image, (self.width, self.height))
            else:
                self.frame_count += 1

    def move(self, screen_width, screen_height, keys, extra_speed, is_invulnerable=False):
        """
        Method used for normal movement as well as dodge. Moves the given Character by their speed

        Args:
        keys (arr): The key pressed determines the direction the speed is added to
        extra_speed (int): Gets added to the character's base speed, used for dodge ability
        is_invulnerable (bool, optional): Used to make the player invulnerable during dodge
        """
        new_x = self.x
        new_y = self.y

        if is_invulnerable:
            self.invulnerable = True

        direction = None  # Store the current movement direction

        if keys[pygame.K_w]:
            new_y -= self.speed + extra_speed
            # direction = 'up'
        if keys[pygame.K_a]:
            new_x -= self.speed + extra_speed
            direction = 'left'
        if keys[pygame.K_s]:
            new_y += self.speed + extra_speed
            # direction = 'down'
        if keys[pygame.K_d]:
            new_x += self.speed + extra_speed
            direction = 'right'

        if direction:
            self.set_image(direction)  # Set the character's image based on the current direction

        # Keeps character within bounds
        if 0 <= new_x <= screen_width - self.width and 0 <= new_y <= screen_height - self.height:
            self.x = new_x
            self.y = new_y

        self.invulnerable = False

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def take_damage(self, damage):
        """
        Reduce the character's health by a specified amount of damage.
        This method calculates damage based on the character's health and armor and updates both accordingly.


        Args:
        damage (int): The amount of damage to subtract from the character's health.
        """
        if not self.invulnerable:
            current_time = pygame.time.get_ticks()
            # Needed to be done differently for player and enemies, so players can't be instantly killed and enemies can be destroyed by things like shotguns
            if self.name == 'Player':
                # To change invulnerability time, change value of 300
                if current_time - self.last_hurt > 300:
                    extra_damage = 0
                    if self.armor > 0:
                        self.armor -= damage
                        if self.armor < 0:
                            extra_damage = self.armor * -1
                            self.armor = 0
                    if extra_damage > 0:
                        self.health -= extra_damage
                    else:
                        self.health -= damage
                    if self.health < 0:
                        self.health = 0
                    self.last_hurt = current_time
            else:
                extra_damage = 0
                if self.armor > 0:
                    self.armor -= damage
                    if self.armor < 0:
                        extra_damage = self.armor * -1
                        self.armor = 0
                if extra_damage > 0:
                    self.health -= extra_damage
                else:
                    self.health -= damage
                if self.health < 0:
                    self.health = 0

    def heal(self, amount):
        """
        Increase the character's health by a specified amount, up to the maximum health. Used exlusively for medkits.

        Args:
        amount (int): The amount of health to add to the character.
        """
        if self.health + amount > self.max_health:
            self.health = self.max_health
        else:
            self.health += amount

    def draw(self, screen):
        """
        Draw the character on the screen.
        If an image is available, it is drawn; otherwise, a blue rectangle is drawn to represent the character.

        Args:
        screen (pygame.Surface): The pygame screen surface on which to draw the character.
        """
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.width, self.height))

    def pick_up(self, current_room):
        """
        Allow the character to pick up items from the current room.
        This method sees if the chracter pressed e on an item, and, if so, adds it to inventory.

        Args:
        current_room (Room): The current room the character is in.
        """
        keys = pygame.key.get_pressed()
        items = current_room.items.copy()  # Make a copy of the items in the room to avoid modifying the original list while iterating
        for item in items:
            if (self.x < item.x + item.width and
                self.x + self.width > item.x and
                self.y < item.y + item.height and
                self.y + self.height > item.y) and keys[pygame.K_e]:
                if type(item) == weapons.Weapon or type(item) == weapons.Shotgun:
                    self.gun = item
                    current_room.items.remove(item)
                else:
                    # Add the object to the character's inventory
                    self.inventory.append(item)
                    # Remove the object from the list of objects in the room
                    current_room.items.remove(item)

    def update_position(self):
        """ Update the object's position to the character inventory if it's picked up """
        for item in self.inventory:
            item.x = self.x
            item.y = self.y + self.height
