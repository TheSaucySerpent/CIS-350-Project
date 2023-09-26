import pygame
import glob_var
import colors
import UI

# This is just to make it easier to read in the running loop.
player = glob_var.player
obj = glob_var.obj
enemies = glob_var.enemies


class Game:
    def __init__(self, screen, screen_width, screen_height, font):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.font = font

    def run_game(self):

        game_over = False
        self.screen.fill(colors.BLACK)
        # If r is press, calls weapon reload function
        # If space is pressed and its been 1 second, does a dodge/teleport with invulnerability
        # wasd to move
        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_r]:
                player.gun.reload()
            if keys[pygame.K_SPACE]:
                current_time = pygame.time.get_ticks()
                if current_time - player.last_dodge > 1000:
                    player.move(keys, 200, True)
                    player.last_dodge = current_time
                else:
                    player.move(keys, 0)
            else:
                player.move(keys, 0)

            if pygame.mouse.get_pressed()[0]:  # Left mouse button
                if player.gun != 0:
                    player.gun.attack()
                else:
                    print("You don't got a gun!")

        # Labeled separately so I can use pygame's .colliderect()
        player_rect = (player.x, player.y, player.width, player.height)

        # Draw the character
        pygame.draw.rect(self.screen, colors.BLUE, player_rect)

        # Draw projectiles
        for g in glob_var.guns:
            for p in g.projectiles:
                p.move()
                pygame.draw.rect(self.screen, colors.YELLOW, (p.x, p.y, p.width, p.height))
            g.update_projectiles()

        # Draw and update enemy: makes enemies move towards player, checks for enemy-player collision and
        # kills them
        for enemy in enemies:
            enemy.move_towards_character()

            if enemy.health > 0:
                pygame.draw.rect(self.screen, (255, 0, 0), (enemy.x, enemy.y, enemy.width, enemy.height))
            else:
                enemies.remove(enemy)

        # Draw objects & handle object collision
        for obj in glob_var.objs:
            for entity in glob_var.entities:
                entity_rect = pygame.Rect(entity.x, entity.y, entity.width, entity.height)
                if entity_rect.colliderect(obj.obj_rect):
                    # Left Border
                    if entity.x + entity.width < obj.x + 2:
                        entity.x -= 1
                    # Right Border
                    elif entity.x > obj.x + obj.width - 2:
                        entity.x += 1
                    # Upper Border
                    elif entity.y < obj.y:
                        entity.y -= 1
                    # Lower Board
                    elif entity.y > obj.y:
                        entity.y += 1
            pygame.draw.rect(self.screen, (192, 192, 192), obj.obj_rect)

            UI.display_player_stats(self.screen, player, self.font)

            # Death Message/Game Over
            if player.health == 0:
                ded_text = self.font.render(f"You Died.", True, (255, 0, 0))
                self.screen.blit(ded_text,
                                 ((self.screen_width - ded_text.get_width()) // 2,
                                  (self.screen_height - ded_text.get_height()) // 2))
                game_over = True

        # update the display
        pygame.display.update()
