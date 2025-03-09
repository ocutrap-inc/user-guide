#!/usr/bin/env python3
"""
translate_repo.py

This script recursively copies all Markdown files (and other assets) from a source GitBook repo,
translates the titles and content into Spanish, and writes them to a destination folder.
It handles SUMMARY.md separately so that Markdown link texts are translated while keeping the file URLs intact.

Requirements:
  pip install googletrans==4.0.0-rc1

Usage:
  python translate_repo.py --src path/to/OcuTrap_Knowledge_Base --dest path/to/OcuTrap_Knowledge_Base_spanish
"""

import os
import re
import argparse
from googletrans import Translator

def translate_text(text, translator):
    """
    Translate the entire text to Spanish.
    """
    # You can split text if needed if it's very long (here we assume the texts are moderate in size)
    translation = translator.translate(text, dest='es')
    return translation.text

def translate_markdown_links(content, translator):
    """
    Find all markdown links and translate the link text (i.e. the part inside the square brackets)
    while preserving the link URL.
    
    Example:
      [Introduction](getting-started/introduction.md)
    becomes:
      [Introducción](getting-started/introduction.md)
    """
    # Define a callback function for regex substitution.
    def repl(match):
        link_text = match.group(1)
        url = match.group(2)
        # Translate only the link text
        translated_link_text = translator.translate(link_text, dest='es').text
        return f'[{translated_link_text}]({url})'
    
    # Replace all markdown link texts.
    new_content = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', repl, content)
    return new_content

def process_file(src_path, dest_path, translator):
    """
    Read a file, translate its content and (if SUMMARY.md) process the markdown links,
    then write the translated content to the destination file.
    """
    with open(src_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # If this is SUMMARY.md, do special link processing.
    if os.path.basename(src_path).lower() == 'summary.md':
        translated_content = translate_markdown_links(content, translator)
    else:
        translated_content = translate_text(content, translator)

    # Write the translated content to the destination file.
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(translated_content)
    print(f"Translated: {src_path} -> {dest_path}")

def process_directory(src_dir, dest_dir, translator):
    """
    Recursively process all files in the source directory.
    Markdown files are translated while other files (images, etc.) are copied as-is.
    """
    for root, dirs, files in os.walk(src_dir):
        rel_path = os.path.relpath(root, src_dir)
        dest_root = os.path.join(dest_dir, rel_path)
        os.makedirs(dest_root, exist_ok=True)
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_root, file)
            if file.endswith('.md'):
                process_file(src_file, dest_file, translator)
            else:
                # Simply copy non-markdown files (like images) without changes.
                with open(src_file, 'rb') as f:
                    data = f.read()
                with open(dest_file, 'wb') as f:
                    f.write(data)
                print(f"Copied asset: {src_file} -> {dest_file}")

def main():
    parser = argparse.ArgumentParser(description="Translate GitBook repo from English to Spanish.")
    parser.add_argument('--src', required=True, help='Path to the source repository directory (English version)')
    parser.add_argument('--dest', required=True, help='Path to the destination repository directory (Spanish version)')
    args = parser.parse_args()

    translator = Translator()
    process_directory(args.src, args.dest, translator)
    print("Translation complete.")

if __name__ == '__main__':
    main()
