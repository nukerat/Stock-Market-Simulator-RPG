import pygame
from save.save_manager import save_game

class PauseMenuUI:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 48)
        self.options = ["Resume", "Save Game", "Quit"]
        self.selected = 0

    def draw(self, screen):
        overlay = pygame.Surface(screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        y = 200
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(400, y))
            screen.blit(text, rect)
            y += 80
        pygame.display.flip()

    def handle_input(self, event, player, market=None):
        """
        Returns True to keep menu open, False to close menu.
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                choice = self.options[self.selected]
                if choice == "Resume":
                    return False   # close pause menu
                elif choice == "Save Game":
                    save_game(player, market)
                    return True    # stay in menu
                elif choice == "Quit":
                    pygame.quit()
                    exit()
        return True  # keep menu open by default



    
