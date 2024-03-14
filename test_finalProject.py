import pygame
import sys


def display_new_menu():
    pygame.init()
    new_menu_width = 500
    new_menu_height = 500
    new_menu_screen = pygame.display.set_mode((new_menu_width, new_menu_height))
    pygame.display.set_caption("New Menu")

    # Placeholder content for the new menu
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        new_menu_screen.fill((255, 255, 255))  # Fill the new menu screen with white
        pygame.display.flip()
    pygame.quit()
    sys.exit()


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
                    display_new_menu()

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
        screen.blit(headline_label, (100, 45))

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
