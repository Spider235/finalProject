import pygame
import sys

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
GRAY = (197, 194, 197)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)


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
        self.content_rect = content_rect  # Store the content rectangle

    def update(self):
        if self.scroll_up:
            self.content_rect.y += self.scroll_speed
        elif self.scroll_down:
            self.content_rect.y -= self.scroll_speed

        # Limit the movement of content_rect to keep it within the content area
        if self.content_rect.top > 50:
            self.content_rect.top = 50
        elif self.content_rect.bottom < SCREEN_HEIGHT - 50:
            self.content_rect.bottom = SCREEN_HEIGHT - 50

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


def review_menu(username):
    pygame.init()
    clock = pygame.time.Clock()
    screen_width = 700
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Sprachenspiel Review Menu")
    base_font = pygame.font.Font(None, 32)
    headline_font = pygame.font.Font(None, 100)
    button_width = 200
    button_height = 50
    button_spacing = 50
    back_button_rect = pygame.Rect((screen_width - button_width) // 2, 500, button_width, button_height)
    button_color = pygame.Color("red")
    button_text_color = pygame.Color("white")
    back_button_text = "Go Back"
    running = True

    # Define content area
    content_rect = pygame.Rect(50, 150, 600, 1000)
    content_height = 1000

    scrollbar = ScrollBar(content_height, content_rect)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            scrollbar.event_handler(event)

        scrollbar.update()

        screen.fill((0, 0, 0))

        # Headline label
        headline_label = headline_font.render("Review Menu", True, (255, 255, 255))
        screen.blit(headline_label, ((screen_width - headline_label.get_width()) // 2, 50))

        # Render the "Go Back" button
        pygame.draw.rect(screen, button_color, back_button_rect)
        back_button_label = base_font.render(back_button_text, True, button_text_color)
        back_button_label_rect = back_button_label.get_rect(center=back_button_rect.center)
        screen.blit(back_button_label, back_button_label_rect)

        # Draw content area
        pygame.draw.rect(screen, GRAY, content_rect)

        # Draw scrollbar
        scrollbar.draw(screen)

        pygame.display.flip()
        clock.tick(60)


def main_menu(username):
    pygame.init()
    clock = pygame.time.Clock()
    screen_width = 700
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Sprachenspiel Main Menu")
    base_font = pygame.font.Font(None, 32)
    headline_font = pygame.font.Font(None, 100)
    score_font = pygame.font.Font(None, 32)

    # Define the buttons
    button_width = 200
    button_height = 50
    button_spacing = 50
    practice_button_rect = pygame.Rect((screen_width - button_width) // 2, 250, button_width, button_height)
    review_button_rect = pygame.Rect((screen_width - button_width) // 2, 250 + button_height + button_spacing, button_width, button_height)
    button_color = pygame.Color("red")
    button_text_color = pygame.Color("white")
    practice_button_text = "Practice"
    review_button_text = "Review"

    score = 0  # Placeholder for the score
    level = " "  # Placeholder for the level

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if practice_button_rect.collidepoint(event.pos):
                    print("Practice button clicked")
                    # Add your practice button functionality here
                elif review_button_rect.collidepoint(event.pos):
                    print("Review button clicked")
                    review_menu(username)  # Open the review menu
                    return  # Close the main menu window

        screen.fill((0, 0, 0))

        # Headline label
        headline_label = headline_font.render("Sprachenspiel", True, (255, 255, 255))
        screen.blit(headline_label, ((screen_width - headline_label.get_width()) // 2, 50))

        # Welcome message
        welcome_message = base_font.render(f"Welcome {username}!", True, (255, 255, 255))
        screen.blit(welcome_message, ((screen_width - welcome_message.get_width()) // 2, 180))

        # Render the buttons
        pygame.draw.rect(screen, button_color, practice_button_rect)
        practice_button_label = base_font.render(practice_button_text, True, button_text_color)
        practice_button_label_rect = practice_button_label.get_rect(center=practice_button_rect.center)
        screen.blit(practice_button_label, practice_button_label_rect)

        pygame.draw.rect(screen, button_color, review_button_rect)
        review_button_label = base_font.render(review_button_text, True, button_text_color)
        review_button_label_rect = review_button_label.get_rect(center=review_button_rect.center)
        screen.blit(review_button_label, review_button_label_rect)

        # Render the score
        score_label = score_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_label, ((screen_width - score_label.get_width()) // 2, 500))

        # Render the difficulty level
        level_label = score_font.render(f"Difficulty: {level}", True, (255, 255, 255))
        screen.blit(level_label, ((screen_width - level_label.get_width()) // 2, 525))

        pygame.display.flip()
        clock.tick(60)


def login_menu():
    pygame.init()
    clock = pygame.time.Clock()
    screen_width = 700
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Sprachenspiel Log In")
    base_font = pygame.font.Font(None, 32)
    headline_font = pygame.font.Font(None, 100)
    user_text1 = ""  # Text for the first input box
    user_text2 = ""  # Text for the second input box

    # Define the fixed width for the input boxes
    fixed_input_width = 400
    input_rect1 = pygame.Rect(150, 250, fixed_input_width, 32)  # Initial position and dimensions of the first input box
    input_rect2 = pygame.Rect(150, 350, fixed_input_width,
                              32)  # Initial position and dimensions of the second input box

    # Define the "Log In" button
    button_rect = pygame.Rect(150, 450, 400, 50)
    button_color = pygame.Color("red")
    button_text = "Log In"
    button_font = pygame.font.Font(None, 40)

    color_active = pygame.Color("white")
    color_inactive = pygame.Color("gray15")
    # color1 = color_inactive
    # color2 = color_inactive
    active1 = False
    active2 = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle mouse click events for the first input box
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect1.collidepoint(event.pos):
                    active1 = True
                    active2 = False  # Deactivate the second input box
                else:
                    active1 = False

            # Handle mouse click events for the second input box
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect2.collidepoint(event.pos):
                    active2 = True
                    active1 = False  # Deactivate the first input box
                else:
                    active2 = False

            # Handle mouse click events for the "Log In" button
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    # Perform login action here (you can add your logic)
                    print("Logging in...")
                    print("Username:", user_text1)
                    print("Password:", user_text2)
                    # Display the new menu
                    main_menu(user_text1)

            # Handle keyboard events for the first input box
            if event.type == pygame.KEYDOWN:
                if active1:
                    if event.key == pygame.K_BACKSPACE:
                        user_text1 = user_text1[:-1]
                    elif len(user_text1) < 20:  # Limiting user to use only 20 characters
                        user_text1 += event.unicode

            # Handle keyboard events for the second input box
            if event.type == pygame.KEYDOWN:
                if active2:
                    if event.key == pygame.K_BACKSPACE:
                        user_text2 = user_text2[:-1]
                    elif len(user_text2) < 20:  # Limiting user to use only 20 characters
                        user_text2 += event.unicode

        screen.fill((0, 0, 0))

        # Headline label
        headline_label = headline_font.render("Sprachenspiel", True, (255, 255, 255))
        screen.blit(headline_label, (102, 50))

        # Render text labels above the input boxes
        label1 = base_font.render("Username:", True, (255, 255, 255))
        screen.blit(label1, (input_rect1.x, input_rect1.y - 30))

        label2 = base_font.render("Password:", True, (255, 255, 255))
        screen.blit(label2, (input_rect2.x, input_rect2.y - 30))

        # Determine the color for the first input box
        color1 = color_active if active1 else color_inactive
        pygame.draw.rect(screen, color1, input_rect1, 3)
        text_surface1 = base_font.render(user_text1, True, (255, 255, 255))
        screen.blit(text_surface1, (input_rect1.x + 5, input_rect1.y + 5))

        # Determine the color for the second input box
        color2 = color_active if active2 else color_inactive
        pygame.draw.rect(screen, color2, input_rect2, 3)
        text_surface2 = base_font.render(user_text2, True, (255, 255, 255))
        screen.blit(text_surface2, (input_rect2.x + 5, input_rect2.y + 5))

        # Render the "Log In" button
        pygame.draw.rect(screen, button_color, button_rect)
        button_label = button_font.render(button_text, True, (255, 255, 255))
        button_label_rect = button_label.get_rect(center=button_rect.center)
        screen.blit(button_label, button_label_rect)

        pygame.display.flip()
        clock.tick(60)


login_menu()
