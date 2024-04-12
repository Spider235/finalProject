import pygame
from gtts import gTTS
import os
import tempfile
import speech_recognition as sr


class GermanPronunciationExercise:
    def __init__(self, screen):
        pygame.font.init()
        self.screen = screen
        self.word = "Bruder"  # Example German word
        self.button_width = 200
        self.button_height = 80
        self.button_spacing = 20
        self.button_x = (700 - self.button_width) // 2
        self.play_button_y = (700 - (self.button_height * 2 + self.button_spacing)) // 2
        self.record_button_y = self.play_button_y + self.button_height + self.button_spacing
        self.play_button_rect = pygame.Rect(self.button_x, self.play_button_y, self.button_width, self.button_height)
        self.record_button_rect = pygame.Rect(self.button_x, self.record_button_y, self.button_width, self.button_height)
        self.text_font = pygame.font.Font(None, 32)
        self.score = 0  # Initialize score counter
        self.completed_correctly = False  # Flag to track if the exercise is completed correctly
        self.next_button_width = 100
        self.next_button_height = 50
        self.next_button_font = pygame.font.Font(None, 24)
        self.next_button_color = (200, 200, 200)
        self.next_button_rect = pygame.Rect((700 - self.next_button_width) // 2, 600,
                                            self.next_button_width, self.next_button_height)

    def play_word(self):
        tts = gTTS(text=self.word, lang='de')
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
            tts.write_to_fp(temp_file)
            temp_file.close()
            pygame.mixer.init()
            pygame.mixer.music.load(temp_file.name)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():  # Wait for sound playback to finish
                pygame.time.Clock().tick(10)  # Check every 10 milliseconds
            pygame.mixer.music.stop()  # Stop the playback after it finishes

    def record_and_check(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Speak the word:")
            audio = recognizer.listen(source)
        try:
            user_input = recognizer.recognize_google(audio, language='de-DE')
            if user_input.lower() == self.word.lower():
                print("Correct pronunciation!")
                self.score += 100
                self.completed_correctly = True  # Set the flag if pronunciation is correct
            else:
                print("Incorrect pronunciation. Try again.")
                self.score = max(0, self.score - 50)  # Ensure score doesn't go below 0
                self.completed_correctly = False  # Reset the flag if pronunciation is incorrect
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

    def draw(self):
        background_image = pygame.image.load("images/ex3.png")
        self.screen.blit(background_image, (0, 0))

        # Display score on the screen
        score_text = self.text_font.render(f"Score: {self.score}", True, (0, 0, 0))
        score_text_rect = score_text.get_rect(center=(self.screen.get_width() // 2, 50))
        self.screen.blit(score_text, score_text_rect)

        pygame.draw.rect(self.screen, (0, 255, 0), self.play_button_rect)
        pygame.draw.rect(self.screen, (255, 0, 0), self.record_button_rect)

        play_button_text = self.text_font.render("Play Sound", True, (0, 0, 0))
        play_button_text_rect = play_button_text.get_rect(center=self.play_button_rect.center)
        self.screen.blit(play_button_text, play_button_text_rect)

        record_button_text = self.text_font.render("Record", True, (0, 0, 0))
        record_button_text_rect = record_button_text.get_rect(center=self.record_button_rect.center)
        self.screen.blit(record_button_text, record_button_text_rect)

        word_text = self.text_font.render(self.word, True, (0, 0, 0))
        word_text_rect = word_text.get_rect(center=(self.screen.get_width() // 2, 200))
        self.screen.blit(word_text, word_text_rect)

        if self.completed_correctly:
            # Draw the Next button if exercise completed correctly
            pygame.draw.rect(self.screen, self.next_button_color, self.next_button_rect)
            next_button_text = self.next_button_font.render("Next", True, (0, 0, 0))
            next_button_text_rect = next_button_text.get_rect(center=self.next_button_rect.center)
            self.screen.blit(next_button_text, next_button_text_rect)

        pygame.display.flip()

    def next_button_clicked(self, pos):
        if self.next_button_rect.collidepoint(pos):
            # Move to the next exercise (replace with the instantiation of the next exercise class)
            # next_exercise = GermanPronunciationExercise(self.screen)
            # next_exercise.run()
            return True  # Return True to indicate that the button click was handled
        return False  # Return False if the button click was not handled

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.next_button_clicked(event.pos):  # Check if the Next button was clicked
                    return False  # Exit the loop if the Next button was clicked

                # Check if the Play Sound button was clicked
                if self.play_button_rect.collidepoint(event.pos):
                    self.play_word()

                # Check if the Record button was clicked
                if self.record_button_rect.collidepoint(event.pos):
                    self.record_and_check()
        return True

    def completed(self):
        return self.completed_correctly

    def reset(self):
        # Reset all relevant attributes to their initial state
        self.score = 0
        self.completed_correctly = False

    def run(self):
        running = True
        while running:
            # Handle events
            running = self.handle_events()

            # Draw elements
            self.draw()


if __name__ == "__main__":
    pygame.init()
    screen_width = 700
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("German Pronunciation Exercise")

    exercise = GermanPronunciationExercise(screen)
    exercise.run()

    pygame.quit()
