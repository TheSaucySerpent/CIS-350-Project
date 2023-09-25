import pygame

class Object:
    def __init__(self, x, y, width, height, health, image_path=None):
        self.x = x
        self.y = y
        self.init_y = y  # Initial y position for bounce reset
        self.width = width
        self.height = height
        self.health = health
        self.bounce_speed = 8  # Speed of the bounce
        self.bounce_direction = 1  # Start moving down

        if image_path:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, screen):
        if hasattr(self, 'image'):
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, self.width, self.height))

    def bounce(self):
        self.y += self.bounce_speed * self.bounce_direction
        if self.y >= self.init_y + 10 or self.y <= self.init_y - 10:
            self.bounce_direction *= -1  # Reverse direction

    @property
    def area(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def is_near(self, player):
        # Assume player has x and y attributes
        distance = ((self.x - player.x) ** 2 + (self.y - player.y) ** 2) ** 0.5
        return distance < 50  # change 50 to the desired interaction distance

    def interact(self, screen, font):
        text = font.render('Interact with object', True, (255, 255, 255))
        screen.blit(text, (self.x, self.y - 30))  # change the coordinates as needed