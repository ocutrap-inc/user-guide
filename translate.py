import os
import re
import subprocess
import openai

# Set up your OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

def translate_text(text):
    """
    Translates the given text from English to Spanish using the new ChatCompletion API.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are a translation assistant. Translate the provided text from English to Spanish. "
                "Preserve any formatting like Markdown syntax."
            )
        },
        {"role": "user", "content": text}
    ]
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error translating text: {e}")
        return text  # fallback: return original text

def translate_summary(content):
    """
    Special handling for SUMMARY.md: only the link text is translated, while the URL is preserved.
    """
    def replace_link(match):
        link_text = match.group(1)
        url = match.group(2)
        return f"[{translate_text(link_text)}]({url})"

    # Process each line: if it contains a markdown link, translate only the link text.
    lines = content.splitlines()
    translated_lines = []
    for line in lines:
        if re.search(r'\[.*?\]\(.*?\)', line):
            translated_line = re.sub(r'\[(.*?)\]\((.*?)\)', replace_link, line)
        else:
            translated_line = translate_text(line)
        translated_lines.append(translated_line)
    return "\n".join(translated_lines)

def process_files(src_dir, dest_dir):
    """
    Recursively translates all Markdown files from src_dir into dest_dir.
    For SUMMARY.md, use custom handling.
    Non-Markdown files are copied as is.
    """
    for root, dirs, files in os.walk(src_dir):
        # Skip the destination directory if inside the source
        if os.path.abspath(dest_dir) in os.path.abspath(root):
            continue

        relative_path = os.path.relpath(root, src_dir)
        dest_root = os.path.join(dest_dir, relative_path)
        os.makedirs(dest_root, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_root, file)
            if file.lower() == "summary.md":
                print(f"Translating SUMMARY file: {src_file} -> {dest_file}")
                with open(src_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                translated_content = translate_summary(content)
                with open(dest_file, 'w', encoding='utf-8') as f_out:
                    f_out.write(translated_content)
            elif file.endswith('.md'):
                print(f"Translating {src_file} -> {dest_file}")
                with open(src_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                translated_content = translate_text(content)
                with open(dest_file, 'w', encoding='utf-8') as f_out:
                    f_out.write(translated_content)
            else:
                # Copy non-Markdown files unchanged
                with open(src_file, 'rb') as f_src, open(dest_file, 'wb') as f_dest:
                    f_dest.write(f_src.read())

if __name__ == '__main__':
    source_directory = '.'         # Root of your repository
    destination_directory = './translated'
    
    process_files(source_directory, destination_directory)

    # Change directory to the translated folder
    os.chdir(destination_directory)
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "config", "user.email", "action@github.com"], check=True)
    subprocess.run(["git", "config", "user.name", "GitHub Action"], check=True)
    
    # Set remote URL; ensure SPANISH_REPO_URL is correct and repo exists
    spanish_repo_url = os.environ.get("SPANISH_REPO_URL")
    try:
        subprocess.run(["git", "remote", "set-url", "origin", spanish_repo_url], check=True)
    except subprocess.CalledProcessError:
        subprocess.run(["git", "remote", "add", "origin", spanish_repo_url], check=True)
    
    subprocess.run(["git", "add", "."], check=True)
    commit_result = subprocess.run(
        ["git", "commit", "-m", "Automated Spanish translation update using ChatGPT API"],
        capture_output=True, text=True
    )
    if commit_result.returncode != 0:
        print("No changes to commit.")
    else:
        # Push changes to the 'main' branch (adjust branch name if necessary)
        subprocess.run(["git", "push", "--force", "origin", "main"], check=True)
