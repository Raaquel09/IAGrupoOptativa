import sys
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup


def extract_abstract_from_xml(xml_path):
    abstract = ""
    with open(xml_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'xml')
        abstract_tag = soup.find('abstract')
        if abstract_tag:
            abstract = abstract_tag.get_text(separator=' ', strip=True)
    return abstract

def combine_abstracts(xml_paths):
    combined_abstract = ""
    for xml_path in xml_paths:
        abstract = extract_abstract_from_xml(xml_path)
        combined_abstract += abstract + " "
    return combined_abstract

def generate_wordcloud(text, output_file):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    wordcloud.to_file(output_file)

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <output_file> <path_to_xml1> <path_to_xml2> ...")
        return

    output_file = sys.argv[1]
    xml_paths = sys.argv[2:]
    combined_abstract = combine_abstracts(xml_paths)
    generate_wordcloud(combined_abstract, output_file)

if __name__ == "__main__":
    main()
