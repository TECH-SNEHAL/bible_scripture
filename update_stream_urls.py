import os
import json
import subprocess

# -----------------------------
# Paths
# -----------------------------
base_folder = r"C:\Users\VIJAY SNEHAL\Desktop\giturlmapping\bible_scripture"
json_folder = os.path.join(base_folder, "stream_urls")

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
# Process each language
# -----------------------------
for lang, info in language_repo_mapping.items():
    json_path = os.path.join(json_folder, info["json_file"])
    if not os.path.exists(json_path):
        print(f"⚠️ {info['json_file']} not found for {lang}. Skipping.")
        continue

    print(f"Processing {lang}...")

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    updated = False

    # Go through each book and chapter
    for book, chapters in data.items():
        for chapter_num, filename in chapters.items():
            # Extract the file code (prefix before '-')
            file_code = filename.split("-", 1)[0]
            # Build the new URL
            new_url = f"{GITHUB_BASE_RAW}/{info['repo']}/main/{info['folder']}/{filename}"
            if data[book][chapter_num] != new_url:
                data[book][chapter_num] = new_url
                updated = True

    # Save only if updated
    if updated:
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        print(f"✅ Updated URLs in {info['json_file']} for {lang}")
    else:
        print(f"ℹ️ No changes needed for {info['json_file']}")

# -----------------------------
# Commit changes if any
# -----------------------------
try:
    subprocess.run(['git', '-C', base_folder, 'add', 'stream_urls'], check=True)
    subprocess.run(['git', '-C', base_folder, 'commit', '-m', 'Update all_books_stream.json files with correct GitHub URLs'], check=True)
    subprocess.run(['git', '-C', base_folder, 'push'], check=True)
    print("\n✅ All updates committed and pushed!")
except subprocess.CalledProcessError as e:
    print("\n⚠️ Git operation failed:", e)
