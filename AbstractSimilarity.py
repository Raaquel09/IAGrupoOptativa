import os
import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

def parse_tei_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        abstracts = []
        for abstract_elem in root.findall(".//{http://www.tei-c.org/ns/1.0}abstract"):
            abstract_text = ""
            for p_elem in abstract_elem.findall(".//{http://www.tei-c.org/ns/1.0}p"):
                abstract_text += p_elem.text.strip() + " "
            abstracts.append(abstract_text.strip())

        return abstracts
    except Exception as e:
        print(f"Error parsing TEI XML file {file_path}: {e}")
        return []

def main():
    # Prompt user for input directory
    input_dir = input("Enter the path to the directory containing TEI XML files: ")
    input_dir = os.path.normpath(input_dir)
    if not os.path.isdir(input_dir):
        print("Invalid directory path:", input_dir)
        return

    # Prompt user for output file path
    output_file = input("Enter the path to save the similarity matrix (including file extension): ")

    # Prompt user for output folder for the image
    output_image_folder = input("Enter the path to the folder to save the clustering image: ")
    output_image_folder = os.path.normpath(output_image_folder)
    if not os.path.isdir(output_image_folder):
        print("Invalid directory path:", output_image_folder)
        return

    abstracts = []
    filenames = []  # To keep track of the filenames for future reference
    for filename in os.listdir(input_dir):
        if filename.endswith(".xml"):
            xml_file = os.path.join(input_dir, filename)
            abstracts_found = parse_tei_xml(xml_file)
            if abstracts_found:
                abstracts.extend(abstracts_found)
                filenames.extend([filename] * len(abstracts_found))

    # Print number of abstracts found
    print(f"Found {len(abstracts)} abstracts.")

    if not abstracts:
        print("No abstracts found in the specified directory.")
        return

    # Initialize SentenceTransformer model
    sbert_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

    # Encode abstracts into embeddings
    abstract_embeddings = sbert_model.encode(abstracts)

    # Compute cosine similarity between all pairs of abstracts
    similarity_matrix = cosine_similarity(abstract_embeddings, abstract_embeddings)

    # Normalize the similarity matrix
    similarity_matrix = np.clip(similarity_matrix, 0, 1)

    # Write similarity matrix to file
    np.savetxt(output_file, similarity_matrix, fmt='%.4f', delimiter='\t')
    
    # Perform Agglomerative Clustering
    clustering = AgglomerativeClustering(n_clusters=3, linkage='complete', metric='cosine')
    labels = clustering.fit_predict(similarity_matrix)

    # Print the clusters
    df = pd.DataFrame({'document': filenames, 'cluster': labels})
    print(df)
    
    # Apply PCA for dimensionality reduction
    pca = PCA(n_components=2)
    abstract_embeddings_reduced = pca.fit_transform(abstract_embeddings)
    
    # Plotting
    plt.scatter(abstract_embeddings_reduced[:, 0], abstract_embeddings_reduced[:, 1], c=labels, cmap='viridis')
    plt.title('Clustering Result (with PCA)')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.colorbar(label='Cluster')
    
    # Save the image to the specified folder
    output_image_path = os.path.join(output_image_folder, 'clustering_result.png')
    plt.savefig(output_image_path)
    print(f"Clustering image saved to: {output_image_path}")

if __name__ == "__main__":
    main()
