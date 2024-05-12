import sys
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

def count_figures_total(xml_paths):
    total_figures = []
    for xml_path in xml_paths:
        with open(xml_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'xml')
            # Contar el número de etiquetas <figure>
            figures_count = len(soup.find_all('figure'))
            total_figures.append(figures_count)
    return total_figures

def visualize_total_figures(xml_paths, total_figures, output_filename):
    plt.bar(xml_paths, total_figures, color='skyblue')
    plt.xlabel('XMLs')
    plt.ylabel('Total Figures')
    plt.title('Total Number of Figures for Each XML')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(output_filename)
    plt.close()

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <output_filename> <path_to_xml1> <path_to_xml2> ...")
        return

    output_filename = sys.argv[1]
    xml_paths = sys.argv[2:]
    total_figures = count_figures_total(xml_paths)
    print("Total number of figures for each XML:", total_figures)
    visualize_total_figures(xml_paths, total_figures, output_filename)

if __name__ == "__main__":
    main()
