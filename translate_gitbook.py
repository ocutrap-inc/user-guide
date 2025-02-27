import os
import requests

# DeepL API Configuration
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
DEEPL_URL = "https://api-free.deepl.com/v2/translate"  # Use "https://api.deepl.com/v2/translate" for PRO users

# Language Configuration
SOURCE_LANG = "EN"
TARGET_LANG = "ES"

# Directories
GITBOOK_SRC = "docs/"
GITBOOK_TRANSLATED = "translated/"

def translate_text(text, target_language=TARGET_LANG):
    """Translates text using DeepL API"""
    response = requests.post(
        DEEPL_URL,
        data={
            "auth_key": DEEPL_API_KEY,
            "text": text,
            "source_lang": SOURCE_LANG,
            "target_lang": target_language,
            "preserve_formatting": 1,
            "split_sentences": 1
        },
    )
    result = response.json()
    return result["translations"][0]["text"] if "translations" in result else text

def translate_files():
    """Translates all markdown files in GitBook repo"""
    if not os.path.exists(GITBOOK_TRANSLATED):
        os.makedirs(GITBOOK_TRANSLATED)

    for filename in os.listdir(GITBOOK_SRC):
        if filename.endswith(".md"):
            src_path = os.path.join(GITBOOK_SRC, filename)
            dest_path = os.path.join(GITBOOK_TRANSLATED, filename)

            with open(src_path, "r", encoding="utf-8") as f:
                content = f.read()

            translated_content = translate_text(content)

            with open(dest_path, "w", encoding="utf-8") as f:
                f.write(translated_content)

            print(f"Translated: {filename}")

if __name__ == "__main__":
    translate_files()
