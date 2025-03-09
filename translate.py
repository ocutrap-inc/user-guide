import os
import re
import subprocess
import openai

# Set up the API key from the environment variable
openai.api_key = os.environ["OPENAI_API_KEY"]

def translate_markdown(content):
    """
    Translates given Markdown content from English to Spanish using the updated ChatCompletion API.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are a translation assistant that translates Markdown content from English to Spanish. "
                "Preserve all formatting exactly (including Markdown syntax such as headers, lists, code blocks, etc.)."
            )
        },
        {
            "role": "user",
            "content": (
                "Please translate the following Markdown text into Spanish while preserving the formatting:\n\n"
                + content
            )
        }
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
        return content  # Fallback to original content if an error occurs

def translate_summary(summary_text):
    """
    Processes the SUMMARY.md file line-by-line.
    For lines containing markdown links, only the link text is translated
    (the URL remains unchanged). Other lines are translated as a whole.
    """
    lines = summary_text.splitlines()
    translated_lines = []
    for line in lines:
        # Look for markdown links: [link text](URL)
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
    Recursively processes files in src_dir:
      - For SUMMARY.md, uses translate_summary.
      - For other Markdown files, translates the entire content.
      - Copies non-Markdown files as-is.
    The output is written to dest_dir preserving the directory structure.
    """
    for root, dirs, files in os.walk(src_dir):
        # Skip the destination folder to avoid processing output files
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
                # Copy non-Markdown files
                with open(src_file, 'rb') as f_src, open(dest_file, 'wb') as f_dest:
                    f_dest.write(f_src.read())

if __name__ == '__main__':
    source_directory = '.'         # Root of your repository
    destination_directory = './translated'
    
    process_files(source_directory, destination_directory)

    # Initialize Git in the translated folder and set remote
    os.chdir(destination_directory)
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "config", "user.email", "action@github.com"], check=True)
    subprocess.run(["git", "config", "user.name", "GitHub Action"], check=True)
    
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
        # Note: Push to the 'main' branch (not 'master')
        subprocess.run(["git", "push", "--force", "origin", "main"], check=True)
