import os
from simhash import Simhash
from typing import List

# Function to calculate SimHash for a document
def calculate_simhash(text: str) -> Simhash:
    tokens = text.split()
    return Simhash(tokens)

# Function to calculate the Hamming distance between two SimHashes
def hamming_distance(hash1: Simhash, hash2: Simhash) -> int:
    return hash1.distance(hash2)

# Function to detect near-duplicate documents based on SimHash
def find_near_duplicates(documents: List[str], file_names: List[str], threshold: int = 3) -> List[List[int]]:
    simhashes = [calculate_simhash(doc) for doc in documents]
    duplicates = []
    
    for i in range(len(simhashes)):
        for j in range(i + 1, len(simhashes)):
            dist = hamming_distance(simhashes[i], simhashes[j])
            if dist <= threshold:
                duplicates.append((file_names[i], file_names[j]))
    
    return duplicates

# Function to read text files from a folder
def read_documents_from_folder(folder_path: str) -> (List[str], List[str]):
    documents = []
    file_names = []

    # Iterate through all files in the folder
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        # Check if it is a file and has a .txt extension
        if os.path.isfile(file_path) and file_name.endswith(".txt"):
            with open(file_path, 'r', encoding='utf-8') as file:
                documents.append(file.read())
                file_names.append(file_name)
    
    return documents, file_names

# Example usage with folder input
if __name__ == "__main__":
    folder_path = "D:/de_duplication nlp/"  # Change this to the path where your text files are stored
    
    # Read all documents and their file names from the folder
    documents, file_names = read_documents_from_folder(folder_path)
    
    # Check for near-duplicate documents
    duplicates = find_near_duplicates(documents, file_names, threshold=3)
    
    # Print the result
    if duplicates:
        print("Near-duplicate documents detected:")
        for file1, file2 in duplicates:
            print(f"File '{file1}' is similar to File '{file2}'")
    else:
        print("No near-duplicate documents found.")
