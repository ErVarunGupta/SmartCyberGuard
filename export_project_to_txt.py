import os

# ========= CONFIG =========
PROJECT_ROOT = r"D:\AI & ML PROJECTS\smart_laptop_analyzer"
OUTPUT_FILE = "smart_laptop_analyzer_selected_files.txt"

# folders to skip
EXCLUDE_DIRS = {
    "venv",
    "__pycache__",
    ".git",
    ".idea",
    ".vscode",
    "build"
    # NOTE: dist is NOT excluded so .exe can be picked
}

# allowed file extensions
INCLUDE_EXTENSIONS = {
    ".py",
    ".txt",
    ".spec"
}
# ==========================

def is_included_file(filename):
    return any(filename.lower().endswith(ext) for ext in INCLUDE_EXTENSIONS)

def export_project():
    with open(OUTPUT_FILE, "w", encoding="utf-8", errors="ignore") as out:
        for root, dirs, files in os.walk(PROJECT_ROOT):

            # remove excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                if not is_included_file(file):
                    continue

                file_path = os.path.join(root, file)

                out.write("\n" + "=" * 80 + "\n")
                out.write(f"FILE PATH: {file_path}\n")
                out.write("=" * 80 + "\n\n")

                try:
                    # .exe is binary → don't dump contents
                    if file.lower().endswith(".exe"):
                        size_kb = os.path.getsize(file_path) / 1024
                        out.write(f"[BINARY FILE]\nSize: {size_kb:.2f} KB\n")
                    else:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                            out.write(f.read())

                except Exception as e:
                    out.write(f"[ERROR READING FILE]: {e}")

                out.write("\n\n")

    print("\n✅ Selected files exported successfully!")
    print(f"📄 Output file: {OUTPUT_FILE}")

if __name__ == "__main__":
    export_project()