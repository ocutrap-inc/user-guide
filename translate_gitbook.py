import os
import requests

# DeepL API Configuration
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
DEEPL_URL = "https://api-free.deepl.com/v2/translate"  # Use "https://api.deepl.com/v2/translate" for PRO users

# Source & Destination Repositories
SOURCE_DIR = "."  # English repo root
DEST_DIR = "spanish-repo"  # Cloned Spanish repo directory

def translate_text(text, target_language="ES"):
    """Translates text using DeepL API"""
    response = requests.post(
        DEEPL_URL,
        data={
            "auth_key": DEEPL_API_KEY,
            "text": text,
            "source_lang": "EN",
            "target_lang": target_language,
            "preserve_formatting": 1,
            "split_sentences": 1
        },
    )

    try:
        result = response.json()
        return result["translations"][0]["text"]
    except requests.exceptions.JSONDecodeError:
        print("⚠️ Error: Failed to decode JSON response from DeepL. Check API key or rate limits.")
        print("Response content:", response.text)
        return text  # Return original text in case of failure

def translate_files():
    """Recursively finds and translates all Markdown (.md) files while maintaining folder structure"""
    for root, _, files in os.walk(SOURCE_DIR):
        if "spanish-repo" in root:  # Skip files already in the Spanish repo
            continue

        for filename in files:
            if filename.endswith(".md"):
                src_path = os.path.join(root, filename)

                # Preserve original folder structure
                rel_path = os.path.relpath(src_path, SOURCE_DIR)
                dest_path = os.path.join(DEST_DIR, rel_path)

                # Ensure destination folder exists
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                # Read and translate content
                with open(src_path, "r", encoding="utf-8") as f:
                    content = f.read()

                translated_content = translate_text(content)

                # Save translated content
                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write(translated_content)

                print(f"✅ Translated: {src_path} -> {dest_path}")

if __name__ == "__main__":
    translate_files()
