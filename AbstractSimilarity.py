import os
import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import PCA
from sentence_transformers import SentenceTransformer
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.metrics import silhouette_score


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

def perform_clustering(abstract_embeddings, num_clusters, output_file=None):
    similarity_matrix = cosine_similarity(abstract_embeddings, abstract_embeddings)
    similarity_matrix = np.clip(similarity_matrix, 0, 1)     
    clustering = AgglomerativeClustering(n_clusters=num_clusters, linkage='complete', metric='precomputed')
    labels = clustering.fit_predict(1 - similarity_matrix)
    
    if output_file:
        # Write similarity matrix to file
        np.savetxt(output_file, similarity_matrix, fmt='%.4f', delimiter='\t')
    
    return labels

def perform_topic_modeling(abstracts, num_topics=5):
    vectorizer = CountVectorizer(stop_words='english')
    dtm = vectorizer.fit_transform(abstracts)
    lda = LatentDirichletAllocation(n_components=num_topics, random_state=0)
    lda.fit(dtm)
    return lda, vectorizer

def display_topics(model, feature_names, num_top_words):
    topics = []
    for topic_idx, topic in enumerate(model.components_):
        topics.append(" ".join([feature_names[i] for i in topic.argsort()[:-num_top_words - 1:-1]]))
    return topics

def find_optimal_topics(abstracts, max_topics=10):
    vectorizer = CountVectorizer(stop_words='english')
    dtm = vectorizer.fit_transform(abstracts)
    coherence_scores = []
    
    for n_topics in range(2, max_topics + 1):
        lda = LatentDirichletAllocation(n_components=n_topics, random_state=0)
        lda.fit(dtm)
        
        feature_names = vectorizer.get_feature_names_out()
        topic_words = []
        for topic in lda.components_:
            top_words = [feature_names[i] for i in topic.argsort()[:-10 - 1:-1]]
            topic_words.append(top_words)
        
        coherence_scores.append(0)  # Placeholder, as we're not using coherence score in this version
    
    optimal_topics = coherence_scores.index(max(coherence_scores)) + 2
    return optimal_topics

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
    
    # Perform topic modeling to determine the number of clusters (topics)
    lda_model, vectorizer = perform_topic_modeling(abstracts)
    num_clusters = lda_model.n_components
    
    if num_topics is None:
        num_topics = find_optimal_topics(abstracts)
    
    labels = perform_clustering(abstract_embeddings, num_clusters=num_topics, output_file=output_file)
    lda_model, vectorizer = perform_topic_modeling(abstracts, num_topics=num_topics)
    topics = display_topics(lda_model, vectorizer.get_feature_names_out(), 10)

    df = pd.DataFrame({'document': filenames, 'cluster': labels})
    print(df)
    
    # Print number of clusters found
    print(f"Found {num_topics} clusters.")
    
    for cluster_num in range(num_topics):
        print(f"Cluster {cluster_num} topics:")
        cluster_indices = df[df['cluster'] == cluster_num].index
        cluster_abstracts = [abstracts[i] for i in cluster_indices]
        cluster_dtm = vectorizer.transform(cluster_abstracts)
        cluster_topic_distribution = lda_model.transform(cluster_dtm)
        dominant_topic = cluster_topic_distribution.mean(axis=0).argmax()
        print(f"  Dominant topic: {topics[dominant_topic]}")

    #Determine the number of principal components based on the clusters
    num_topics = len(np.unique(labels))
    num_principal_components = min(num_topics, 2) #Minumum of 2 clusters
    
    # Perform PCA on the abstract embeddings
    pca = PCA(n_components=2)
    abstract_embeddings_reduced = pca.fit_transform(abstract_embeddings)
    
    plt.scatter(abstract_embeddings_reduced[:, 0], abstract_embeddings_reduced[:, 1], c=labels, cmap='viridis', s=50, alpha=0.5)
    plt.title('Clustering Result (with PCA)')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.colorbar(label='Cluster')
    
    
    output_image_path = os.path.join(output_image_folder, 'clustering_result.png')
    plt.savefig(output_image_path)
    print(f"Clustering image saved to: {output_image_path}")

if __name__ == "__main__":
    main()
