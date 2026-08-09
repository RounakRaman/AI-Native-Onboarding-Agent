import os
import zipfile

def create_app_zip():
    app_dir = os.path.dirname(os.path.abspath(__file__))
    zip_filename = os.path.join(app_dir, "setup_copilot_streamlit_app.zip")
    
    print(f"Creating ZIP file at: {zip_filename}")
    
    ignore_files = {"setup_copilot_streamlit_app.zip", "__pycache__", ".git", ".DS_Store"}
    
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(app_dir):
            # Exclude pycache dirs
            dirs[:] = [d for d in dirs if d not in ignore_files and not d.endswith(".pyc")]
            for file in files:
                if file in ignore_files or file.endswith(".pyc"):
                    continue
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, app_dir)
                zipf.write(file_path, arcname)
                print(f"  Added: {arcname}")
                
    print(f"Successfully created {zip_filename} ({os.path.getsize(zip_filename)} bytes).")

if __name__ == "__main__":
    create_app_zip()
