import json
import os

# Folder containing the files
folder_path = r"C:\Users\VIJAY SNEHAL\Desktop\giturlmapping\bible_scripture\stream_urls"
json_file = "english_all_books_stream.json"

file_path = os.path.join(folder_path, json_file)

with open(file_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

books = list(data.keys())
index_mapping = {}
name_to_index = {}

for idx, book in enumerate(books, start=1):
    index = str(idx)
    index_mapping[index] = book
    name_to_index[book] = index

# Save index mapping to a file (optional)
with open(os.path.join(folder_path, "index_mapping.json"), "w", encoding='utf-8') as f_out:
    json.dump(index_mapping, f_out, ensure_ascii=False, indent=4)

print("Index mapping created.")
