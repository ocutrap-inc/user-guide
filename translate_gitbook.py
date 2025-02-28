import os
import requests

# DeepL API Configuration
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
DEEPL_URL = "https://api-free.deepl.com/v2/translate"  # Use "https://api.deepl.com/v2/translate" for PRO users

# Language Configuration
SOURCE_LANG = "EN"
TARGET_LANG = "ES"

# Define directories
ROOT_DIR = "."  # English repo root
SPANISH_REPO = "spanish-repo"  # Spanish repo name inside GitHub Actions workspace

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
    """Recursively finds and translates all Markdown (.md) files while maintaining the directory structure"""
    for root, _, files in os.walk(ROOT_DIR):
        for filename in files:
            if filename.endswith(".md"):
                src_path = os.path.join(root, filename)

                # Determine the destination path inside the Spanish repository
                rel_path = os.path.relpath(src_path, ROOT_DIR)  # Keep relative folder structure
                dest_path = os.path.join(SPANISH_REPO, rel_path)

                # Ensure the destination folder exists
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                # Read and translate content
                with open(src_path, "r", encoding="utf-8") as f:
                    content = f.read()

                translated_content = translate_text(content)

                # Save translated content in the same folder structure
                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write(translated_content)

                print(f"Translated: {src_path} -> {dest_path}")

if __name__ == "__main__":
    translate_files()
