"""
Assignment 2: File Organisation Script
Automatically organises files in the Downloads folder into subfolders
Author: Opoka Eric
Registration: U/24/10784/EVE
Student Number: 2400710784
"""

import os
import shutil
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("file_organiser.log"),
        logging.StreamHandler()
    ]
)

# File category mappings
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff"],
    "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md", ".csv", ".json", ".xml"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
    "Audio": [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a"],
    "Video": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv"],
    "Programs": [".exe", ".msi", ".bat", ".sh", ".ps1", ".app"],
    "Code": [".py", ".js", ".ts", ".html", ".css", ".cpp", ".c", ".java", ".rb", ".go", ".rs"],
    "Torrents": [".torrent"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
    "Spreadsheets": [".xls", ".xlsx", ".ods", ".numbers"],
}

UNCATEGORISED = "Uncategorised"


def get_category(filename):
    """Determine the category for a given filename based on its extension."""
    ext = Path(filename).suffix.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return UNCATEGORISED


def organise_downloads(download_path=None):
    """
    Organise files in the given directory into subfolders based on file type.
    If no path is provided, uses the default Downloads folder.
    """
    if download_path is None:
        download_path = str(Path.home() / "Downloads")

    downloads_dir = Path(download_path)

    if not downloads_dir.exists():
        logging.error(f"Directory does not exist: {download_path}")
        return

    logging.info(f"Starting file organisation in: {download_path}")

    files_moved = 0
    errors = 0

    for item in downloads_dir.iterdir():
        if not item.is_file():
            continue

        filename = item.name
        # Skip the script itself and log file
        if filename in (__file__, "file_organiser.log"):
            continue

        category = get_category(filename)
        category_dir = downloads_dir / category

        try:
            category_dir.mkdir(exist_ok=True)
            destination = category_dir / filename

            # Handle name conflicts by appending a number
            counter = 1
            while destination.exists():
                stem = item.stem
                suffix = item.suffix
                destination = category_dir / f"{stem}_{counter}{suffix}"
                counter += 1

            shutil.move(str(item), str(destination))
            logging.info(f"Moved: {filename} -> {category}/")
            files_moved += 1

        except PermissionError as e:
            logging.error(f"Permission denied for {filename}: {e}")
            errors += 1
        except Exception as e:
            logging.error(f"Error moving {filename}: {e}")
            errors += 1

    logging.info(f"Organisation complete. Files moved: {files_moved}, Errors: {errors}")
    return files_moved, errors


if __name__ == "__main__":
    print("=" * 60)
    print("FILE ORGANISATION SCRIPT")
    print("Author: Opoka Eric | U/24/10784/EVE | 2400710784")
    print("=" * 60)

    # Check for command-line argument for custom directory
    import sys
    target_path = sys.argv[1] if len(sys.argv) > 1 else None

    if target_path:
        print(f"\nOrganising directory: {target_path}")
    else:
        print("\nNo path provided. Using default Downloads folder.")

    confirm = input("\nProceed with file organisation? (y/n): ").strip().lower()
    if confirm == "y":
        moved, errs = organise_downloads(target_path)
        print(f"\nDone! {moved} files organised, {errs} errors.")
    else:
        print("Operation cancelled.")
