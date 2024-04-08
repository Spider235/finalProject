import pygame
import sys
from exersices import VocabularyExercise
from sentence_building import SentenceExerciseEnglish
from sentence_building import SentenceExerciseGerman


class Interface:
    def __init__(self):
        self.next_button_rect = None
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen_width = 700
        self.screen_height = 700
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Sprachenspiel Interface")
        self.base_font = pygame.font.Font(None, 32)
        self.headline_font = pygame.font.Font(None, 100)
        self.button_width = 200
        self.button_height = 50
        self.button_color = pygame.Color("red")
        self.button_text_color = pygame.Color("white")
        self.exercises = [VocabularyExercise(self.screen), SentenceExerciseEnglish(self.screen),
                          SentenceExerciseGerman(self.screen)]

    def review_menu(self, username):
        pygame.init()
        clock = pygame.time.Clock()
        screen_width = 700
        screen_height = 700
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Sprachenspiel Review Menu")
        base_font = pygame.font.Font(None, 32)
        headline_font = pygame.font.Font(None, 100)
        button_width = 175
        button_height = 50
        back_button_rect = pygame.Rect((screen_width - button_width) // 2, 575, button_width, button_height)
        next_page_button_rect = pygame.Rect(50, 575, button_width, button_height)
        previous_page_button_rect = pygame.Rect(screen_width - button_width - 50, 575, button_width, button_height)
        button_color = pygame.Color("red")
        button_text_color = pygame.Color("white")
        back_button_text = "Home Menu"
        next_page_button_text = "Next Page"
        previous_page_button_text = "Previous Page"
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if back_button_rect.collidepoint(event.pos):
                        self.main_menu(username)  # Go back to the main menu
                        return  # Close the review menu window

            screen.fill((0, 0, 0))

            # Headline label
            headline_label = headline_font.render("Review Menu", True, (255, 255, 255))
            screen.blit(headline_label, ((screen_width - headline_label.get_width()) // 2, 50))

            # Render the "Go Back" button
            pygame.draw.rect(screen, button_color, back_button_rect)
            back_button_label = base_font.render(back_button_text, True, button_text_color)
            back_button_label_rect = back_button_label.get_rect(center=back_button_rect.center)
            screen.blit(back_button_label, back_button_label_rect)

            # Render the "Next Page" button
            pygame.draw.rect(screen, button_color, next_page_button_rect)
            next_page_button_label = base_font.render(next_page_button_text, True, button_text_color)
            next_page_button_label_rect = next_page_button_label.get_rect(center=next_page_button_rect.center)
            screen.blit(next_page_button_label, next_page_button_label_rect)

            # Render the "Previous Page" button
            pygame.draw.rect(screen, button_color, previous_page_button_rect)
            previous_page_button_label = base_font.render(previous_page_button_text, True, button_text_color)
            previous_page_button_label_rect = previous_page_button_label.get_rect(
                center=previous_page_button_rect.center)
            screen.blit(previous_page_button_label, previous_page_button_label_rect)

            pygame.display.flip()
            clock.tick(60)

    def practice_menu(self, username, current_exercise_index=0):
        # List of exercises
        exercises = [VocabularyExercise(self.screen), SentenceExerciseGerman(self.screen), SentenceExerciseEnglish(self.screen)]  # Replace Exercise1, Exercise2, etc. with your exercise classes

        current_exercise_index = 0
        while current_exercise_index < len(exercises):
            exercise = exercises[current_exercise_index]

            # Run the current exercise
            exercise.run()

            # Wait for the user to complete the exercise
            while not exercise.completed():
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                pygame.display.flip()
                self.clock.tick(60)

            # Draw "Next" button
            self.screen.fill((0, 0, 0))
            self.draw_next_button()

            # Wait for user to click "Next" button
            next_button_clicked = False
            while not next_button_clicked:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.next_button_rect.collidepoint(event.pos):
                            next_button_clicked = True

                pygame.display.flip()
                self.clock.tick(60)

            current_exercise_index += 1

    def draw_next_button(self):
        font = pygame.font.Font(None, 36)
        next_button_text = font.render("Next", True, (255, 255, 255))
        self.next_button_rect = next_button_text.get_rect(center=(self.screen_width // 2, self.screen_height - 50))
        self.screen.blit(next_button_text, self.next_button_rect.topleft)
        
    def main_menu(self, username):
        pygame.init()
        clock = pygame.time.Clock()
        screen_width = 700
        screen_height = 700
        screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Sprachenspiel Main Menu")
        base_font = pygame.font.Font(None, 32)
        headline_font = pygame.font.Font(None, 100)
        score_font = pygame.font.Font(None, 32)

        # Load the background image
        background_image = pygame.image.load("images/ex1.png").convert()  # Load the image
        background_image = pygame.transform.scale(background_image,
                                                  (screen_width, screen_height))  # Scale the image to fit the screen

        # Load the image
        cat_image = pygame.image.load(
            "images/traced-cat.jpg")  # Change "your_image_path.jpg" to the actual path of your image
        cat_image = pygame.transform.scale(cat_image, (300, 300))  # Adjust desired_width and desired_height
        cat_image_rect = cat_image.get_rect()
        # Set the position of the image
        cat_image_rect.center = (screen_width // 2, screen_height - 75)  # Adjust the position as needed

        # Define the buttons
        button_width = 200
        button_height = 50
        button_spacing = 50
        practice_button_rect = pygame.Rect((screen_width - button_width) // 2, 275, button_width, button_height)
        review_button_rect = pygame.Rect((screen_width - button_width) // 2, 275 + button_height + button_spacing,
                                         button_width, button_height)
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
                        self.practice_menu(username)  # Open the practice menu
                        return  # Close the main menu window
                    elif review_button_rect.collidepoint(event.pos):
                        print("Review button clicked")
                        self.review_menu(username)  # Open the review menu
                        return  # Close the main menu window

            # Blit the background image onto the screen
            screen.blit(background_image, (0, 0))
            screen.blit(cat_image, cat_image_rect)

            # Headline label
            headline_label = headline_font.render("Sprachenspiel", True, (0, 0, 0))
            screen.blit(headline_label, ((screen_width - headline_label.get_width()) // 2, 50))

            # Welcome message
            welcome_message = base_font.render(f"Welcome {username}!", True, (0, 0, 0))
            screen.blit(welcome_message, ((screen_width - welcome_message.get_width()) // 2, 150))

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
            score_label = score_font.render(f"Score: {score}", True, (0, 0, 0))
            screen.blit(score_label, (70, 485))

            # Render the difficulty level
            level_label = score_font.render(f"Difficulty: {level}", True, (0, 0, 0))
            screen.blit(level_label, (525, 485))

            pygame.display.flip()
            clock.tick(60)

    def login_menu(self):
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

        # Load the background image
        background_image = pygame.image.load("images/ex1.png").convert()  # Load the image
        background_image = pygame.transform.scale(background_image,
                                                  (screen_width, screen_height))  # Scale the image to fit the screen

        # Define the fixed width for the input boxes
        fixed_input_width = 400
        input_rect1 = pygame.Rect(150, 250, fixed_input_width,
                                  32)  # Initial position and dimensions of the first input box
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
                        self.main_menu(user_text1)

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

            screen.blit(background_image, (0, 0))

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

    def run(self):
        self.login_menu()


# Main function
def main():
    interface = Interface()
    username = "Player"
    interface.practice_menu(username)


# Add a guard condition to execute code only if the module is run directly
if __name__ == "__main__":
    interface_main = Interface()
    interface_main.run()

