import pygame
import random
from deep_translator import GoogleTranslator


class VocabularyExercise:
    def __init__(self, screen):
        self.screen = screen
        self.left_buttons = []
        self.right_buttons = []
        self.selected_left_button = None
        self.selected_right_button = None
        self.correct_pairs = set()
        self.left_clickable = [True] * 7
        self.right_clickable = [True] * 7

        # Define button properties
        button_width = 150
        button_height = 50
        button_spacing = 40  # Adjusted spacing between buttons

        # English and German word lists (replace with your own words)
        self.english_words = ["Dog", "Cat", "Bird", "Horse", "Fish", "Mouse", "Elephant"]
        self.german_words = ["Hund", "Katze", "Vogel", "Pferd", "Fisch", "Maus", "Elefant"]

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

    def handle_click(self, pos):
        for i, (button_rect, english_word) in enumerate(self.left_buttons):
            if button_rect.collidepoint(pos) and self.left_clickable[i]:
                self.selected_left_button = (button_rect, english_word)
                return

        for i, (button_rect, german_word) in enumerate(self.right_buttons):
            if button_rect.collidepoint(pos) and self.right_clickable[i]:
                translated_word = GoogleTranslator(source='german', target='english').translate(german_word)
                self.selected_right_button = (button_rect, translated_word)
                return

        self.selected_left_button = None
        self.selected_right_button = None

    def check_correctness(self):
        if self.selected_left_button and self.selected_right_button:
            left_button_rect, german_word = self.selected_left_button
            right_button_rect, english_word = self.selected_right_button
            if german_word.lower() == english_word.lower():  # Case-insensitive comparison
                self.correct_pairs.add((german_word, english_word))  # Store German and English word pair
                self.selected_left_button = None
                self.selected_right_button = None
                return True
            else:
                self.selected_left_button = None
                self.selected_right_button = None
                return False

    def update_clickable(self):
        for german_word, english_word in self.correct_pairs:
            # Re-translate the English word back to German
            retranslated_german_word = GoogleTranslator(source='english', target='german').translate(english_word)
            for i, (left_button_rect, left_word_check) in enumerate(self.left_buttons):
                if left_word_check.strip().lower() == german_word.strip().lower():  # Case-insensitive comparison
                    self.left_clickable[i] = False
            for i, (right_button_rect, right_word_check) in enumerate(self.right_buttons):
                if right_word_check.strip().lower() == retranslated_german_word.strip().lower():  # Case-insensitive comparison
                    self.right_clickable[i] = False

    def draw(self):
        self.screen.fill((0, 0, 0))  # Clear the screen

        # Draw left buttons with English words
        for i, (button_rect, english_word) in enumerate(self.left_buttons):
            color = (255, 255, 255) if self.left_clickable[i] else (150, 150, 150)
            pygame.draw.rect(self.screen, color, button_rect)  # White fill
            pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2)  # Black border
            button_font = pygame.font.Font(None, 24)
            button_text = button_font.render(english_word, True, (0, 0, 0))
            button_text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, button_text_rect)

        # Draw right buttons with German words
        for i, (button_rect, german_word) in enumerate(self.right_buttons):
            color = (255, 255, 255) if self.right_clickable[i] else (150, 150, 150)
            pygame.draw.rect(self.screen, color, button_rect)  # White fill
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

        # Draw green border and fill for correct pairs
        for left_word, right_word in self.correct_pairs:
            left_button_rects = [button_rect for button_rect, word in self.left_buttons if word == left_word]
            right_button_rects = [button_rect for button_rect, word in self.right_buttons if word == right_word]
            if left_button_rects and right_button_rects:
                left_button_rect = left_button_rects[0]
                right_button_rect = right_button_rects[0]
                pygame.draw.rect(self.screen, (0, 255, 0), left_button_rect, 2)  # Green border for left button
                pygame.draw.rect(self.screen, (0, 255, 0), right_button_rect, 2)  # Green border for right button
                if not self.left_clickable[self.left_buttons.index((left_button_rect, left_word))]:
                    pygame.draw.rect(self.screen, (0, 255, 0), left_button_rect)  # Green fill for left button
                if not self.right_clickable[self.right_buttons.index((right_button_rect, right_word))]:
                    pygame.draw.rect(self.screen, (0, 255, 0), right_button_rect)  # Green fill for right button

        pygame.display.flip()  # Flip the screen after all drawing operations


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
                correct = exercise.check_correctness()  # Check correctness after each click
                if correct:
                    exercise.update_clickable()

        exercise.draw()

    pygame.quit()
