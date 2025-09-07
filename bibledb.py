import sqlite3
import zipfile
import os

# List of zipped DB files
zip_files = [
    "bible_en.zip",
    "bible_hi.zip",
    "bible_kn.zip",
    "bible_ml.zip",
    "bible_ta.zip",
    "bible_te.zip"
]

for zip_file in zip_files:
    try:
        with zipfile.ZipFile(zip_file, 'r') as z:
            # Find the .db file inside the zip
            db_name = [name for name in z.namelist() if name.endswith('.db')][0]
            print(f"📦 {zip_file} contains DB: {db_name}")

            # Extract the DB temporarily
            temp_path = os.path.join(".", db_name)
            z.extract(db_name, ".")

            # Connect to the extracted DB
            conn = sqlite3.connect(temp_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [t[0] for t in cursor.fetchall()]
            print(f"   🗂 Tables: {tables}")
            conn.close()

            # Remove the temporary DB file
            os.remove(temp_path)

    except Exception as e:
        print(f"❌ Error with {zip_file}: {e}")
