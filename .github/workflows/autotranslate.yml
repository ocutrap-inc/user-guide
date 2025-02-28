import os
from google.cloud import translate_v2 as translate

# Initialize the Google Translate client.
translate_client = translate.Client()

# Define directories:
SOURCE_DIR = "."  # Your English GitBook repo (the root)
DEST_DIR = "spanish-repo"  # Local folder where the Spanish version will be built

# Files and file extensions to copy without translation:
SKIP_FILES = {"SUMMARY.md", "book.json"}  # GitBook-specific files you want to keep unchanged
SKIP_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".mp4", ".pdf"}

def translate_text(text, target_language="es"):
    """Translate the given text using Google Translate."""
    if not text.strip():
        return text  # Return empty or whitespace-only strings unchanged.
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]

def translate_markdown(content):
    """
    Split content by triple backticks (which denote code blocks).
    Only translate the parts outside code blocks.
    Reassemble the file with code blocks left intact.
    """
    parts = content.split("```")
    # parts with even indices are outside code blocks.
    for i in range(0, len(parts), 2):
        parts[i] = translate_text(parts[i])
    return "```".join(parts)

def translate_files():
    """Walk through the source directory, and process each file."""
    for root, _, files in os.walk(SOURCE_DIR):
        # Skip our destination folder if it already exists.
        if DEST_DIR in os.path.abspath(root):
            continue

        for filename in files:
            src_path = os.path.join(root, filename)
            rel_path = os.path.relpath(src_path, SOURCE_DIR)
            dest_path = os.path.join(DEST_DIR, rel_path)

            # If the file is one we want to skip (like assets or specific GitBook files), just copy it.
            if filename in SKIP_FILES or os.path.splitext(filename)[1] in SKIP_EXTENSIONS:
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                os.system(f"cp '{src_path}' '{dest_path}'")
                print(f"Copied: {src_path} -> {dest_path}")
                continue

            # If it's a Markdown file, process it:
            if filename.endswith(".md"):
                with open(src_path, "r", encoding="utf-8") as f:
                    content = f.read()
                translated_content = translate_markdown(content)
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write(translated_content)
                print(f"Translated: {src_path} -> {dest_path}")
            else:
                # For any other file types, simply copy them.
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                os.system(f"cp '{src_path}' '{dest_path}'")
                print(f"Copied: {src_path} -> {dest_path}")

if __name__ == "__main__":
    translate_files()
