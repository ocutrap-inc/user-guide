#!/usr/bin/env python
import os
import shutil
from google.cloud import translate_v2 as translate

def translate_text(text, target='es'):
    result = translate_client.translate(text, target_language=target)
    return result["translatedText"]

def translate_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()
    translated_text = translate_text(text, target='es')
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(translated_text)

def translate_directory(input_dir, output_dir):
    # Remove output_dir if it exists to avoid stale files
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)
    
    for root, dirs, files in os.walk(input_dir):
        # Skip the Spanish repo directory if it exists inside the repo
        if os.path.abspath(output_dir) in [os.path.abspath(os.path.join(root, d)) for d in dirs]:
            continue
        # Create a corresponding directory in output_dir
        relative_path = os.path.relpath(root, input_dir)
        new_dir = os.path.join(output_dir, relative_path)
        os.makedirs(new_dir, exist_ok=True)
        
        for file in files:
            # For example, translate markdown files
            if file.endswith(".md"):
                in_file = os.path.join(root, file)
                out_file = os.path.join(new_dir, file)
                translate_file(in_file, out_file)
            else:
                # Copy non-markdown files as is
                shutil.copy2(os.path.join(root, file), new_dir)

if __name__ == "__main__":
    # Initialize the Google Translate client.
    # This uses the GOOGLE_APPLICATION_CREDENTIALS env variable.
    translate_client = translate.Client()
    
    # Assuming your Gitbook repo is the current directory.
    # Define the output directory as a sibling (or adjust as needed).
    input_directory = "."
    output_directory = "../OcuTrap_Knowledge_Base_spanish"
    
    translate_directory(input_directory, output_directory)
