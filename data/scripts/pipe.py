import pygame
import random

from data.scripts.image_functions import load_image, scale_image_size


class PipeManager:
    def __init__(self, screen_size):
        self.screen_size = screen_size
        self.pipe_number = 5
        self.speed = 3
        self.distance = 150
        self.height_distance = 80
        self.pipes_data = []
        self.initial_arrangements()

    def add_another_pipe(self):
        if self.pipes_data == []:
            start_x = self.screen_size[1] + 50
        else:
            start_x = self.pipes_data[-1].x + self.distance
        first_height = random.randint(self.screen_size[1] - self.height_distance - 160,
                                      self.screen_size[1] - self.height_distance - 20)
        second_height = self.screen_size[1] - self.height_distance - first_height
        pipe_number = random.randint(1, 4)
        self.pipes_data.append(Pipe(start_x, 0, first_height, pipe_number))
        self.pipes_data.append(Pipe(start_x, first_height + self.height_distance, second_height, pipe_number))
        start_x += self.distance

    def initial_arrangements(self):
        for _ in range(0, self.pipe_number):
            self.add_another_pipe()

    def update_pipes(self, display, bird_rect):
        for _, pipe in enumerate(self.pipes_data):
            pipe.update_pos(self.speed)
            collide = pipe.display(display, bird_rect)
            if pipe.check_disappearence():
                self.pipes_data.remove(pipe)
                self.add_another_pipe()
            if collide:
                return True

class Pipe:
    def __init__(self, x, y, height, pipe_number):
        self.x = x
        self.y = y
        self.height = height
        self.image = load_image(f'pipes/pipe_{pipe_number}.png')
        self.image = scale_image_size(self.image, self.image.get_width(), self.height)
        self.rect = pygame.Rect(self.x, self.y, self.image.get_width(), self.height)

    def check_disappearence(self):
        if self.x < -300:
            return True
        return False

    def update_pos(self, speed):
        self.x -= speed
        self.rect.x = self.x

    def display(self, display, bird_rect):
        display.blit(self.image, (self.x, self.y))
        # pygame.draw.rect(display, (255, 255, 0), self.rect)
        if self.rect.colliderect(bird_rect):
            return True
        return False