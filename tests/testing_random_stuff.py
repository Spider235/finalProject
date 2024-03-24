from deep_translator import GoogleTranslator

translated = GoogleTranslator(source='english', target='german').translate("My brother is very tall")  # output -> Weiter so, du bist großartig
print(translated)
translatedd = GoogleTranslator(source='german', target='english').translate("Mein Bruder ist sehr groß")  # output -> Weiter so, du bist großartig
print(translatedd)