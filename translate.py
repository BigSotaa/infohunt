from googletrans import Translator

def translate_to_english(text):
    translator = Translator()
    translation = translator.translate(text, dest='en')
    return translation.text

# Read the content of the README file
with open('README.md', 'r', encoding='utf-8') as file:
    content = file.read()

# Translate the content
translated_content = translate_to_english(content)

# Write the translated content to a new file
with open('README_translated.md', 'w', encoding='utf-8') as file:
    file.write(translated_content)

print("Translation complete. Check README_translated.md for the translated content.")