import pygame

screen_width = 1200
screen_height = 700


class Character:
    def __init__(self, x, y, width, height, speed, health, armor, gun, image_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.health = health
        self.armor = armor
        self.gun = gun
        self.last_hurt = 0
        self.last_dodge = 0
        self.invulnerable = False
        self.image_counter = 0  # Initialize counter at 0
        self.animation_delay = 250  # Time in milliseconds between animation frames
        self.last_animation_update = 0  # Time of last animation frame update

        if isinstance(image_path, str):  # Single image
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        elif isinstance(image_path, dict):  # Animated sprites
            self.images = {}
            for direction, paths in image_path.items():
                self.images[direction] = [pygame.image.load(p) for p in paths]
                self.images[direction] = [pygame.transform.scale(img, (self.width, self.height)) for img in
                                          self.images[direction]]
            # Initialize with the first image in 'down' direction or any other default direction
            self.image = self.images['down'][0]

    def draw(self, screen):
        if hasattr(self, 'image') and self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.width, self.height))

    def move(self, keys, extra_speed, is_invulnerable=False):
        new_x = self.x
        new_y = self.y
        current_direction = None  # Keep track of the current direction

        if is_invulnerable:
            self.invulnerable = True

        if keys[pygame.K_w]:
            new_y -= self.speed + extra_speed
            current_direction = 'up'
        if keys[pygame.K_a]:
            new_x -= self.speed + extra_speed
            current_direction = 'left'
        if keys[pygame.K_s]:
            new_y += self.speed + extra_speed
            current_direction = 'down'
        if keys[pygame.K_d]:
            new_x += self.speed + extra_speed
            current_direction = 'right'

        current_time = pygame.time.get_ticks()
        if current_time - self.last_animation_update >= self.animation_delay:
            self.last_animation_update = current_time
            if current_direction:
                self.image_counter = (self.image_counter + 1) % len(self.images[current_direction])
                self.image = self.images[current_direction][self.image_counter]

        if 0 <= new_x <= screen_width - self.width and 0 <= new_y <= screen_height - self.height:
            self.x = new_x
            self.y = new_y

        self.invulnerable = False


    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


    def take_damage(self, damage):
        if not self.invulnerable:
            current_time = pygame.time.get_ticks()
            #To change invulnerability time, change value of 100
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

    def heal(self, amount):
        maxhealth = 100 #VALUE WE WANT FOR MAX HEALTH
        if self.health >= maxhealth:
            self.health = maxhealth
        else:
            self.health += amount





