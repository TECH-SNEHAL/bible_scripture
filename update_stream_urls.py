import os
import json
import requests
import subprocess

# -----------------------------
# JSON folder path
# -----------------------------
json_folder = r"C:\Users\VIJAY SNEHAL\Desktop\giturlmapping\bible_scripture\stream_urls"

# -----------------------------
# Language to GitHub repo/folder mapping
# -----------------------------
language_repo_mapping = {
    "english": {"repo": "audiofiles1", "folder": "english", "json_file": "english_all_books_stream.json"},
    "hindi": {"repo": "audiofiles2", "folder": "hindi", "json_file": "hindi_all_books_stream.json"},
    "malayalam": {"repo": "audiofiles2", "folder": "malayalam", "json_file": "malayalam_all_books_stream.json"},
    "kannada": {"repo": "audiofiles3", "folder": "kannada", "json_file": "kannada_all_books_stream.json"},
    "tamil": {"repo": "audiofiles3", "folder": "tamil", "json_file": "tamil_all_books_stream.json"},
    "telugu": {"repo": "audiofiles3", "folder": "telugu", "json_file": "telugu_all_books_stream.json"},
}

GITHUB_BASE_RAW = "https://raw.githubusercontent.com/TECH-SNEHAL"

# -----------------------------
# Function to list files from GitHub repo folder
# -----------------------------
def get_github_files(repo, folder):
    url = f"https://api.github.com/repos/TECH-SNEHAL/{repo}/contents/{folder}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"⚠️ Failed to fetch files for {repo}/{folder}: {response.status_code}")
        return []
    data = response.json()
    files = [item['name'] for item in data if item['type'] == 'file' and item['name'].endswith(".mp3")]
    return sorted(files)

# -----------------------------
# Update JSON URLs
# -----------------------------
for lang, info in language_repo_mapping.items():
    json_file_path = os.path.join(json_folder, info["json_file"])
    if not os.path.exists(json_file_path):
        print(f"JSON file {json_file_path} not found. Skipping {lang}.")
        continue

    # Get actual filenames from GitHub
    filenames = get_github_files(info["repo"], info["folder"])
    if not filenames:
        print(f"No files found for {lang}. Skipping.")
        continue

    # Load JSON
    with open(json_file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Replace URLs in order
    chapter_index = 0
    for book, chapters in data.items():
        for chapter in chapters:
            if chapter_index < len(filenames):
                file_name = filenames[chapter_index]
                new_url = f"{GITHUB_BASE_RAW}/{info['repo']}/main/{info['folder']}/{file_name}"
                data[book][chapter] = new_url
                chapter_index += 1
            else:
                print(f"⚠️ Not enough files in GitHub repo to match chapters for {lang}")
                break

    # Save updated JSON
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"✅ Updated URLs in {info['json_file']} for {lang}")

# -----------------------------
# Commit and push updated JSON
# -----------------------------
try:
    subprocess.run(['git', 'add', json_folder], check=True)
    subprocess.run(['git', 'commit', '-m', 'Update all_books_stream.json with exact GitHub URLs'], check=True)
    subprocess.run(['git', 'push'], check=True)
    print("\n✅ All JSON files committed and pushed successfully!")
except subprocess.CalledProcessError as e:
    print("\n⚠️ Git command failed:", e)
