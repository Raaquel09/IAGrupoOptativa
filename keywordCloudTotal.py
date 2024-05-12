import sys
from PyPDF2 import PdfReader
import matplotlib.pyplot as plt
from wordcloud import WordCloud

def extract_abstract_from_pdf(pdf_path):
    abstract = ""
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        try:
            abstract = reader.pages[0].extract_text()
        except:
            pass
    return abstract

def combine_abstracts(pdf_paths):
    combined_abstract = ""
    for pdf_path in pdf_paths:
        abstract = extract_abstract_from_pdf(pdf_path)
        combined_abstract += abstract + " "
    return combined_abstract

def generate_wordcloud(text, output_path):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    wordcloud.to_file(output_path)

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <output_image_path> <path_to_pdf1> <path_to_pdf2> ...")
        return

    output_image_path = sys.argv[1]
    pdf_paths = sys.argv[2:]
    combined_abstract = combine_abstracts(pdf_paths)
    generate_wordcloud(combined_abstract, output_image_path)

if __name__ == "__main__":
    main()
