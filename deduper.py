
import os
import hashlib
from PIL import Image  # For perceptual hashing
import imagehash
def find_duplicates(directory, hash_type="md5"):
    """Finds duplicate images based on their hash values.

    Args:
        directory: The directory to search for images.
        hash_type: The type of hash to use ("md5", "sha256", or "phash").

    Returns:
        A list of lists, where each inner list contains duplicate file paths.
    """

    hashes = {}
    duplicates = []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            try:
                with open(filepath, 'rb') as f:
                    file_hash = None
                    if hash_type == "md5":
                        file_hash = hashlib.md5(f.read()).hexdigest()
                    elif hash_type == "sha256":
                        file_hash = hashlib.sha256(f.read()).hexdigest()
                    elif hash_type == "phash":
                        image = Image.open(filepath)
                        file_hash = imagehash.phash(image)  # Perceptual hash
                    else:
                        raise ValueError("Invalid hash_type. Choose 'md5', 'sha256', or 'phash'")

                if file_hash in hashes:
                    duplicates.append([filepath, hashes[file_hash]])  # Store both paths
                else:
                    hashes[file_hash] = filepath
            except (OSError, IOError, ValueError) as e:
                print(f"Error processing {filepath}: {e}")

    return duplicates

def remove_duplicates(duplicates, ask_confirmation=True):
    """Removes duplicate files.

    Args:
        duplicates: A list of lists of duplicate file paths.
        ask_confirmation: If True, ask for confirmation before deletion.
    """

    for group in duplicates:
        print(f"\nDuplicate group ({len(group)} files):")
        for i, path in enumerate(group):
            print(f"{i + 1}. {path}")

        if ask_confirmation:
            choice = "y"
            if choice.lower() != 'y':
                continue

        # Keep the first file in the group, delete the rest
        for path in group[1:]:
            try:
                os.remove(path)
                print(f"Removed: {path}")
            except OSError as e:
                print(f"Error removing {path}: {e}")

if __name__ == "__main__":
    image_dir = r".\tmp"  # Replace with your directory
    hash_type = "phash"  # For more robust comparison, but slower

    duplicates = find_duplicates(image_dir, hash_type)
    if duplicates:
        remove_duplicates(duplicates)
    else:
        print("No duplicate images found.")
