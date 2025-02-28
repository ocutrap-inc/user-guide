import os
import re
from google.cloud import translate_v2 as translate

# Initialize Google Translate Client
translate_client = translate.Client()

# Directories
SOURCE_DIR = "."  # English GitBook repo
DEST_DIR = "spanish-repo"  # Translated Spanish GitBook repo

# Files/Folders to Skip
SKIP_FILES = {"SUMMARY.md", "book.json"}  # GitBook-specific files
SKIP_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".mp4", ".pdf"}  # Do not translate assets


def translate_text(text, target_language="es"):
    """Translates text while preserving Markdown structure."""
    if not text.strip():
        return text  # Avoid translating empty strings
    result = translate_client.translate(text, target_language=target_language)
    return result["translatedText"]


def process_markdown(content):
    """Translates only visible text while preserving Markdown syntax."""
    
    # Define translation function
    def translate_match(match):
        return translate_text(match.group(1))

    # Patterns to translate (headers, list items, blockquotes, etc.)
    patterns = [
        (r"(^# .+)", translate_match),  # H1 Headers
        (r"(^## .+)", translate_match),  # H2 Headers
        (r"(^### .+)", translate_match),  # H3 Headers
        (r"(^#### .+)", translate_match),  # H4 Headers
        (r"(^##### .+)", translate_match),  # H5 Headers
        (r"(^###### .+)", translate_match),  # H6 Headers
        (r"(^> .+)", translate_match),  # Blockquotes
        (r"(^- .+)", translate_match),  # Bullet lists
        (r"(^\d+\..+)", translate_match),  # Numbered lists
        (r"(\*\*(.*?)\*\*)", translate_match),  # Bold text (**text**)
        (r"(\*(.*?)\*)", translate_match),  # Italics (*text*)
        (r"(`[^`]+`)", lambda m: m.group(0)),  # Skip inline code (`code`)
        (r"(```.*?```)", lambda m: m.group(0), re.DOTALL),  # Skip code blocks
        (r"(!\[.*\]\(.*\))", lambda m: m.group(0)),  # Skip images ![alt](img.png)
        (r"(\[.*\]\(.*\))", lambda m: m.group(0)),  # Skip links [text](url)
    ]

    # Apply patterns
    for pattern, replacer in patterns:
        content = re.sub(pattern, replacer, content, flags=re.MULTILINE)

    return content


def translate_files():
    """Recursively translates Markdown files while preserving structure."""
    for root, _, files in os.walk(SOURCE_DIR):
        if "spanish-repo" in root:  # Skip already translated repo
            continue

        for filename in files:
            src_path = os.path.join(root, filename)
            rel_path = os.path.relpath(src_path, SOURCE_DIR)
            dest_path = os.path.join(DEST_DIR, rel_path)

            # Skip assets & special files
            if filename in SKIP_FILES or os.path.splitext(filename)[1] in SKIP_EXTENSIONS:
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                os.system(f"cp '{src_path}' '{dest_path}'")  # Copy unmodified
                print(f"🔄 Copied: {src_path} -> {dest_path}")
                continue

            # Process Markdown files
            if filename.endswith(".md"):
                with open(src_path, "r", encoding="utf-8") as f:
                    content = f.read()

                translated_content = process_markdown(content)

                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                with open(dest_path, "w", encoding="utf-8") as f:
                    f.write(translated_content)

                print(f"✅ Translated: {src_path} -> {dest_path}")


if __name__ == "__main__":
    translate_files()
