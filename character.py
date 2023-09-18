import pygame
screen_width = 1200
screen_height = 700

class Character:
    def __init__(self, x, y, width, height, speed, health, armor):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.health = health
        self.armor = armor

    def move(self, keys):
        new_x = self.x
        new_y = self.y

        if keys[pygame.K_w]:
            new_y -= self.speed
        if keys[pygame.K_a]:
            new_x -= self.speed
        if keys[pygame.K_s]:
            new_y += self.speed
        if keys[pygame.K_d]:
            new_x += self.speed

        # Check if the new position is within the screen bounds
        if 0 <= new_x <= screen_width - self.width and 0 <= new_y <= screen_height - self.height:
            self.x = new_x
            self.y = new_y

    def take_damage(self, damage):
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



    def heal(self, amount):
        maxhealth = 100 #VALUE WE WANT FOR MAX HEALTH
        if self.health >= maxhealth:
            self.health = maxhealth
        else:
            self.health += amount

