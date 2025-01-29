import os
from simhash import Simhash
from typing import List
from tqdm import tqdm  # Import tqdm for progress bar

# Function to calculate SimHash for a document
def calculate_simhash(text: str) -> Simhash:
    tokens = text.split()
    return Simhash(tokens)

# Function to calculate the Hamming distance between two SimHashes
def hamming_distance(hash1: Simhash, hash2: Simhash) -> int:
    return hash1.distance(hash2)

# Function to detect near-duplicate documents and delete one of the duplicates
def find_and_delete_near_duplicates(documents: List[str], file_names: List[str], folder_path: str, threshold: int = 3) -> List[str]:
    simhashes = [calculate_simhash(doc) for doc in documents]
    deleted_files = []
    
    # Using tqdm to show progress while comparing files
    for i in tqdm(range(len(simhashes)), desc="Processing files", unit="file"):
        for j in range(i + 1, len(simhashes)):
            dist = hamming_distance(simhashes[i], simhashes[j])
            if dist <= threshold:
                # If files are near-duplicates, delete one of them
                file_to_delete = file_names[j]
                file_to_delete_path = os.path.join(folder_path, file_to_delete)
                
                try:
                    os.remove(file_to_delete_path)  # Delete the file
                    deleted_files.append(file_to_delete)
                except Exception as e:
                    print(f"Error deleting file '{file_to_delete}': {e}")

    return deleted_files

# Function to read text files from a folder
def read_documents_from_folder(folder_path: str) -> (List[str], List[str]):
    documents = []
    file_names = []

    # Iterate through all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        # Check if it is a file and has a .txt extension
        if os.path.isfile(file_path) and file_name.endswith(".txt"):
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    documents.append(file.read())
                    file_names.append(file_name)
            except Exception as e:
                print(f"Error reading file '{file_name}': {e}")
    
    return documents, file_names

# Example usage with folder input
if __name__ == "__main__":
    folder_path = "D:/de_duplication nlp/"  # Change this to the path where your text files are stored
    
    # Read all documents and their file names from the folder
    documents, file_names = read_documents_from_folder(folder_path)
    #put sim hash here--
    
    # Find near-duplicates and delete them with progress indication
    deleted_files = find_and_delete_near_duplicates(documents, file_names, folder_path, threshold=3)
    
    # Print the result--optional line
    if deleted_files:
        print("The following near-duplicate files were deleted:")
        for file in deleted_files:
            print(f"File '{file}' has been deleted.")
    else:
        print("No near-duplicate documents found.")

#---document wale list me simhash use karna
simhash ka dictionary use karna
filename + simhash key value pair