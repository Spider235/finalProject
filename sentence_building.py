import pygame
import random
import time
from deep_translator import GoogleTranslator

from pronunciation import GermanPronunciationExercise


class SentenceExerciseGerman:  # This class is used to build sentences in German.
    def __init__(self, screen):
        self.screen = screen
        self.background_image = pygame.image.load(
            r"C:\Users\nurim\PycharmProjects\finalProject\images\ex1.png")  # Load the background image
        self.background_image = pygame.transform.scale(self.background_image, (
            screen.get_width(), screen.get_height()))  # Scale the image to fit the screen
        self.animal_image = pygame.image.load(
            r"C:\Users\nurim\PycharmProjects\finalProject\images\traced-cat.jpg")  # Load the image of the animal
        self.animal_image = pygame.transform.scale(self.animal_image, (275, 275))  # Scale the image
        self.sentence_font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 24)
        self.sentence = "My brother is very tall"  # Updated English sentence
        self.german_words = ["Mein", "Bruder", "ist", "sehr", "groß", "klein", "schwer", "dünn", "klug",
                             "stark"]  # Example German words (replace with your own)
        random.shuffle(self.german_words)
        self.selected_words = []  # Store selected German words for building the sentence
        self.selected_rects = []  # Store rects of selected buttons
        self.score = 0  # Initialize score counter
        self.correct_sound = pygame.mixer.Sound(r"C:\Users\nurim\PycharmProjects\finalProject\Sounds\correct.wav")
        self.wrong_sound = pygame.mixer.Sound(r"C:\Users\nurim\PycharmProjects\finalProject\Sounds\wrong.wav")
        # Define button properties
        self.button_width = 100
        self.button_height = 50
        self.button_spacing = 20
        self.button_margin_x = 62
        self.button_margin_y = 550
        self.buttons = []
        self.correctness_checked = False
        self.correct_sentence_matched = False
        # Define message properties
        self.message_box_font = pygame.font.Font(None, 36)
        self.message_box_color = (255, 255, 255)
        self.message_timer = 0
        self.message_text = ""
        # Define check button properties
        self.check_button_width = 100
        self.check_button_height = 50
        self.check_button_font = pygame.font.Font(None, 24)
        self.check_button_color = (200, 200, 200)
        self.check_button_rect = pygame.Rect((screen.get_width() - self.check_button_width) // 2, 450,
                                             self.check_button_width, self.check_button_height)
        # Define next button properties
        self.next_button_width = 100
        self.next_button_height = 50
        self.next_button_font = pygame.font.Font(None, 24)
        self.next_button_color = (200, 200, 200)
        self.next_button_rect = pygame.Rect((screen.get_width() - self.next_button_width) // 2, 600,
                                            self.next_button_width, self.next_button_height)

        # Create buttons with German words
        for i, word in enumerate(self.german_words):
            button_x = self.button_margin_x + (i % 5) * (self.button_width + self.button_spacing)
            button_y = self.button_margin_y + (i // 5) * (self.button_height + self.button_spacing)
            button_rect = pygame.Rect(button_x, button_y, self.button_width, self.button_height)
            self.buttons.append((button_rect, word))

        # Create the "Check" button
        self.check_button = pygame.Rect(300, 480, 100, 40)

    def handle_click(self, pos):
        if self.check_button.collidepoint(pos):
            self.check_correctness()  # Check correctness when the "Check" button is clicked
            return

        max_buttons_per_line = 5
        buttons_in_current_line = len(self.selected_rects) % max_buttons_per_line
        y_offset = 100  # Initial y-offset for the buttons (adjust this value as needed)
        y_offset_increment = self.button_height + self.button_spacing

        for button_rect, word in self.buttons:
            if button_rect.collidepoint(pos):
                if word in self.selected_words:
                    index = self.selected_words.index(word)
                    del self.selected_words[index]
                    del self.selected_rects[index]
                else:
                    if buttons_in_current_line == max_buttons_per_line:
                        y_offset += y_offset_increment
                        buttons_in_current_line = 0

                    if not self.selected_words:
                        x_offset = 20  # Initial x-offset for the first selected button
                    else:
                        last_rect = self.selected_rects[-1][0]  # Get the rect of the last selected button
                        if buttons_in_current_line == 0:
                            x_offset = 20  # Reset x-offset to start a new line
                        else:
                            x_offset = last_rect.x + last_rect.width + self.button_spacing  # Calculate x-offset for the new button

                    new_rect = button_rect.copy()  # Create a copy of the button rect
                    new_rect.x = x_offset  # Set the x-coordinate for the new button
                    new_rect.y = y_offset  # Set the y-coordinate for the new button
                    self.selected_words.append(word)
                    self.selected_rects.append((new_rect, word))
                    buttons_in_current_line += 1

    def check_correctness(self):
        # Step 2: Define the German translation of the English sentence
        german_translation = GoogleTranslator(source='english', target='german').translate(self.sentence)

        # Step 3: Retrieve the German translation of the user-built sentence
        user_german_sentence = ' '.join(word for word in self.selected_words)

        # Step 4: Normalize sentences for comparison (remove punctuation and convert to lowercase)
        user_german_sentence_normalized = user_german_sentence.replace('.', '').lower()
        german_translation_normalized = german_translation.replace('.', '').lower()

        # Step 5: Compare normalized sentences
        self.correct_sentence_matched = user_german_sentence_normalized == german_translation_normalized

        if self.correct_sentence_matched:
            self.correct_sound.play()  # Play correct sound
            self.show_message(random.choice(["Amazing", "Awesome", "Great!", "Wonderful!"]))
            self.score += 100
        else:
            self.wrong_sound.play()  # Play correct sound
            self.show_message("Try again")
            self.score = max(0, self.score - 50)

        # Set the flag to indicate that correctness has been checked
        self.correctness_checked = True

    def check_correctness_for_next_button(self):
        english_translation = GoogleTranslator(source='german', target='english').translate(self.sentence)
        user_english_sentence = ' '.join(word for word in self.selected_words)
        user_english_sentence_normalized = user_english_sentence.replace('.', '').lower()
        english_translation_normalized = english_translation.replace('.', '').lower()
        if user_english_sentence_normalized == english_translation_normalized:
            return True
        else:
            return False

    def draw(self):
        # Draw the background image
        self.screen.blit(self.background_image, (0, 0))

        # Draw the animal image
        image_rect = self.animal_image.get_rect(center=(150, 110))
        self.screen.blit(self.animal_image, image_rect)

        # Draw the English sentence at the top
        sentence_surface = self.sentence_font.render(self.sentence, True, (0, 0, 0))
        sentence_rect = sentence_surface.get_rect(center=(450, 125))
        self.screen.blit(sentence_surface, sentence_rect)

        # Draw the Check button
        pygame.draw.rect(self.screen, self.check_button_color, self.check_button_rect)
        check_button_text = self.check_button_font.render("Check", True, (0, 0, 0))
        check_button_text_rect = check_button_text.get_rect(center=self.check_button_rect.center)
        self.screen.blit(check_button_text, check_button_text_rect)

        # Draw score on the top middle of the screen
        score_text = self.button_font.render(f"Score: {self.score}", True, (0, 0, 0))
        score_rect = score_text.get_rect(center=(350, 50))
        self.screen.blit(score_text, score_rect)

        # Draw buttons with German words
        for button_rect, word in self.buttons:
            color = (200, 200, 200) if word in self.selected_words else (150, 150, 150)
            pygame.draw.rect(self.screen, color, button_rect)  # Button fill
            pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2)  # Button border
            button_text = self.button_font.render(word, True, (0, 0, 0))
            button_text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, button_text_rect)

        # Draw selected words on the left side
        for i, (rect, word) in enumerate(self.selected_rects):
            x_offset = 80
            y_offset = 250
            max_buttons_per_line = 5
            spacing = 10  # Adjust the spacing between buttons
            if i >= max_buttons_per_line:
                x_offset += (self.button_width + spacing) * (i % max_buttons_per_line)
                y_offset += self.button_height + self.button_spacing
            else:
                x_offset += (self.button_width + spacing) * i
            rect.x = x_offset
            rect.y = y_offset
            pygame.draw.rect(self.screen, (200, 200, 200), rect)  # Button fill
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)  # Button border
            button_text = self.button_font.render(word, True, (0, 0, 0))
            button_text_rect = button_text.get_rect(center=rect.center)
            self.screen.blit(button_text, button_text_rect)

        # Draw message box if necessary
        if time.time() < self.message_timer:
            message_surface = self.message_box_font.render(self.message_text, True, (0, 0, 0))
            message_rect = message_surface.get_rect(center=(250, 75))
            pygame.draw.rect(self.screen, self.message_box_color, message_rect)  # Draw message box background
            pygame.draw.rect(self.screen, (0, 0, 0), message_rect, 2)  # Draw message box border
            self.screen.blit(message_surface, message_rect.topleft)

        # Check if the exercise is completed
        if self.completed():
            # Draw the next button
            next_button_y_offset = 500  # Adjust the vertical position of the next button
            self.next_button_rect.y = next_button_y_offset
            pygame.draw.rect(self.screen, self.next_button_color, self.next_button_rect)
            next_button_text = self.next_button_font.render("Next", True, (0, 0, 0))
            next_button_text_rect = next_button_text.get_rect(center=self.next_button_rect.center)
            self.screen.blit(next_button_text, next_button_text_rect)

        # Update the display
        pygame.display.flip()

        pygame.display.flip()  # Flip the screen after all drawing operations

    def show_message(self, text):
        self.message_text = text
        self.message_timer = time.time() + 2  # Display message for 2 seconds

    def check_button_clicked(self, pos):
        return self.check_button_rect.collidepoint(pos)

    def next_button_clicked(self, pos):
        if self.next_button_rect.collidepoint(pos):
            # Move to the next exercise (replace with the instantiation of the next exercise class)
            next_exercise = SentenceExerciseEnglish(self.screen)
            next_exercise.run(self.screen)
            return True  # Return True to indicate that the button click was handled
        return False  # Return False if the button click was not handled

    def completed(self):
        # Join the selected words to form the user's sentence
        user_sentence = ' '.join(self.selected_words)

        # Translate the displayed English sentence to German for comparison
        correct_german_sentence = GoogleTranslator(source='english', target='german').translate(self.sentence)

        # Normalize both sentences for comparison
        user_sentence_normalized = user_sentence.replace('.', '').lower()
        correct_german_sentence_normalized = correct_german_sentence.replace('.', '').lower()

        # Check if the correctness of the user's sentence has been verified
        return self.correctness_checked and self.correct_sentence_matched

    def run(self, screen):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.next_button_clicked(event.pos):
                        # Move to the next exercise (replace with the instantiation of the next exercise class)
                        next_exercise = SentenceExerciseEnglish(screen)
                        next_exercise.run(screen)
                        return  # Exit the current run method after moving to the next exercise
                    elif self.check_button_clicked(event.pos):
                        self.check_correctness()
                    else:
                        self.handle_click(event.pos)

            self.draw()

        pygame.quit()


class SentenceExerciseEnglish:  # This class is used to build sentences in German.
    def __init__(self, screen):
        self.screen = screen
        self.background_image = pygame.image.load(
            r"C:\Users\nurim\PycharmProjects\finalProject\images\ex1.png")  # Load the background image
        self.background_image = pygame.transform.scale(self.background_image, (
            screen.get_width(), screen.get_height()))  # Scale the image to fit the screen
        self.animal_image = pygame.image.load(
            r"C:\Users\nurim\PycharmProjects\finalProject\images\traced-cat.jpg")  # Load the image of the animal
        self.animal_image = pygame.transform.scale(self.animal_image, (275, 275))  # Scale the image
        self.sentence_font = pygame.font.Font(None, 36)
        self.button_font = pygame.font.Font(None, 24)
        self.sentence = "Mein Bruder ist sehr groß"  # Updated German sentence
        self.german_words = ["My", "Brother", "is", "very", "tall", "small", "difficult", "thin", "smart",
                             "strong"]  # Example German words (replace with your own)
        random.shuffle(self.german_words)
        self.selected_words = []  # Store selected German words for building the sentence
        self.selected_rects = []  # Store rects of selected buttons
        self.score = 0  # Initialize score counter
        self.correct_sound = pygame.mixer.Sound(r"C:\Users\nurim\PycharmProjects\finalProject\Sounds\correct.wav")
        self.wrong_sound = pygame.mixer.Sound(r"C:\Users\nurim\PycharmProjects\finalProject\Sounds\wrong.wav")
        # Define button properties
        self.button_width = 100
        self.button_height = 50
        self.button_spacing = 20
        self.button_margin_x = 62
        self.button_margin_y = 550
        self.buttons = []
        self.correctness_checked = False
        self.correct_sentence_matched = False
        # Define message properties
        self.message_box_font = pygame.font.Font(None, 36)
        self.message_box_color = (255, 255, 255)
        self.message_timer = 0
        self.message_text = ""
        # Define check button properties
        self.check_button_width = 100
        self.check_button_height = 50
        self.check_button_font = pygame.font.Font(None, 24)
        self.check_button_color = (200, 200, 200)
        self.check_button_rect = pygame.Rect((screen.get_width() - self.check_button_width) // 2, 450,
                                             self.check_button_width, self.check_button_height)
        # Define next button properties
        self.next_button_width = 100
        self.next_button_height = 50
        self.next_button_font = pygame.font.Font(None, 24)
        self.next_button_color = (200, 200, 200)
        self.next_button_rect = pygame.Rect((screen.get_width() - self.next_button_width) // 2, 600,
                                            self.next_button_width, self.next_button_height)

        # Create buttons with German words
        for i, word in enumerate(self.german_words):
            button_x = self.button_margin_x + (i % 5) * (self.button_width + self.button_spacing)
            button_y = self.button_margin_y + (i // 5) * (self.button_height + self.button_spacing)
            button_rect = pygame.Rect(button_x, button_y, self.button_width, self.button_height)
            self.buttons.append((button_rect, word))

        # Create the "Check" button
        self.check_button = pygame.Rect(300, 480, 100, 40)

    def handle_click(self, pos):
        if self.check_button.collidepoint(pos):
            self.check_correctness()  # Check correctness when the "Check" button is clicked
            return

        max_buttons_per_line = 5
        buttons_in_current_line = len(self.selected_rects) % max_buttons_per_line
        y_offset = 100  # Initial y-offset for the buttons (adjust this value as needed)
        y_offset_increment = self.button_height + self.button_spacing

        for button_rect, word in self.buttons:
            if button_rect.collidepoint(pos):
                if word in self.selected_words:
                    index = self.selected_words.index(word)
                    del self.selected_words[index]
                    del self.selected_rects[index]
                else:
                    if buttons_in_current_line == max_buttons_per_line:
                        y_offset += y_offset_increment
                        buttons_in_current_line = 0

                    if not self.selected_words:
                        x_offset = 20  # Initial x-offset for the first selected button
                    else:
                        last_rect = self.selected_rects[-1][0]  # Get the rect of the last selected button
                        if buttons_in_current_line == 0:
                            x_offset = 20  # Reset x-offset to start a new line
                        else:
                            x_offset = last_rect.x + last_rect.width + self.button_spacing  # Calculate x-offset for the new button

                    new_rect = button_rect.copy()  # Create a copy of the button rect
                    new_rect.x = x_offset  # Set the x-coordinate for the new button
                    new_rect.y = y_offset  # Set the y-coordinate for the new button
                    self.selected_words.append(word)
                    self.selected_rects.append((new_rect, word))
                    buttons_in_current_line += 1

    def check_correctness(self):
        # Step 2: Define the German translation of the English sentence
        german_translation = GoogleTranslator(source='german', target='english').translate(self.sentence)

        # Step 3: Retrieve the German translation of the user-built sentence
        user_german_sentence = ' '.join(word for word in self.selected_words)

        # Step 4: Normalize sentences for comparison (remove punctuation and convert to lowercase)
        user_german_sentence_normalized = user_german_sentence.replace('.', '').lower()
        german_translation_normalized = german_translation.replace('.', '').lower()

        # Step 5: Compare normalized sentences
        self.correct_sentence_matched = user_german_sentence_normalized == german_translation_normalized

        if self.correct_sentence_matched:
            self.correct_sound.play()  # Play correct sound
            self.show_message(random.choice(["Amazing", "Awesome", "Great!", "Wonderful!"]))
            self.score += 100
        else:
            self.wrong_sound.play()  # Play correct sound
            self.show_message("Try again")
            self.score = max(0, self.score - 50)

        # Set the flag to indicate that correctness has been checked
        self.correctness_checked = True

    def check_correctness_for_next_button(self):
        english_translation = GoogleTranslator(source='english', target='german').translate(self.sentence)
        user_english_sentence = ' '.join(word for word in self.selected_words)
        user_english_sentence_normalized = user_english_sentence.replace('.', '').lower()
        english_translation_normalized = english_translation.replace('.', '').lower()
        if user_english_sentence_normalized == english_translation_normalized:
            return True
        else:
            return False

    def draw(self):
        # Draw the background image
        self.screen.blit(self.background_image, (0, 0))

        # Draw the animal image
        image_rect = self.animal_image.get_rect(center=(150, 110))
        self.screen.blit(self.animal_image, image_rect)

        # Draw the English sentence at the top
        sentence_surface = self.sentence_font.render(self.sentence, True, (0, 0, 0))
        sentence_rect = sentence_surface.get_rect(center=(450, 125))
        self.screen.blit(sentence_surface, sentence_rect)

        # Draw the Check button
        pygame.draw.rect(self.screen, self.check_button_color, self.check_button_rect)
        check_button_text = self.check_button_font.render("Check", True, (0, 0, 0))
        check_button_text_rect = check_button_text.get_rect(center=self.check_button_rect.center)
        self.screen.blit(check_button_text, check_button_text_rect)

        # Draw score on the top middle of the screen
        score_text = self.button_font.render(f"Score: {self.score}", True, (0, 0, 0))
        score_rect = score_text.get_rect(center=(350, 50))
        self.screen.blit(score_text, score_rect)

        # Draw buttons with German words
        for button_rect, word in self.buttons:
            color = (200, 200, 200) if word in self.selected_words else (150, 150, 150)
            pygame.draw.rect(self.screen, color, button_rect)  # Button fill
            pygame.draw.rect(self.screen, (0, 0, 0), button_rect, 2)  # Button border
            button_text = self.button_font.render(word, True, (0, 0, 0))
            button_text_rect = button_text.get_rect(center=button_rect.center)
            self.screen.blit(button_text, button_text_rect)

        # Draw selected words on the left side
        for i, (rect, word) in enumerate(self.selected_rects):
            x_offset = 80
            y_offset = 250
            max_buttons_per_line = 5
            spacing = 10  # Adjust the spacing between buttons
            if i >= max_buttons_per_line:
                x_offset += (self.button_width + spacing) * (i % max_buttons_per_line)
                y_offset += self.button_height + self.button_spacing
            else:
                x_offset += (self.button_width + spacing) * i
            rect.x = x_offset
            rect.y = y_offset
            pygame.draw.rect(self.screen, (200, 200, 200), rect)  # Button fill
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)  # Button border
            button_text = self.button_font.render(word, True, (0, 0, 0))
            button_text_rect = button_text.get_rect(center=rect.center)
            self.screen.blit(button_text, button_text_rect)

        # Draw message box if necessary
        if time.time() < self.message_timer:
            message_surface = self.message_box_font.render(self.message_text, True, (0, 0, 0))
            message_rect = message_surface.get_rect(center=(250, 75))
            pygame.draw.rect(self.screen, self.message_box_color, message_rect)  # Draw message box background
            pygame.draw.rect(self.screen, (0, 0, 0), message_rect, 2)  # Draw message box border
            self.screen.blit(message_surface, message_rect.topleft)

        # Check if the exercise is completed
        if self.completed():
            # Draw the next button
            next_button_y_offset = 500  # Adjust the vertical position of the next button
            self.next_button_rect.y = next_button_y_offset
            pygame.draw.rect(self.screen, self.next_button_color, self.next_button_rect)
            next_button_text = self.next_button_font.render("Next", True, (0, 0, 0))
            next_button_text_rect = next_button_text.get_rect(center=self.next_button_rect.center)
            self.screen.blit(next_button_text, next_button_text_rect)

        # Update the display
        pygame.display.flip()

        pygame.display.flip()  # Flip the screen after all drawing operations

    def show_message(self, text):
        self.message_text = text
        self.message_timer = time.time() + 2  # Display message for 2 seconds

    def check_button_clicked(self, pos):
        return self.check_button_rect.collidepoint(pos)

    def next_button_clicked(self, pos):
        if self.next_button_rect.collidepoint(pos):
            # Move to the next exercise (replace with the instantiation of the next exercise class)
            next_exercise = GermanPronunciationExercise(self.screen)
            next_exercise.run()
            return True  # Return True to indicate that the button click was handled
        return False  # Return False if the button click was not handled

    def completed(self):
        # Join the selected words to form the user's sentence
        user_sentence = ' '.join(self.selected_words)

        # Translate the displayed English sentence to German for comparison
        correct_german_sentence = GoogleTranslator(source='english', target='german').translate(self.sentence)

        # Normalize both sentences for comparison
        user_sentence_normalized = user_sentence.replace('.', '').lower()
        correct_german_sentence_normalized = correct_german_sentence.replace('.', '').lower()

        # Check if the correctness of the user's sentence has been verified
        return self.correctness_checked and self.correct_sentence_matched

    def run(self, screen):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.next_button_clicked(event.pos):
                        # Move to the next exercise (replace with the instantiation of the next exercise class)
                        next_exercise = GermanPronunciationExercise(screen)
                        next_exercise.run()
                        return  # Exit the current run method after moving to the next exercise
                    elif self.check_button_clicked(event.pos):
                        self.check_correctness()
                    else:
                        self.handle_click(event.pos)

            self.draw()

        pygame.quit()


if __name__ == "__main__":
    pygame.init()
    screen_width = 700
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Sentence Exercise")

    exercise = SentenceExerciseGerman(screen)  # chnage it accoringly for the exercise

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if exercise.check_button_clicked(event.pos):
                    exercise.check_correctness()
                else:
                    exercise.handle_click(event.pos)

        exercise.draw()

    pygame.quit()
