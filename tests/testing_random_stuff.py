from deep_translator import GoogleTranslator

translated = GoogleTranslator(source='english', target='german').translate("klein")  # output -> Weiter so, du bist großartig
print(translated)
translatedd = GoogleTranslator(source='german', target='english').translate("stark")  # output -> Weiter so, du bist großartig
print(translatedd)