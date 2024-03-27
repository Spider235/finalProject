import pygame
from gtts import gTTS
import os
import tempfile
import speech_recognition as sr


class GermanPronunciationExercise:
    def __init__(self, screen):
        self.screen = screen
        self.word = "Bruder"  # Example German word
        self.button_width = 200
        self.button_height = 80
        self.button_spacing = 20
        self.button_x = (screen.get_width() - self.button_width) // 2
        self.play_button_y = (screen.get_height() - (self.button_height * 2 + self.button_spacing)) // 2
        self.record_button_y = self.play_button_y + self.button_height + self.button_spacing
        self.play_button_rect = pygame.Rect(self.button_x, self.play_button_y, self.button_width, self.button_height)
        self.record_button_rect = pygame.Rect(self.button_x, self.record_button_y, self.button_width, self.button_height)
        self.text_font = pygame.font.Font(None, 36)

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
            else:
                print("Incorrect pronunciation. Try again.")
        except sr.UnknownValueError:
            print("Could not understand audio")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

    def draw(self):
        background_image = pygame.image.load("images/ex3.png")
        self.screen.blit(background_image, (0, 0))

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

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button_rect.collidepoint(event.pos):
                    self.play_word()
                elif self.record_button_rect.collidepoint(event.pos):
                    self.record_and_check()
        return True

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            pygame.display.flip()


if __name__ == "__main__":
    pygame.init()
    screen_width = 700
    screen_height = 700
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("German Pronunciation Exercise")

    exercise = GermanPronunciationExercise(screen)
    exercise.run()

    pygame.quit()
