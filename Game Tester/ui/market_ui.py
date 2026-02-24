import pygame

class MarketUI:
    def __init__(self):
        self.font = pygame.font.SysFont(None, 24)
        self.text_font = pygame.font.SysFont(None, 40)

        self.selected_index = 0
        self.item_rects = []

        self.buy_rect = pygame.Rect(500, 40, 100, 60)
        self.sell_rect = pygame.Rect(600, 40, 100, 60)

        # Confirmation state
        self.confirming = False
        self.confirm_action = None  # "buy" or "sell"
        self.confirm_choice = 0  # 0 = Yes, 1 = No

        #warning windows
        self.show_warning = False
        self.warning_text = ""

    def handle_input(self, event, player, market):
        # -------- CONFIRM WINDOW INPUT --------
        if self.confirming:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    self.confirm_choice = 1 - self.confirm_choice

                elif event.key == pygame.K_RETURN:
                    if self.confirm_choice == 0:
                        if self.confirm_action == "buy":
                            self.execute_buy(player, market)
                        elif self.confirm_action == "sell":
                            self.execute_sell(player, market)

                    self.confirming = False
                    self.confirm_action = None

                elif event.key == pygame.K_ESCAPE:
                    self.confirming = False
                    self.confirm_action = None
            return
        if self.show_warning:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.show_warning = False
            return

        # -------- NORMAL INPUT --------
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(market.items)

            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(market.items)

            elif event.key == pygame.K_b:
                self.start_confirm("buy")

            elif event.key == pygame.K_v:
                self.start_confirm("sell")

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            for i, rect in enumerate(self.item_rects):
                if rect.collidepoint(mouse_pos):
                    self.selected_index = i
                    return

            if self.buy_rect.collidepoint(mouse_pos):
                self.start_confirm("buy")

            if self.sell_rect.collidepoint(mouse_pos):
                self.start_confirm("sell")


    def start_confirm(self, action):
        self.confirming = True
        self.confirm_action = action
        self.confirm_choice = 0

    def execute_buy(self, player, market):
        item = market.items[self.selected_index]
        if player.gold >= item.price:
            player.gold -= item.price
            player.inventory[item.name] = player.inventory.get(item.name, 0) + 1
            player.history.append(f"bought {item.name} for {item.price} gold")
            
        else:
            self.show_warning = True
            self.warning_text = "You do not have enough Gold"

    def execute_sell(self, player, market):
        item = market.items[self.selected_index]
        if player.inventory.get(item.name, 0) > 0:
            player.inventory[item.name] -= 1
            player.gold += item.price
            player.history.append(f"sold {item.name} for {item.price} gold")
        else:
            self.show_warning = True
            self.warning_text = "You do not have this item"

    def draw_warning(self, screen):
        rect = pygame.Rect(250,200,300,100)
        pygame.draw.rect(screen,(40,40,40), rect)
        pygame.draw.rect(screen,(250,0,0), rect, 2)

        text = self.font.render(self.warning_text, True, (255,0,0))
        screen.blit(text, (rect.x+10, rect.y+40))
        


    def draw(self, screen, market):
        pygame.draw.rect(screen, (20, 20, 20), (100, 100, 600, 400))

        self.item_rects = []
        y = 130

        for i, item in enumerate(market.items):
            color = (255, 255, 0) if i == self.selected_index else (255, 255, 255)
            text = self.font.render(f"{item.name}: {item.price} gold", True, color)
            rect = text.get_rect(topleft=(130, y))
            screen.blit(text, rect)
            self.item_rects.append(rect)
            y += 40

        # BUY button
        pygame.draw.rect(screen, (0, 200, 0), self.buy_rect)
        buy_text = self.text_font.render("BUY", True, (255, 255, 255))
        screen.blit(buy_text, buy_text.get_rect(center=self.buy_rect.center))

        # SELL button
        pygame.draw.rect(screen, (200, 0, 0), self.sell_rect)
        sell_text = self.text_font.render("SELL", True, (255, 255, 255))
        screen.blit(sell_text, sell_text.get_rect(center=self.sell_rect.center))

        # CONFIRM WINDOW
        if self.confirming:
            self.draw_confirm(screen, market)

        # WARNING WINDOW
        if self.show_warning:
            self.draw_warning(screen)

    def draw_confirm(self, screen, market):
        pygame.draw.rect(screen, (0, 0, 0), (200, 200, 400, 200))
        pygame.draw.rect(screen, (255, 255, 255), (200, 200, 400, 200), 2)

        item = market.items[self.selected_index]
        price = item.price
        action_text = "Buy" if self.confirm_action == "buy" else "Sell"

        msg = f"{action_text} {item.name} for {price} gold?"
        text = self.font.render(msg, True, (255, 255, 255))
        screen.blit(text, (230, 250))

        yes_color = (255, 255, 0) if self.confirm_choice == 0 else (255, 255, 255)
        no_color = (255, 255, 0) if self.confirm_choice == 1 else (255, 255, 255)

        yes_text = self.font.render("YES", True, yes_color)
        no_text = self.font.render("NO", True, no_color)

        screen.blit(yes_text, (300, 330))
        screen.blit(no_text, (450, 330))
