import os
import zipfile

# Only per-language DB files (no bible.db)
db_files = [
    "bible_en.db",
    "bible_hi.db",
    "bible_kn.db",
    "bible_ml.db",
    "bible_ta.db",
    "bible_te.db"
]

def get_size(path):
    """Return human readable size"""
    size = os.path.getsize(path)
    return f"{size/1024/1024:.2f} MB"

for db in db_files:
    if os.path.exists(db):
        zip_name = db.replace(".db", ".zip")
        
        # Create zip archive
        with zipfile.ZipFile(zip_name, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            zf.write(db, arcname=os.path.basename(db))
        
        print(f"📖 {db}: {get_size(db)} → {zip_name}: {get_size(zip_name)}")
    else:
        print(f"❌ {db} not found")
