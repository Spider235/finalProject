import pygame
import random
from deep_translator import GoogleTranslator


class VocabularyExercise:
    def __init__(self, screen):
        self.screen = screen
        self.left_buttons = []
        self.right_buttons = []

        # Define button properties
        button_width = 150
        button_height = 50
        button_spacing = 40  # Adjusted spacing between buttons

        # English and German word lists (replace with your own words)
        self.english_words = ["Dog", "Cat", "Bird", "Horse", "Rabbit", "Mouse", "Elephant"]
        self.german_words = ["Hund", "Katze", "Vogel", "Pferd", "Kanin", "Maus", "Elefant"]

        # Randomly shuffle word lists
        random.shuffle(self.english_words)
        random.shuffle(self.german_words)

        # Create left buttons with English words
        left_button_x = 50
        left_button_y = 50
        for i, english_word in enumerate(self.english_words[:7]):  # Select first 7 English words
            left_button_rect = pygame.Rect(left_button_x, left_button_y + i * (button_height + button_spacing),
                                           button_width, button_height)
            self.left_buttons.append((left_button_rect, english_word))

        # Create right buttons with German words
        right_button_x = 500
        right_button_y = 50
        for i, german_word in enumerate(self.german_words[:7]):  # Select first 7 German words
            right_button_rect = pygame.Rect(right_button_x, right_button_y + i * (button_height + button_spacing),
                                            button_width, button_height)
            self.right_buttons.append((right_button_rect, german_word))

        # Variables to track selected buttons and correctness
        self.selected_left_button = None
        self.selected_right_button = None
        self.correct_pair = None

    def handle_click(self, pos):
        # Check if a left button is clicked
        for button_rect, english_word in self.left_buttons:
            if button_rect.collidepoint(pos):
                self.selected_left_button = (button_rect, english_word)
                return

        # Check if a right button is clicked
        for button_rect, german_word in self.right_buttons:
            if button_rect.collidepoint(pos):
                # Translate the German word to English on button click
                translated_word = GoogleTranslator(source='german', target='english').translate(german_word)
                self.selected_right_button = (button_rect, translated_word)
                return

        # If no button is clicked, reset selections
        self.selected_left_button = None
        self.selected_right_button = None

    def check_correctness(self):
        if self.selected_left_button and self.selected_right_button:
            left_button_rect, english_word = self.selected_left_button
            right_button_rect, translated_word = self.selected_right_button

            # Convert both words to lowercase for case-insensitive comparison
            english_word_lower = english_word.lower()
            translated_word_lower = translated_word.lower()

            # Check if the lowercase English word matches the lowercase translated word
            if english_word_lower == translated_word_lower:
                self.correct_pair = (self.selected_left_button, self.selected_right_button)
                print("Correct")  # Debug print statement
            else:
                self.correct_pair = None
                print("Incorrect")  # Debug print statement

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear the screen

        # Draw left buttons with English words
        for button_rect, english_word in self.left_buttons:
            pygame.draw.rect(self.screen, (255, 255, 255), button_rect)  # White fill
            pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2)  # Black border
            button_font = pygame.font.Font(None, 24)
            button_text = button_font.render(english_word, True, (0, 0, 0))
            button_text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, button_text_rect)

        # Draw right buttons with German words
        for button_rect, german_word in self.right_buttons:
            pygame.draw.rect(self.screen, (255, 255, 255), button_rect)  # White fill
            pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2)  # Black border
            button_font = pygame.font.Font(None, 24)
            button_text = button_font.render(german_word, True, (0, 0, 0))
            button_text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, button_text_rect)

        # Highlight selected buttons
        if self.selected_left_button:
            pygame.draw.rect(self.screen, (0, 255, 0), self.selected_left_button[0],
                             2)  # Green border for selected left button
        if self.selected_right_button:
            pygame.draw.rect(self.screen, (0, 255, 0), self.selected_right_button[0],
                             2)  # Green border for selected right button

        # Draw green border for correct pair
        if self.correct_pair:
            pygame.draw.rect(self.screen, (0, 255, 0), self.correct_pair[0][0],
                             2)  # Green border for correct left button
            pygame.draw.rect(self.screen, (0, 255, 0), self.correct_pair[1][0],
                             2)  # Green border for correct right button

        pygame.display.flip()  # Flip the screen after all drawing operations


# Example usage:
if __name__ == "__main__":
    pygame.init()
    screen_width = 700
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Vocabulary Exercise")

    exercise = VocabularyExercise(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                exercise.handle_click(event.pos)
                exercise.check_correctness()  # Check correctness after each click

        exercise.draw()

    pygame.quit()
