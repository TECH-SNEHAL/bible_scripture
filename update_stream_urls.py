import os
import sqlite3
import json
import random

# Folder paths
db_folder = "C:/Users/VIJAY SNEHAL/Desktop/giturlmapping/bible_scripture/db_files"
json_folder = "C:/Users/VIJAY SNEHAL/Desktop/giturlmapping/bible_scripture/stream_urls"

# Mapping of language to DB table
table_names = {
    "English": "bible_en",
    "Hindi": "bible_hi",
    "Kannada": "bible_kn",
    "Malayalam": "bible_ml",
    "Tamil": "bible_ta",
    "Telugu": "bible_te"
}

# Load all JSON audio files
audio_files = {}
languages = table_names.keys()
for lang in languages:
    json_file = os.path.join(json_folder, f"{lang.lower()}_all_books_stream.json")
    with open(json_file, "r", encoding="utf-8") as f:
        audio_files[lang] = json.load(f)

# Book indices range
book_indices = list(range(1, 67))  # 1 to 66

# Randomly select a book index and chapter (or specify manually)
book_index = random.choice(book_indices)
chapter_number = random.randint(1, 5)  # Example: choose chapter 1-5 randomly

print(f"Random Test -> Book index: {book_index}, Chapter: {chapter_number}\n")

# Fetch verses and audio for each language
for lang in languages:
    db_file = os.path.join(db_folder, table_names[lang] + ".db")
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Fetch verses
    cursor.execute(f"""
        SELECT verse, text FROM {table_names[lang]}
        WHERE book=? AND chapter=? ORDER BY verse
    """, (book_index, chapter_number))
    rows = cursor.fetchall()
    conn.close()

    print(f"--- {lang} Verses ---")
    if rows:
        for verse, text in rows:
            print(f"{verse}: {text}")
    else:
        print("No verses found for this chapter.")
    
    # Fetch audio URL
    audio_url = audio_files[lang].get(str(book_index), {}).get(str(chapter_number), "No audio URL")
    print(f"{lang} Audio URL: {audio_url}\n")
