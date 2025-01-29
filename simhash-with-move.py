import os
from simhash import Simhash
from tqdm import tqdm
import shutil

# Folder to store unique files
unique_folder = "unique_folder"
total_size_before_deduplication = 0
total_size_after_deduplication = 0

# Function to collect all file paths from the provided folder
def get_files_from_folder(folder_path):
    file_paths = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.txt'):
                file_paths.append(os.path.join(root, file))
    return file_paths

# Function to calculate SimHash for a document
def calculate_simhash(file_path):
    """Compute SimHash for a file's content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
        simhash_value = Simhash(text.split())  # Split the content into tokens for SimHash
        return simhash_value
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None

# Function to calculate Hamming distance between two SimHashes
def hamming_distance(hash1, hash2):
    return hash1.distance(hash2)

# Function to deduplicate files based on SimHash similarity
def deduplicate_files(file_paths, simhashes, folder_path, duplicates_folder, threshold=3):
    global total_size_after_deduplication, total_size_before_deduplication
    unique_files = []
    
    # Create folder for duplicates if not existing
    os.makedirs(duplicates_folder, exist_ok=True)
    
    for i in tqdm(range(len(simhashes)), desc="Processing files", unit="file"):
        file_path = file_paths[i]
        simhash = simhashes[i]
        data_size = os.path.getsize(file_path)
        total_size_before_deduplication += data_size
        
        # Check if the file is a near-duplicate by comparing with previous unique files
        is_duplicate = False
        for j in range(len(unique_files)):
            if hamming_distance(simhash, simhashes[unique_files[j]]) <= threshold:
                is_duplicate = True
                break

        if is_duplicate:
            # Move duplicate file to the duplicates folder
            duplicate_file_path = os.path.join(duplicates_folder, os.path.basename(file_path))
            shutil.move(file_path, duplicate_file_path)
        else:
            unique_files.append(i)  # Store the index of the unique file
            total_size_after_deduplication += data_size

    return [file_paths[i] for i in unique_files]

# Function to compute SimHashes and deduplicate files
def simhash_computation(file_paths, folder_path, duplicates_folder, threshold=3):
    simhashes = []
    
    # Compute SimHash for all files
    for file_path in tqdm(file_paths, desc="Computing SimHashes", unit="file"):
        simhash = calculate_simhash(file_path)
        if simhash:
            simhashes.append(simhash)
    
    # Perform deduplication
    unique_files = deduplicate_files(file_paths, simhashes, folder_path, duplicates_folder, threshold)
    return unique_files

if __name__ == "__main__":
    folder_path = "D:/de_duplication nlp/"  # Folder containing the text files
    duplicates_folder = "D:/de_duplication nlp/duplicates_folder/"  # Folder to store duplicate files
    
    # Get all file paths from the folder
    file_paths = get_files_from_folder(folder_path)
    
    # Perform SimHash computation and deduplication
    unique_files = simhash_computation(file_paths, folder_path, duplicates_folder)
    
    # Output the results
    with open('unique_files.txt', 'w') as f:
        f.write(f"Total files before deduplication: {len(file_paths)}\n")
        f.write(f"Total size before deduplication: {total_size_before_deduplication / (1024 * 1024)} MB\n")
        f.write(f"Total files after deduplication: {len(unique_files)}\n")
        f.write(f"Total size after deduplication: {total_size_after_deduplication / (1024 * 1024)} MB\n")
        for file_path in unique_files:
            f.write(f"{file_path}\n")
