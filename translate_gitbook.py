import os
import requests

# DeepL API Configuration
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
DEEPL_URL = "https://api-free.deepl.com/v2/translate"  # Use "https://api.deepl.com/v2/translate" for PRO users

# Define source and target language
SOURCE_LANG = "EN"
TARGET_LANG = "ES"

# Root directory where Markdown files are stored
ROOT_DIR = "."  # Start from the root directory

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
    """Recursively finds and translates all Markdown (.md) files"""
    for root, _, files in os.walk(ROOT_DIR):
        for filename in files:
            if filename.endswith(".md"):
                src_path = os.path.join(root, filename)
                translated_path = os.path.join(root.replace("OcuTrap_Knowledge_Base", "OcuTrap_Knowledge_Base_spanish"), filename)

                with open(src_path, "r", encoding="utf-8") as f:
                    content = f.read()

                translated_content = translate_text(content)

                os.makedirs(os.path.dirname(translated_path), exist_ok=True)
                with open(translated_path, "w", encoding="utf-8") as f:
                    f.write(translated_content)

                print(f"Translated: {src_path} -> {translated_path}")

if __name__ == "__main__":
    translate_files()
