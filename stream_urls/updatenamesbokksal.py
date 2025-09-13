import json
import os

folder_path = r"C:\Users\VIJAY SNEHAL\Desktop\giturlmapping\bible_scripture\stream_urls"
index_file = os.path.join(folder_path, "index_mapping.json")

# Load index mapping
with open(index_file, 'r', encoding='utf-8') as f:
    index_mapping = json.load(f)

# Create reverse mapping: name -> index
name_to_index = {v: k for k, v in index_mapping.items()}

json_files = [
    "english_all_books_stream.json",
    "hindi_all_books_stream.json",
    "kannada_all_books_stream.json",
    "malayalam_all_books_stream.json",
    "tamil_all_books_stream.json",
    "telugu_all_books_stream.json"
]

for file_name in json_files:
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Replace book names with index
    new_data = {}
    for book_name, chapters in data.items():
        index = name_to_index.get(book_name)
        if index:
            new_data[index] = chapters
        else:
            print(f"Warning: {book_name} not found in index")

    # Save back to file or a new file
    with open(file_path, 'w', encoding='utf-8') as f_out:
        json.dump(new_data, f_out, ensure_ascii=False, indent=2)

    print(f"Updated {file_name}")
