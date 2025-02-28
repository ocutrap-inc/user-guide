import os
import json
from google.cloud import translate_v2 as translate

# Google Cloud authentication setup
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if GOOGLE_CREDENTIALS:
    with open("gcp_credentials.json", "w") as f:
        f.write(GOOGLE_CREDENTIALS)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gcp_credentials.json"

# Initialize Google Translate client
translate_client = translate.Client()

# Source & Destination Repositories
SOURCE_DIR = "."  # English repo root
DEST_DIR = "spanish-repo"  # Cloned Spanish repo directory

def translate_text(text, target_language="es"):
    """Translates text using Google Translate API"""
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]

def translate_files():
    """Recursively translates all Markdown (.md) files while preserving folder structure"""
    for root, _, files in os.walk(SOURCE_DIR):
        if "spanish-repo" in root:  # Avoid overwriting Spanish repo files
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
