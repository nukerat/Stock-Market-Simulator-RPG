import pygame
import sys
from player.player import Player
from market.market import Market
from ui.market_ui import MarketUI
from ui.main_menu_ui import MainMenuUI
from ui.pause_menu_ui import PauseMenuUI
from save.save_manager import save_game, load_game

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Market RPG")
        self.clock = pygame.time.Clock()

        # Systems
        self.player = Player()
        self.market = Market()
        self.market_ui = MarketUI()
        self.main_menu = MainMenuUI()
        self.pause_menu = PauseMenuUI()

        # Fonts
        self.font = pygame.font.SysFont(None, 24)

        # State
        self.running = True
        self.in_menu = True
        self.in_pause = False
        self.show_market = False

        self.day_timer = 0
        self.DAY_LENGTH = 300

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_input()
            self.update()
            self.draw()

    def handle_input(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # -------- MAIN MENU --------
            if self.in_menu:
                choice = self.main_menu.handle_input(event)
                if choice == "New Game":
                    self.in_menu = False
                elif choice == "Load Game":
                    if load_game(self.player, self.market):
                        self.in_menu = False
                elif choice == "Quit":
                    pygame.quit()
                    sys.exit()
                continue

            # -------- PAUSE TOGGLE --------
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.in_pause = not self.in_pause
                return

            # -------- PAUSE MENU INPUT --------
            if self.in_pause:
                stay_open = self.pause_menu.handle_input(event, self.player, self.market)
                self.in_pause = stay_open
                return

            # -------- GAME INPUT --------
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                self.show_market = not self.show_market

            # -------- MARKET INPUT --------
            if self.show_market:
                self.market_ui.handle_input(event, self.player, self.market)

        # -------- MOVEMENT --------
        if not self.in_menu and not self.in_pause and not self.show_market:
            pressed = pygame.key.get_pressed()
            keys = {
                "up": pressed[pygame.K_w],
                "down": pressed[pygame.K_s],
                "left": pressed[pygame.K_a],
                "right": pressed[pygame.K_d]
            }
            self.player.move(keys)

    def update(self):
        if not self.in_menu and not self.in_pause:
            self.day_timer += 1
            if self.day_timer >= self.DAY_LENGTH:
                self.day_timer = 0
                self.market.update_day()

    def draw(self):
        if self.in_menu:
            self.main_menu.draw(self.screen)
        else:
            self.screen.fill((30, 30, 40))

            # Player
            pygame.draw.rect(
                self.screen,
                (200, 200, 255),
                (self.player.x, self.player.y, self.player.size, self.player.size)
            )

            # Gold display
            gold_text = self.font.render(f"Gold: {self.player.gold}", True, (255, 255, 0))
            self.screen.blit(gold_text, (10, 10))

            # Market UI
            if self.show_market:
                self.market_ui.draw(self.screen, self.market)

            # Pause menu
            if self.in_pause:
                self.pause_menu.draw(self.screen)

            pygame.display.flip()
