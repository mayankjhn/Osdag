
import sqlite3
import subprocess
from importlib.resources import files
import shutil
from pathlib import Path
import sys

# Add src to path
REPO_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

def create_sqlite():
    try:
        # Get paths
        # We need osdag_core, so ensure it can be found.
        # It's in src/osdag_core
        
        sqlpath = files('osdag_core.data.ResourceFiles.Database').joinpath('Intg_osdag.sql')
        sqlitepath = files('osdag_core.data.ResourceFiles.Database').joinpath('Intg_osdag.sqlite')

        print(f"SQL Path: {sqlpath}")
        print(f"SQLite Path: {sqlitepath}")

        if not sqlpath.exists():
            print(f"[ERROR] SQL file not found: {sqlpath}")
            return

        # Determine if we need to create or update
        needs_creation = not sqlitepath.exists()
        needs_update = (sqlitepath.exists() and 
                    (sqlitepath.stat().st_size == 0 or 
                        sqlitepath.stat().st_mtime < sqlpath.stat().st_mtime - 1))

        print(f"Needs Creation: {needs_creation}")
        print(f"Needs Update: {needs_update}")

        if not needs_creation and not needs_update:
            print("[INFO] Database is up to date (forced update anyway for safety)")
            # return # FORCE UPDATE for testing

        # Backup logic removed to keep workspace clean
        # Create/update database

        # Create/update database
        target_path = sqlitepath
        if needs_update or True: # Force logic
            # target_path = sqlitepath # In main it uses temp if update.
            pass

        # Use Python sqlite3
        try:
            with open(sqlpath, 'r', encoding='utf-8') as sql_file:
                sql_content = sql_file.read()
            
            # Ensure dir exists
            sqlitepath.parent.mkdir(parents=True, exist_ok=True)
            
            # If exists, delete to be sure
            if sqlitepath.exists():
                sqlitepath.unlink()

            conn = sqlite3.connect(sqlitepath)
            conn.executescript(sql_content)
            conn.close()
            
            print(f"[INFO] Database created using Python sqlite3")
            
        except Exception as e:
            print(f"[ERROR] Python sqlite3 failed: {e}")
            raise

    except Exception as e:
        print(f"[ERROR] Database setup failed: {e}")

if __name__ == "__main__":
    create_sqlite()
