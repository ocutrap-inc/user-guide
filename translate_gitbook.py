import os
import shutil
import html
from google.cloud import translate_v2 as translate

# Initialize the Google Translate client.
translate_client = translate.Client()

# Define directories:
SOURCE_DIR = "."  # English GitBook repo root.
DEST_DIR = "spanish-repo"  # Local folder for the Spanish version.

# File extensions that should be copied without translation (binary assets).
SKIP_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".mp4", ".pdf"}

def translate_text(text, target_language="es"):
    """Translate the given text using Google Translate and unescape HTML entities."""
    if not text.strip():
        return text
    result = translate_client.translate(text, target_language=target_language)
    return html.unescape(result["translatedText"])

def translate_markdown(content):
    """
    Translate markdown content while preserving code blocks.
    Splits content by triple backticks and translates only the text outside the code blocks.
    """
    parts = content.split("```")
    # Even-indexed parts are outside code blocks.
    for i in range(0, len(parts), 2):
        parts[i] = translate_text(parts[i])
    return "```".join(parts)

def process_file(src_path, dest_path):
    """Process a single file: translate markdown or copy other files."""
    ext = os.path.splitext(src_path)[1].lower()
    # Copy binary files directly.
    if ext in SKIP_EXTENSIONS:
        shutil.copy2(src_path, dest_path)
        print(f"Copied (binary): {src_path} -> {dest_path}")
    elif src_path.endswith(".md"):
        # Open and read the markdown file.
        with open(src_path, "r", encoding="utf-8") as f:
            content = f.read()
        # Translate the markdown content.
        translated_content = translate_markdown(content)
        # Write the translated content to the destination.
        with open(dest_path, "w", encoding="utf-8") as f:
            f.write(translated_content)
        print(f"Translated: {src_path} -> {dest_path}")
    else:
        # For any other files, simply copy them.
        shutil.copy2(src_path, dest_path)
        print(f"Copied: {src_path} -> {dest_path}")

def translate_files():
    """Walk the source directory and process each file."""
    for root, dirs, files in os.walk(SOURCE_DIR):
        # Skip the destination folder to avoid processing already translated files.
        if os.path.abspath(DEST_DIR) in os.path.abspath(root):
            continue

        for filename in files:
            src_path = os.path.join(root, filename)
            # Calculate the relative path from SOURCE_DIR.
            rel_path = os.path.relpath(src_path, SOURCE_DIR)
            dest_path = os.path.join(DEST_DIR, rel_path)
            # Ensure the destination directory exists.
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            process_file(src_path, dest_path)

if __name__ == "__main__":
    translate_files()
