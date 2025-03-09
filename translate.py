import os
import openai
import subprocess

# Set your OpenAI API key from the environment variable
openai.api_key = os.environ["OPENAI_API_KEY"]

def translate_markdown(content):
    """
    Uses OpenAI's ChatCompletion endpoint to translate Markdown content from English to Spanish.
    The prompt instructs the model to preserve Markdown formatting.
    """
    messages = [
        {
            "role": "system", 
            "content": (
                "You are a translation assistant that translates Markdown content from English to Spanish, "
                "preserving all formatting exactly (headers, code blocks, links, etc.) and without any commentary."
            )
        },
        {
            "role": "user", 
            "content": (
                "Please translate the following Markdown text into Spanish, preserving the formatting exactly:\n\n"
                f"{content}"
            )
        }
    ]
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0
        )
        translated_text = response['choices'][0]['message']['content'].strip()
        return translated_text
    except Exception as e:
        print(f"Error translating text: {e}")
        return content  # In case of error, fallback to original text

def process_files(src_dir, dest_dir):
    """
    Recursively processes files in src_dir. Translates .md files and copies other files.
    The translated files are saved in a parallel structure under dest_dir.
    """
    for root, dirs, files in os.walk(src_dir):
        # Avoid processing the destination folder itself
        if os.path.abspath(dest_dir) in os.path.abspath(root):
            continue

        relative_path = os.path.relpath(root, src_dir)
        dest_root = os.path.join(dest_dir, relative_path)
        os.makedirs(dest_root, exist_ok=True)
        
        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_root, file)
            if file.endswith('.md'):
                print(f"Translating {src_file} to {dest_file}")
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
    # Define the source directory (your current repo) and destination for translated files.
    source_directory = '.'  # Assuming your repo root
    destination_directory = './translated'
    
    process_files(source_directory, destination_directory)

    # Prepare to push the translated files to the Spanish repository
    os.chdir(destination_directory)
    subprocess.run(["git", "init"], check=True)
    subprocess.run(["git", "config", "user.email", "action@github.com"], check=True)
    subprocess.run(["git", "config", "user.name", "GitHub Action"], check=True)
    subprocess.run(["git", "remote", "add", "origin", os.environ["SPANISH_REPO_URL"]], check=True)
    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "commit", "-m", "Automated Spanish translation update using GPT"], check=True)
    
    # Adjust branch name as necessary (e.g., master or main)
    subprocess.run(["git", "push", "--force", "origin", "master"], check=True)
