from deep_translator import GoogleTranslator

translated = GoogleTranslator(source='german', target='english').translate("Kaninch")  # output -> Weiter so, du bist großartig
print(translated)