import pygame

class MainMenuUI:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 48)
        self.options = ["New Game", "Load Game", "Quit"]
        self.selected = 0

    def draw(self, screen):
        screen.fill((10, 10, 30))
        y = 200
        for i, option in enumerate(self.options):
            color = (255, 255, 0) if i == self.selected else (255, 255, 255)
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(400, y))
            screen.blit(text, rect)
            y += 80
        pygame.display.flip()

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % len(self.options)

            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % len(self.options)

            elif event.key == pygame.K_RETURN:
                return self.options[self.selected]

        return None 
