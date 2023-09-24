import pygame
screen_width = 1200
screen_height = 700


class Character:
    def __init__(self, name, x, y, width, height, speed, health, armor, gun):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.health = health
        self.max_health = 100  # VALUE WE WANT FOR MAX HEALTH
        self.armor = armor
        self.gun = gun
        self.last_hurt = 0
        self.last_dodge = 0
        self.invulnerable = False

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def move(self, keys, extra_speed, is_invulnerable = False):
        new_x = self.x
        new_y = self.y

        if is_invulnerable:
            self.invulnerable = True

        if keys[pygame.K_w]:
            new_y -= self.speed + extra_speed
        if keys[pygame.K_a]:
            new_x -= self.speed + extra_speed
        if keys[pygame.K_s]:
            new_y += self.speed + extra_speed
        if keys[pygame.K_d]:
            new_x += self.speed + extra_speed

        # Check if the new position is within the screen bounds
        if 0 <= new_x <= screen_width - self.width and 0 <= new_y <= screen_height - self.height:
            self.x = new_x
            self.y = new_y


        self.invulnerable = False

    def take_damage(self, damage):
        if not self.invulnerable:
            current_time = pygame.time.get_ticks()
            if self.name == 'Player':
                #To change invulnerability time, change value of 300
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
        if self.health >= self.max_health:
            self.health = self.max_health
        else:
            self.health += amount





