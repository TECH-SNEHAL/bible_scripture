import zipfile
import os
import sqlite3

# paths
repo_dir = r"C:\Users\VIJAY SNEHAL\Desktop\giturlmapping\bible_scripture"
db_dir = os.path.join(repo_dir, "db_files")

# all language codes
languages = ["en", "hi", "kn", "ml", "ta", "te"]

def format_size(bytes_size):
    """Helper to format size in KB/MB"""
    for unit in ['B', 'KB', 'MB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} GB"

for lang in languages:
    zip_path = os.path.join(repo_dir, f"bible_{lang}.zip")
    db_path = os.path.join(db_dir, f"bible_{lang}.db")

    if os.path.exists(zip_path) and os.path.exists(db_path):
        # overwrite zip with new db
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(db_path, os.path.basename(db_path))
        print(f"\n✅ Updated {lang} zip file")

        # sizes
        zip_size = os.path.getsize(zip_path)
        db_size = os.path.getsize(db_path)
        print(f"📦 Zip: {zip_path} ({format_size(zip_size)})")
        print(f"🗄️  DB: {db_path} ({format_size(db_size)})")

        # --- Verification ---
        extract_path = os.path.join(repo_dir, f"temp_{lang}.db")
        with zipfile.ZipFile(zip_path, 'r') as zipf:
            zipf.extractall(repo_dir)
            os.rename(os.path.join(repo_dir, f"bible_{lang}.db"), extract_path)

        try:
            conn = sqlite3.connect(extract_path)
            cur = conn.cursor()

            # list tables
            cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [t[0] for t in cur.fetchall()]
            print(f"📂 Tables: {tables}")

            # since "book" is a column in bible_xx table
            table_name = tables[0]  # should be bible_en, bible_hi, etc.
            cur.execute(f"SELECT DISTINCT book FROM {table_name} ORDER BY book;")
            books = [row[0] for row in cur.fetchall()]

            print(f"📖 Books in {table_name} ({len(books)} total):")
            print(books)

            conn.close()
        except Exception as e:
            print(f"❌ Error verifying {lang}: {e}")

        if os.path.exists(extract_path):
            os.remove(extract_path)

    else:
        print(f"⚠️ Missing file for {lang}")
