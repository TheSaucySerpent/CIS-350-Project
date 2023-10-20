import pygame


class Item:
    def __init__(self, x, y, width, height, health, image_path=None):
        self.x = x
        self.y = y
        self.original_y = y  # Store the original y position
        self.width = width
        self.height = height
        self.health = health
        self.obj_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.bounce_speed = 0.05  # Adjust the bounce speed for a slower bounce
        self.bounce_direction = 1

        self.image = None

        if image_path:
            self.image_path = image_path
            self.load_image()

    def load_image(self):
        if self.image_path:
            self.image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))


    def bounce(self):
        # Update the y position for bouncing
        self.y += self.bounce_speed * self.bounce_direction

        # Check if the object is within the bounce range
        if self.y >= self.original_y + 10 or self.y <= self.original_y - 10:
            # Reverse the bounce direction when reaching the limits
            self.bounce_direction *= -1

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.width, self.height))