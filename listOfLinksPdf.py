import sys
import json
from PyPDF2 import PdfReader
import re

def extract_links(pdf_path):
    all_links = []
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        for page in reader.pages:
            text = page.extract_text()
            links = re.findall(r'https?://\S+', text)
            all_links.extend(links)
    return all_links

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <path_to_pdf1> <path_to_pdf2> ...")
        return

    pdf_paths = sys.argv[2:]
    results = {}
    for pdf_path in pdf_paths:
        links = extract_links(pdf_path)
        results[pdf_path] = links

    # Obtener el nombre del archivo de salida proporcionado por el usuario
    output_file = sys.argv[1]

    # Escribir los resultados en el archivo JSON especificado
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Los resultados se han guardado en '{output_file}'.")

if __name__ == "__main__":
    main()

