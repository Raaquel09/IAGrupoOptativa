import os
import re
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from sentence_transformers import SentenceTransformer
from bertopic import BERTopic
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim.models.coherencemodel import CoherenceModel
from gensim.corpora.dictionary import Dictionary
import json

# Check if NLTK packages are already downloaded
try:
    nltk.data.find('corpora/stopwords.zip')
    nltk.data.find('corpora/wordnet.zip')
except LookupError:
    # Download NLTK packages if not found
    nltk.download('stopwords')
    nltk.download('wordnet')

# Initialize lemmatizer and stopwords
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    text = text.lower()  # Lowercase
    text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stop_words]  # Lemmatize and remove stopwords
    return words

def parse_tei_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        abstracts = []
        for abstract_elem in root.findall(".//{http://www.tei-c.org/ns/1.0}abstract"):
            abstract_text = ""
            for p_elem in abstract_elem.findall(".//{http://www.tei-c.org/ns/1.0}p"):
                if p_elem.text:
                    abstract_text += p_elem.text.strip() + " "
            abstracts.append(preprocess_text(abstract_text.strip()))
        return abstracts
    except Exception as e:
        print(f"Error parsing TEI XML file {file_path}: {e}")
        return []

def save_normalized_matrix(matrix, file_path):
    np.savetxt(file_path, matrix, fmt='%f')

def find_optimal_clusters(similarity_matrix, min_clusters=2, max_clusters=None):
    if max_clusters is None:
        max_clusters = min(20, len(similarity_matrix) // 2)  # Dynamically set max clusters
    silhouette_scores = []
    distance_matrix = 1 - similarity_matrix
    distance_matrix[distance_matrix < 0] = 0  # Ensure non-negative values
    for n_clusters in range(min_clusters, max_clusters + 1):
        clustering = AgglomerativeClustering(n_clusters=n_clusters, metric='precomputed', linkage='complete')
        cluster_labels = clustering.fit_predict(distance_matrix)
        silhouette_avg = silhouette_score(distance_matrix, cluster_labels, metric='precomputed')
        silhouette_scores.append(silhouette_avg)
    optimal_clusters = np.argmax(silhouette_scores) + min_clusters
    return optimal_clusters

def calculate_coherence_score(topics, abstracts):
    # Check if topics is a list
    if isinstance(topics, int):
        print("No topics found for coherence calculation.")
        return None

    # Create a dictionary and corpus for coherence calculation
    texts = [abstract for abstract in abstracts]
    dictionary = Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    # Convert BERTopic's topics to the required format
    topics_token_ids = [[dictionary.token2id[word] for word in abstracts[i]] for i in range(len(abstracts))]

    # Coherence Model
    coherence_model = CoherenceModel(topics=topics_token_ids, texts=texts, dictionary=dictionary, coherence='c_v')
    coherence = coherence_model.get_coherence()
    return coherence

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
    abstract_embeddings = sbert_model.encode([" ".join(doc) for doc in abstracts])
    similarity_matrix = cosine_similarity(abstract_embeddings)

    scaler = MinMaxScaler()
    normalized_matrix = scaler.fit_transform(similarity_matrix)

    output_matrix_file = input("Enter the path to save the normalized similarity matrix: ")
    save_normalized_matrix(normalized_matrix, output_matrix_file)
    print(f"Normalized similarity matrix saved to: {output_matrix_file}")

    optimal_clusters = find_optimal_clusters(similarity_matrix)
    print(f"Optimal number of clusters: {optimal_clusters}")
    distance_matrix = 1 - similarity_matrix
    distance_matrix[distance_matrix < 0] = 0  # Ensure non-negative values
    clustering = AgglomerativeClustering(n_clusters=optimal_clusters, metric='precomputed', linkage='complete')
    labels = clustering.fit_predict(distance_matrix)

    df = pd.DataFrame({
        'document': filenames,
        'AgglomerativeClustering': labels
    })
    print(df)

    pca = PCA(n_components=2)
    abstract_embeddings_reduced = pca.fit_transform(abstract_embeddings)

    plt.scatter(abstract_embeddings_reduced[:, 0], abstract_embeddings_reduced[:, 1], c=labels, cmap='viridis')
    plt.title('Agglomerative Clustering Result (with PCA)')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.colorbar(label='Cluster')

    output_image_path = os.path.join(output_image_folder, 'clustering_result_agglomerative.png')
    plt.savefig(output_image_path)

    num_clusters_agglomerative = len(np.unique(labels))
    print(f"Agglomerative Clustering: {num_clusters_agglomerative} clusters")
    print(f"Clustering image saved to: {output_image_path}")

    # BERTopic Topic Modeling
    topic_model = BERTopic(nr_topics=None, min_topic_size=2, verbose=True)
    topics, probabilities = topic_model.fit_transform([" ".join(doc) for doc in abstracts])

    # Calculate coherence score for BERTopic
    #coherence_score = calculate_coherence_score(topics, abstracts)
    #print(f"\nCoherence Score for BERTopic: {coherence_score}")
    
    print("\nTopics found by BERTopic:")
    topic_info = topic_model.get_topic_info()
    print(topic_info)

    # Print documents and their assigned topics
    for i, filename in enumerate(filenames):
        topic = topics[i]
        probability = probabilities[i]
        print(f"{filename} belongs to Topic {topic} with probability {probability:.4%}")
    
    # Collect output data
    output_data = []
    for i, filename in enumerate(filenames):
        topic = topics[i]
        probability = float(probabilities[i])  # Convert to native Python float
        similarity_info = {}
        for j, other_filename in enumerate(filenames):
            if i != j:  # Exclude self-similarity
                similarity_info[other_filename] = float(similarity_matrix[i][j])  # Convert to native Python float
        output_data.append({
            "filename": filename,
            "topic": topic,
            "probability": probability,
            "similarities": similarity_info
        })

    # Save output data to JSON file
    with open("Abstract_And_topics.json", "w", encoding="utf-8") as json_file:
        json.dump(output_data, json_file, ensure_ascii=False, indent=4)

    print(f"Extracted data from {len(output_data)} files and saved to 'Abstract_And_topics.json'")

if __name__ == "__main__":
    main()
