import playsound as playsound
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
from tkinter import *
from random_word import RandomWords


translated = GoogleTranslator(source='english', target='german').translate("klein")  # output -> Weiter so, du bist großartig
print(translated)
translatedd = GoogleTranslator(source='german', target='english').translate("stark")  # output -> Weiter so, du bist großartig
print(translatedd)

# The text that you want to convert to audio
mytext = 'Mein Bruder ist sehr groß'

# Language in which you want to convert
language = 'de'

# Passing the text and language to the engine,
# here we have marked slow=False. Which tells
# the module that the converted audio should
# have a high speed
myobj = gTTS(text=mytext, lang=language, slow=False)
myobj.save("welcome.mp3")

# Playing the converted file
playsound.playsound('welcome.mp3')

# Saving the converted audio in a mp3 file named
# welcome
# myobj.save("welcome.mp3")

# Playing the converted file
# os.system("welcome.mp3")

r = RandomWords()

# Return a single random word
r.get_random_word()
