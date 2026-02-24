import pygame
import sys
from market.market import Market

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Market RPG")
        self.clock = pygame.time.Clock()

        self.market = Market()
        self.running = True

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        self.market.update_day()

    def draw(self):
        self.screen.fill((30, 30, 40))
        pygame.display.flip()
