import os
import subprocess
import openai
from openai import ChatCompletion

# Set the API key from the environment
openai.api_key = os.environ["OPENAI_API_KEY"]

def translate_markdown(content):
    """
    Translates Markdown content from English to Spanish.
    Uses the updated ChatCompletion interface from the OpenAI package.
    Preserves Markdown formatting.
    """
    messages = [
        {
            "role": "system",
            "content": (
                "You are a translation assistant that translates Markdown content from English to Spanish, "
                "preserving all formatting (headers, code blocks, links, etc.) exactly."
            )
        },
        {
            "role": "user",
            "content": (
                "Please translate the following Markdown text into Spanish, preserving its formatting exactly:\n\n"
                + content
            )
        }
    ]
    try:
        response = ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error translating text: {e}")
        return content  # fallback to original text if translation fails

def process_files(src_dir, dest_dir):
    """
    Recursively processes files in src_dir. For Markdown files (.md),
    it translates their content; other files are copied as is.
    The translated files are saved under dest_dir with the same structure.
    """
    for root, dirs, files in os.walk(src_dir):
        # Skip the destination folder to avoid reprocessing translated files
        if os.path.abspath(dest_dir) in os.path.abspath(root):
            continue

        relative_path = os.path.relpath(root, src_dir)
        dest_root = os.path.join(dest_dir, relative_path)
        os.makedirs(dest_root, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_root, file)
            if file.endswith('.md'):
                print(f"Translating {src_file} -> {dest_file}")
                with open(src_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                translated_content = translate_markdown(content)
                with open(dest_file, 'w', encoding='utf-8') as f_out:
                    f_out.write(translated_content)
            else:
                # Copy non-Markdown files directly
                with open(src_file, 'rb') as f_src, open(dest_file, 'wb') as f_dest:
                    f_dest.write(f_src.read())

if __name__ == '__main__':
    source_directory = '.'         # Root of your repo
    destination_directory = './translated'
    
    process_files(source_directory, destination_directory)

    # Change working directory to the translated folder and set up Git.
    os.chdir(destination_directory)
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "config", "user.email", "action@github.com"], check=True)
    subprocess.run(["git", "config", "user.name", "GitHub Action"], check=True)
    
    # Update remote URL if it exists; otherwise, add it.
    try:
        subprocess.run(["git", "remote", "set-url", "origin", os.environ["SPANISH_REPO_URL"]], check=True)
    except subprocess.CalledProcessError:
        subprocess.run(["git", "remote", "add", "origin", os.environ["SPANISH_REPO_URL"]], check=True)
    
    subprocess.run(["git", "add", "."], check=True)
    # Only attempt to commit if there are changes.
    commit_result = subprocess.run(
        ["git", "commit", "-m", "Automated Spanish translation update using updated ChatGPT API"],
        capture_output=True, text=True
    )
    if commit_result.returncode != 0:
        print("No changes to commit.")
    else:
        subprocess.run(["git", "push", "--force", "origin", "master"], check=True)
