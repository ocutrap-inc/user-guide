#!/usr/bin/env python
import os
import shutil
import openai
import time

def translate_text(text):
    """
    Uses the OpenAI Chat API to translate text to Spanish.
    Note: For large texts, consider breaking into smaller chunks due to token limits.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional translator. Translate the following text to Spanish, preserving any markdown formatting."},
                {"role": "user", "content": text},
            ],
            temperature=0.3,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"Error during translation: {e}")
        return text  # fallback: return the original text if an error occurs

def translate_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()
    translated_text = translate_text(text)
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
            if file.endswith(".md"):
                in_file = os.path.join(root, file)
                out_file = os.path.join(new_dir, file)
                print(f"Translating {in_file} to {out_file}")
                translate_file(in_file, out_file)
                # Pause briefly to avoid hitting API rate limits
                time.sleep(1)
            else:
                # Copy non-markdown files as is
                shutil.copy2(os.path.join(root, file), new_dir)

if __name__ == "__main__":
    # Set your OpenAI API key from the environment variable
    openai.api_key = os.getenv("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("Please set your OPENAI_API_KEY environment variable.")
    
    # Define directories. This example assumes the Spanish repo is a sibling directory.
    input_directory = "."
    output_directory = "../OcuTrap_Knowledge_Base_spanish"
    
    translate_directory(input_directory, output_directory)
