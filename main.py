import pygame
from pygame import K_SPACE

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
        pygame.display.set_icon(load_image('bird.ico'))

        self.aspect_ratio = 2
        self.display_size = [self.size[0] // self.aspect_ratio, self.size[1] // self.aspect_ratio]
        self.display = pygame.Surface(self.display_size)

        # Images--------------------------#
        self.background = load_image('background.png')

        # Fonts-----------------------------#
        self.score_fonts = Font('small_font.png', (255, 255, 255), 2)
        self.head_fonts = Font('large_font.png', (255, 255, 255), 3)
        self.highest_score_font = Font('large_font.png', (255, 0, 0), 2)
        self.press_font = Font('small_font.png', (255, 255, 255), 1)

        self.bird = Bird(self.display_size[0] // 2, self.display_size[1] // 2, 0, 0)
        self.pipe_manager = PipeManager(self.display_size)

        self.score = 0
        self.highest_score = 0
        self.clock = Clock(30)
        self._game = True
        self.game_start = False

    def reset_game(self):
        self.bird = Bird(self.display_size[0] // 2, self.display_size[1] // 2, 0, 0)
        self.pipe_manager = PipeManager(self.display_size)
        self.score = 0

    def start_screen(self):
        game = True

        if self.score > self.highest_score:
            self.highest_score = self.score

        while game:
            self.display.blit(self.background, (0, 0))
            self.bird.display(self.display)

            head_width = self.head_fonts.get_width('Flapp Bird', 5)
            head_x = self.display_size[0] - head_width
            self.head_fonts.display_fonts(self.display, 'Flappy Bird', [head_x // 2 - 8, 10], 5)

            head_width = self.highest_score_font.get_width(f'{self.highest_score}', 5)
            head_x = self.display_size[0] - head_width
            self.highest_score_font.display_fonts(self.display, f'{self.highest_score}', [head_x // 2, 80], 5)

            head_width = self.press_font.get_width(f'<SPACE> or <MOUSE LEFT BUTTON>', 5)
            head_x = self.display_size[0] - head_width
            pygame.draw.rect(self.display, (63, 70, 200), (head_x - 10, 223, head_width + 20 - 25, 20))
            self.press_font.display_fonts(self.display, f'<SPACE> or <MOUSE LEFT BUTTON>', [head_x // 2, 230], 5)

            head_width = self.press_font.get_width(f'Your Score : {self.score}', 4)
            head_x = self.display_size[0] - head_width
            pygame.draw.rect(self.display, (63, 70, 200), (head_x // 2 - 5, 195, head_width + 20 - 15, 20))
            self.press_font.display_fonts(self.display, f'Your Score : {self.score}', [head_x // 2, 200], 4)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game = False
                    self._game = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    game = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        game = False

            self.screen.blit(pygame.transform.scale(self.display, self.size), (0, 0))
            pygame.display.update()
            self.clock.tick()
        self.reset_game()

    def main(self):
        while self._game:
            self.display.blit(self.background, (0, 0))
            game_over = self.bird.display(self.display)
            self.bird.update_pos()
            collide_over = self.pipe_manager.update_pipes(self.display, self.bird.bird_rect)

            if self.pipe_manager.check_points(self.bird.bird_rect):
                self.score += 1

            if game_over or collide_over:
                self.start_screen()
                game_over = False
                collide_over = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._game = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.bird.jump()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.bird.jump()

            score_width = self.score_fonts.get_width(f'{self.score}', 3)
            score_x = self.display_size[0] - score_width
            # pygame.draw.rect(self.display, (63, 72, 204), (score_x // 2 - 12, 1, score_width + 20, 20))
            self.score_fonts.display_fonts(self.display, f'{self.score}', [score_x // 2, 5])

            self.screen.blit(pygame.transform.scale(self.display, self.size), (0, 0))
            pygame.display.update()
            self.clock.tick()

if __name__ == "__main__":
    game = Game()
    game.start_screen()
    game.main()