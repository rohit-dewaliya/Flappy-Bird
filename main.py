import pygame

from data.scripts.clock import Clock
from data.scripts.font import Font
from data.scripts.image_functions import load_image, scale_image_ratio
from data.scripts.bird import Bird
from data.scripts.pipe import PipeManager


class Game:
    def __init__(self):
        self.size = [512, 512]
        self.screen = pygame.display.set_mode(self.size, 0, 32)

        pygame.display.set_caption("Flappy Bird")

        self.aspect_ratio = 2
        self.display_size = [self.size[0] // self.aspect_ratio, self.size[1] // self.aspect_ratio]
        self.display = pygame.Surface(self.display_size)

        # Images--------------------------#
        self.background = load_image('background.png')


        self.bird = Bird(self.display_size[0] // 2, self.display_size[1] // 2, 0, 0)
        self.pipe_manager = PipeManager(self.display_size)

        self.clock = Clock(30)
        self._game = True

    def main(self):
        while self._game:
            self.display.blit(self.background, (0, 0))
            game_over = self.bird.display(self.display)
            self.bird.update_pos()
            collide_over = self.pipe_manager.update_pipes(self.display, self.bird.bird_rect)
            if game_over or collide_over:
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._game = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.bird.jump()

            self.screen.blit(pygame.transform.scale(self.display, self.size), (0, 0))
            pygame.display.update()
            self.clock.tick()

if __name__ == "__main__":
    game = Game()
    game.main()