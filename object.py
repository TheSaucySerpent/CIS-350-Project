import pygame


class Object:
    def __init__(self, x, y, width, height, health, image_path=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.obj_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Initialize the image attribute with None
        self.image = None

        if image_path:
            self.image_path = image_path
            self.load_image()

    def collision(self, character):
        # Create a smaller bounding box for the character to decrease the impact area
        character_rect = pygame.Rect(
            character.x + character.width * 0.25,
            character.y + character.height * 0.25,
            character.width * 0.5,
            character.height * 0.5
        )

        # Check if there is a collision between the character and the object
        if self.obj_rect.colliderect(character_rect):
            # If there is a collision, adjust the character's position to prevent passing through
            if character.x < self.x:
                character.x = self.x - character.width * 0.75
            elif character.x + character.width > self.x + self.width:
                character.x = self.x + self.width + character.width * 0.25
            if character.y < self.y:
                character.y = self.y - character.height * 0.75
            elif character.y + character.height > self.y + self.height:
                character.y = self.y + self.height + character.height * 0.25

    def load_image(self):
        if self.image_path:
            self.image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(screen, (0, 0, 255), (self.x, self.y, self.width, self.height))
