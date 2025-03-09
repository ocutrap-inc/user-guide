import os
import openai
import subprocess

# Set up the API key
openai.api_key = os.environ["OPENAI_API_KEY"]

def translate_markdown(content):
    """
    Translate Markdown content from English to Spanish while preserving Markdown formatting.
    Uses the new OpenAI Python API interface.
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
                f"{content}"
            )
        }
    ]
    
    try:
        # Using the new interface which supports dot-notation for response access.
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0
        )
        # Accessing the content via dot notation
        translated_text = response.choices[0].message.content.strip()
        return translated_text
    except Exception as e:
        print(f"Error translating text: {e}")
        return content  # fallback to the original content in case of error

def process_files(src_dir, dest_dir):
    """
    Recursively translate .md files in src_dir and copy them (preserving folder structure) to dest_dir.
    Non-Markdown files are copied directly.
    """
    for root, dirs, files in os.walk(src_dir):
        # Skip the destination folder to avoid reprocessing
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
                # Copy non-markdown files
                with open(src_file, 'rb') as f_src, open(dest_file, 'wb') as f_dest:
                    f_dest.write(f_src.read())

if __name__ == '__main__':
    source_directory = '.'  # your repo root
    destination_directory = './translated'
    
    process_files(source_directory, destination_directory)

    # Change to the translated directory and set up Git
    os.chdir(destination_directory)
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "config", "user.email", "action@github.com"], check=True)
    subprocess.run(["git", "config", "user.name", "GitHub Action"], check=True)
    
    # Instead of adding the remote blindly, update it if it already exists.
    try:
        subprocess.run(["git", "remote", "set-url", "origin", os.environ["SPANISH_REPO_URL"]], check=True)
    except subprocess.CalledProcessError:
        subprocess.run(["git", "remote", "add", "origin", os.environ["SPANISH_REPO_URL"]], check=True)
    
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Automated Spanish translation update using the updated ChatGPT API"], check=True)
    # Push to the target branch (adjust branch name if needed)
    subprocess.run(["git", "push", "--force", "origin", "master"], check=True)
