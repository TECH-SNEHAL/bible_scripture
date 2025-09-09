import json
from collections import OrderedDict
import os

# Folder path where the JSON files are located
INPUT_FOLDER = "./stream_urls/"
OUTPUT_FOLDER = "./stream_urls/"

# Base URLs for each language
BASE_URLS = {
    'english': "https://www.wordpocket.org/bibles/app/audio/1",
    'hindi': "https://www.wordproaudio.net/bibles/app/audio/3",
    'kannada': "https://www.wordproaudio.net/bibles/app/audio/24",
    'malayalam': "https://www.wordproaudio.net/bibles/app/audio/25",
    'tamil': "https://www.wordproaudio.net/bibles/app/audio/30",
    'telugu': "https://www.wordproaudio.org/bibles/app/audio/29"
}

# Bible books in order and their number of chapters
books = [
    ("Genesis", 50),
    ("Exodus", 40),
    ("Leviticus", 27),
    ("Numbers", 36),
    ("Deuteronomy", 34),
    ("Joshua", 24),
    ("Judges", 21),
    ("Ruth", 4),
    ("1_Samuel", 31),
    ("2_Samuel", 24),
    ("1_Kings", 22),
    ("2_Kings", 25),
    ("1_Chronicles", 29),
    ("2_Chronicles", 36),
    ("Ezra", 10),
    ("Nehemiah", 13),
    ("Esther", 10),
    ("Job", 42),
    ("Psalms", 150),
    ("Proverbs", 31),
    ("Ecclesiastes", 12),
    ("Song_of_Solomon", 8),
    ("Isaiah", 66),
    ("Jeremiah", 52),
    ("Lamentations", 5),
    ("Ezekiel", 48),
    ("Daniel", 12),
    ("Hosea", 14),
    ("Joel", 3),
    ("Amos", 9),
    ("Obadiah", 1),
    ("Jonah", 4),
    ("Micah", 7),
    ("Nahum", 3),
    ("Habakkuk", 3),
    ("Zephaniah", 3),
    ("Haggai", 2),
    ("Zechariah", 14),
    ("Malachi", 4),
    ("Matthew", 28),
    ("Mark", 16),
    ("Luke", 24),
    ("John", 21),
    ("Acts", 28),
    ("Romans", 16),
    ("1_Corinthians", 16),
    ("2_Corinthians", 13),
    ("Galatians", 6),
    ("Ephesians", 6),
    ("Philippians", 4),
    ("Colossians", 4),
    ("1_Thessalonians", 5),
    ("2_Thessalonians", 3),
    ("1_Timothy", 6),
    ("2_Timothy", 4),
    ("Titus", 3),
    ("Philemon", 1),
    ("Hebrews", 13),
    ("James", 5),
    ("1_Peter", 5),
    ("2_Peter", 3),
    ("1_John", 5),
    ("2_John", 1),
    ("3_John", 1),
    ("Jude", 1),
    ("Revelation", 22)
]

# Mapping file names to language keys
FILES = {
    'english_all_books_stream.json': 'english',
    'hindi_all_books_stream.json': 'hindi',
    'kannada_all_books_stream.json': 'kannada',
    'malayalam_all_books_stream.json': 'malayalam',
    'tamil_all_books_stream.json': 'tamil',
    'telugu_all_books_stream.json': 'telugu'
}

def update_json(file_name, language):
    input_path = INPUT_FOLDER + file_name
    output_path = OUTPUT_FOLDER + "updated_" + file_name
    base_url = BASE_URLS[language]

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f, object_pairs_hook=OrderedDict)

    updated_data = OrderedDict()

    for book_index, (book_name, total_chapters) in enumerate(books, start=1):
        if book_name not in data:
            print(f"⚠ {book_name} not found in {file_name}")
            continue

        updated_data[book_name] = OrderedDict()
        for chapter in range(1, total_chapters + 1):
            chapter_str = str(chapter)
            # Correct URL format: language folder / book_index / chapter.mp3
            url = f"{base_url}/{book_index}/{chapter}.mp3"
            updated_data[book_name][chapter_str] = url

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(updated_data, f, ensure_ascii=False, indent=4)

    print(f"✅ Updated {file_name} -> {output_path}")

def main():
    for file_name, language in FILES.items():
        update_json(file_name, language)

if __name__ == "__main__":
    main()
