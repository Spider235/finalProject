from deep_translator import GoogleTranslator

translated = GoogleTranslator(source='german', target='english').translate("Fisch")  # output -> Weiter so, du bist großartig
print(translated)