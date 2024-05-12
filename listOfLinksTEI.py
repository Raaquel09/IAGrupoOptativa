import sys
import json
from bs4 import BeautifulSoup
import re

def extract_links(xml_path):
    all_links = []
    with open(xml_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'xml')
        for elem in soup.find_all(text=True):
            links = re.findall(r'https?://\S+', elem)
            all_links.extend(links)
    return all_links

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <output_file> <path_to_xml1> <path_to_xml2> ...")
        return

    xml_paths = sys.argv[2:]
    results = {}
    for xml_path in xml_paths:
        links = extract_links(xml_path)
        results[xml_path] = links

    # Obtener el nombre del archivo de salida proporcionado por el usuario
    output_file = sys.argv[1]

    # Escribir los resultados en el archivo JSON especificado
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"Los resultados se han guardado en '{output_file}'.")

if __name__ == "__main__":
    main()
