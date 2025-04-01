import pygame
from data.scripts.animation_player import AnimationPlayer


class Bird:
    def __init__(self, x, y, x_size, y_size):
        self.x = x
        self.y = y
        self.x_size = x_size
        self.y_size = y_size
        self.offset = [0, 0]
        self.gravity = -0.4
        self.velocity = 0
        self.jump_strength = 5
        self.bird = AnimationPlayer(self.x, self.y)
        self.bird.animations('bird')
        self.bird_size = self.bird.size
        self.bird_rect = pygame.Rect(self.x - self.bird_size[0] // 2, self.y - self.bird_size[1] // 3, *self.bird_size)

    def jump(self):
        self.velocity = self.jump_strength

    def game_over(self, display):
        y = self.bird.y - self.offset[1]
        if y < 0 or y > display.get_height():
            return True
        return False

    def update_pos(self):
        self.velocity += self.gravity
        self.offset[1] += self.velocity
        self.y += self.velocity
        self.bird_rect.y -= self.velocity

    def display(self, display):
        self.bird.play_animation(display, self.offset)
        # pygame.draw.rect(display, (255, 0, 0), self.bird_rect)
        return self.game_over(display)
