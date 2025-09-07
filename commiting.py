import os
import zipfile
import sqlite3
import shutil

# Directory containing the zip files
zip_dir = r"C:\Users\VIJAY SNEHAL\Desktop\bible sqlite\bible_languages_files"

# The standardized book names (with underscores for multi-word books)
book_names = [
    "Genesis","Exodus","Leviticus","Numbers","Deuteronomy","Joshua","Judges",
    "Ruth","1_Samuel","2_Samuel","1_Kings","2_Kings","1_Chronicles","2_Chronicles",
    "Ezra","Nehemiah","Esther","Job","Psalms","Proverbs","Ecclesiastes",
    "Song_of_Solomon","Isaiah","Jeremiah","Lamentations","Ezekiel","Daniel",
    "Hosea","Joel","Amos","Obadiah","Jonah","Micah","Nahum","Habakkuk","Zephaniah",
    "Haggai","Zechariah","Malachi","Matthew","Mark","Luke","John","Acts","Romans",
    "1_Corinthians","2_Corinthians","Galatians","Ephesians","Philippians","Colossians",
    "1_Thessalonians","2_Thessalonians","1_Timothy","2_Timothy","Titus","Philemon",
    "Hebrews","James","1_Peter","2_Peter","1_John","2_John","3_John","Jude","Revelation"
]

# Process each zip file
for zip_file in os.listdir(zip_dir):
    if zip_file.endswith(".zip"):
        zip_path = os.path.join(zip_dir, zip_file)
        print(f"\nProcessing {zip_file}...")

        # Get size before
        size_before = os.path.getsize(zip_path) / 1024
        print(f"Size before: {size_before:.2f} KB")

        # Extract zip to temp folder
        temp_dir = os.path.join(zip_dir, "temp_db")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.makedirs(temp_dir)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Find the .db file inside
        db_files = [f for f in os.listdir(temp_dir) if f.endswith(".db")]
        if not db_files:
            print("No DB file found in the zip!")
            continue
        db_path = os.path.join(temp_dir, db_files[0])

        # Connect to DB and update book names
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check table and columns
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cursor.fetchall()]
        table_name = tables[0]  # Assume first table is the main table

        # Get distinct book names from DB
        cursor.execute(f"SELECT DISTINCT book FROM {table_name}")
        db_books = [b[0] for b in cursor.fetchall()]

        # Map current DB names to standardized names
        for idx, name in enumerate(book_names):
            if idx < len(db_books):
                old_name = db_books[idx]
                cursor.execute(f"UPDATE {table_name} SET book = ? WHERE book = ?", (name, old_name))

        # Commit and close
        conn.commit()
        conn.close()

        # Reopen DB to vacuum
        conn = sqlite3.connect(db_path)
        conn.execute("VACUUM")
        conn.close()

        # Re-zip the database
        new_zip_path = zip_path  # overwrite original
        with zipfile.ZipFile(new_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(db_path, arcname=db_files[0])

        # Remove temp folder
        shutil.rmtree(temp_dir)

        # Print size after
        size_after = os.path.getsize(new_zip_path) / 1024
        print(f"Size after: {size_after:.2f} KB")
        print(f"{zip_file} processed successfully.")

print("\nAll zip files updated, vacuumed, and re-zipped!")
