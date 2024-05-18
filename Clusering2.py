import os
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.preprocessing import MinMaxScaler
from sentence_transformers import SentenceTransformer
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

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

def perform_topic_modeling_sklearn(abstracts):
    vectorizer = CountVectorizer(stop_words='english')
    dtm = vectorizer.fit_transform(abstracts)
    # Determine the optimal number of topics using perplexity
    perplexities = []
    for n in range(1, 10):
        lda = LatentDirichletAllocation(n_components=n, random_state=0, max_iter=50)
        lda.fit(dtm)
        perplexities.append(lda.perplexity(dtm))
    optimal_topics = np.argmin(perplexities) + 1
    lda = LatentDirichletAllocation(n_components=optimal_topics, random_state=0)
    lda.fit(dtm)
    return lda, vectorizer, optimal_topics

def display_topics(model, feature_names, num_top_words):
    topics = []
    for topic_idx, topic in enumerate(model.components_):
        topics.append(" ".join([feature_names[i] for i in topic.argsort()[:-num_top_words - 1:-1]]))
    return topics

def save_normalized_matrix(matrix, file_path):
    np.savetxt(file_path, matrix, fmt='%f')

def main():
    input_dir = input("Enter the path to the directory containing TEI XML files: ")
    input_dir = os.path.normpath(input_dir)
    if not os.path.isdir(input_dir):
        print("Invalid directory path:", input_dir)
        return

    output_image_folder = input("Enter the path to the folder to save the clustering image: ")
    output_image_folder = os.path.normpath(output_image_folder)
    if not os.path.isdir(output_image_folder):
        print("Invalid directory path:", output_image_folder)
        return

    abstracts = []
    filenames = []
    for filename in os.listdir(input_dir):
        if filename.endswith(".xml"):
            xml_file = os.path.join(input_dir, filename)
            abstracts_found = parse_tei_xml(xml_file)
            if abstracts_found:
                abstracts.extend(abstracts_found)
                filenames.extend([filename] * len(abstracts_found))

    print(f"Found {len(abstracts)} abstracts.")
    if not abstracts:
        print("No abstracts found in the specified directory.")
        return

    sbert_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')
    abstract_embeddings = sbert_model.encode(abstracts)
    similarity_matrix = cosine_similarity(abstract_embeddings)

    # Normalize the similarity matrix
    scaler = MinMaxScaler()
    normalized_matrix = scaler.fit_transform(similarity_matrix)

    # Save the normalized matrix to a file
    output_matrix_file = input("Enter the path to save the normalized similarity matrix: ")
    save_normalized_matrix(normalized_matrix, output_matrix_file)
    print(f"Normalized similarity matrix saved to: {output_matrix_file}")

    # Perform agglomerative clustering
    clustering_agglomerative = AgglomerativeClustering()
    labels_agglomerative = clustering_agglomerative.fit_predict(normalized_matrix)

    # Create DataFrame
    df = pd.DataFrame({
        'document': filenames,
        'AgglomerativeClustering': labels_agglomerative
    })
    print(df)

    # Visualize clusters using PCA
    pca = PCA(n_components=2)
    abstract_embeddings_reduced = pca.fit_transform(abstract_embeddings)

    plt.scatter(abstract_embeddings_reduced[:, 0], abstract_embeddings_reduced[:, 1], c=labels_agglomerative, cmap='viridis')
    plt.title('Agglomerative Clustering Result (with PCA)')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.colorbar(label='Cluster')

    output_image_path = os.path.join(output_image_folder, 'clustering_result_agglomerative.png')
    plt.savefig(output_image_path)
    
    # Print number of clusters for Agglomerative Clustering
    num_clusters_agglomerative = len(np.unique(labels_agglomerative))
    print(f"Agglomerative Clustering: {num_clusters_agglomerative} clusters")
    print(f"Clustering image saved to: {output_image_path}")

    # Print topics
    lda_model_sklearn, vectorizer_sklearn, num_topics_sklearn = perform_topic_modeling_sklearn(abstracts)
    topics_sklearn = display_topics(lda_model_sklearn, vectorizer_sklearn.get_feature_names_out(), 10)
    print("\nTopics found by sklearn LDA:")
    for idx, topic in enumerate(topics_sklearn):
        print(f"Topic {idx}: {topic}")

    # Find dominant topic for each document in sklearn LDA
    dtm = vectorizer_sklearn.transform(abstracts)
    lda_topics_sklearn = lda_model_sklearn.transform(dtm)
    dominant_topics_sklearn = np.argmax(lda_topics_sklearn, axis=1)
    for i, filename in enumerate(filenames):
        dominant_topic = dominant_topics_sklearn[i]
        topic_percentage = lda_topics_sklearn[i, dominant_topic]
        print(f"{filename} belongs to Topic {dominant_topic} with {topic_percentage * 100:.2f}%")

if __name__ == "__main__":
    main()