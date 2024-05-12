import sys
from PyPDF2 import PdfReader
import matplotlib.pyplot as plt
import io

def count_figures_total(pdf_paths):
    total_figures = []
    for pdf_path in pdf_paths:
        figures_count = 0
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            for page in reader.pages:
                figures_count += page.extract_text().count("Figure")
        total_figures.append(figures_count)
    return total_figures

def visualize_total_figures(pdf_paths, total_figures, output_filename):
    plt.bar(pdf_paths, total_figures, color='skyblue')
    plt.xlabel('PDFs')
    plt.ylabel('Total Figures')
    plt.title('Total Number of Figures for Each PDF')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Convertir el gráfico en un array de bytes
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Escribir el array de bytes en un archivo
    with open(output_filename, 'wb') as f:
        f.write(buf.read())

    plt.close()

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <output_filename> <path_to_pdf1> <path_to_pdf2> ...")
        return

    output_filename = sys.argv[1]
    pdf_paths = sys.argv[2:]
    total_figures = count_figures_total(pdf_paths)
    print("Total number of figures for each PDF:", total_figures)
    visualize_total_figures(pdf_paths, total_figures, output_filename)

if __name__ == "__main__":
    main()
