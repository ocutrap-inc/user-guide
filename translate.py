import os
import re
import subprocess
import openai

# Set up your OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

def translate_markdown(content):
    """
    Translates Markdown content from English to Spanish.
    Uses the new ChatCompletion.create() method.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are a translation assistant that translates Markdown content from English to Spanish. "
                "Preserve all Markdown formatting (headers, lists, code blocks, etc.)."
            )
        },
        {
            "role": "user",
            "content": "Please translate the following text to Spanish:\n\n" + content
        }
    ]
    try:
        # Ensure we call the create() method explicitly.
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error translating text: {e}")
        return content

def translate_summary(summary_text):
    """
    Processes a SUMMARY.md file line by line.
    For markdown links, only the link text is translated.
    """
    lines = summary_text.splitlines()
    translated_lines = []
    for line in lines:
        if re.search(r'\[.*?\]\(.*?\)', line):
            translated_line = re.sub(
                r'\[(.*?)\]\((.*?)\)',
                lambda m: f"[{translate_markdown(m.group(1))}]({m.group(2)})",
                line
            )
        else:
            translated_line = translate_markdown(line)
        translated_lines.append(translated_line)
    return "\n".join(translated_lines)

def process_files(src_dir, dest_dir):
    """
    Recursively translates all Markdown files from src_dir into dest_dir.
    For SUMMARY.md, uses a custom translation that preserves URLs.
    Non-Markdown files are copied as is.
    """
    for root, dirs, files in os.walk(src_dir):
        # Skip the destination directory itself
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
                translated_content = translate_markdown(content)
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

    # Initialize Git in the translated folder and commit changes
    os.chdir(destination_directory)
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "config", "user.email", "action@github.com"], check=True)
    subprocess.run(["git", "config", "user.name", "GitHub Action"], check=True)
    
    # Set or add remote (ensure that SPANISH_REPO_URL is correct and the repo exists)
    try:
        subprocess.run(["git", "remote", "set-url", "origin", os.environ["SPANISH_REPO_URL"]], check=True)
    except subprocess.CalledProcessError:
        subprocess.run(["git", "remote", "add", "origin", os.environ["SPANISH_REPO_URL"]], check=True)
    
    subprocess.run(["git", "add", "."], check=True)
    commit_result = subprocess.run(
        ["git", "commit", "-m", "Automated Spanish translation update using updated ChatGPT API"],
        capture_output=True, text=True
    )
    if commit_result.returncode != 0:
        print("No changes to commit.")
    else:
        # Push changes to the 'main' branch (make sure the repo exists and the branch name is correct)
        subprocess.run(["git", "push", "--force", "origin", "main"], check=True)
