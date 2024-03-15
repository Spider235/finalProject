import pygame

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
GRAY = (197, 194, 197)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)


class ReviewMenuContent:
    def __init__(self):
        self.rect = pygame.Rect(50, 50, 600, 1000)  # Example rect for the content area
        self.content_height = 1000  # Example height of the content
        self.scroll_y = 0  # Initial scroll position
        self.scroll_speed = 10  # Speed of scrolling
        self.scroll_up = False
        self.scroll_down = False

    def update(self):
        if self.scroll_up:
            self.rect.y += self.scroll_speed
        elif self.scroll_down:
            self.rect.y -= self.scroll_speed

        # Limit the movement of content_rect to keep it within the screen bounds
        if self.rect.top > 50:
            self.rect.top = 50
        elif self.rect.bottom < SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.rect)

    def handle_event(self, event):
        pass


class ScrollBar:
    def __init__(self, content_height, content_rect):
        self.content_height = content_height
        self.content_rect = content_rect
        self.scroll_speed = 10  # Speed of scrolling
        self.bar_height = int((SCREEN_HEIGHT - 40) / (content_height / (SCREEN_HEIGHT * 1.0)))
        self.bar_rect = pygame.Rect(SCREEN_WIDTH - 20, 20, 20, self.bar_height)
        self.bar_up = pygame.Rect(SCREEN_WIDTH - 20, 0, 20, 20)
        self.bar_down = pygame.Rect(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20, 20, 20)
        self.on_bar = False
        self.mouse_diff = 0
        self.scroll_up = False
        self.scroll_down = False

    def update(self, content):
        # Calculate the new position of the content rectangle based on the scrollbar's position
        content_position = (self.bar_rect.y - 20) / (SCREEN_HEIGHT - self.bar_rect.height - 40) * \
                           (self.content_height - SCREEN_HEIGHT + 100)
        content.rect.y = -content_position

    def event_handler(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if self.bar_rect.collidepoint(pos):
                self.mouse_diff = pos[1] - self.bar_rect.y
                self.on_bar = True
            elif self.bar_up.collidepoint(pos):
                self.scroll_up = True
            elif self.bar_down.collidepoint(pos):
                self.scroll_down = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.on_bar = False
            self.scroll_up = False
            self.scroll_down = False

        if event.type == pygame.MOUSEMOTION:
            if self.on_bar:
                new_y = pygame.mouse.get_pos()[1] - self.mouse_diff
                if new_y < 20:
                    new_y = 20
                elif new_y > SCREEN_HEIGHT - self.bar_rect.height - 20:
                    new_y = SCREEN_HEIGHT - self.bar_rect.height - 20
                self.bar_rect.y = new_y

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.scroll_up = True
            elif event.key == pygame.K_DOWN:
                self.scroll_down = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.scroll_up = False
            elif event.key == pygame.K_DOWN:
                self.scroll_down = False

    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, self.bar_rect)
        pygame.draw.rect(screen, BLUE, self.bar_up)
        pygame.draw.rect(screen, BLUE, self.bar_down)


def review_menu():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Review Menu")
    clock = pygame.time.Clock()

    content = ReviewMenuContent()
    content.rect.y = 50  # Set the initial y-position of the content rectangle

    scrollbar = ScrollBar(content.content_height, content.rect)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            content.handle_event(event)
            scrollbar.event_handler(event)

        content.update()
        scrollbar.update(content)

        screen.fill(WHITE)
        content.draw(screen)
        scrollbar.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    review_menu()
