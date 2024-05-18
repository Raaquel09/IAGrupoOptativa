import os
import xml.etree.ElementTree as ET
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

def parse_tei_acknowledgements(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        acknowledgements = []
        for ack_elem in root.findall(".//{http://www.tei-c.org/ns/1.0}div[@type='acknowledgement']"):
            ack_text = "".join(p_elem.text.strip() for p_elem in ack_elem.findall(".//{http://www.tei-c.org/ns/1.0}p") if p_elem.text)
            acknowledgements.append(ack_text.strip())

        return acknowledgements
    except Exception as e:
        print(f"Error parsing TEI XML file {file_path}: {e}")
        return []

def main():
    # Prompt user for input directory
    input_dir = input("Enter the input directory path containing TEI XML files: ")
    input_dir = os.path.normpath(input_dir)
    if not os.path.isdir(input_dir):
        print("Error: Invalid directory path.", input_dir)
        return

    # Load a pretrained NER model from Hugging Face
    model_name = "Jean-Baptiste/roberta-large-ner-english"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name)
    ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer)
    
    acknowledgements = []
    filenames = []
    for filename in os.listdir(input_dir):
        if filename.endswith(".xml"):
            xml_file = os.path.join(input_dir, filename)
            ack_found = parse_tei_acknowledgements(xml_file)
            if ack_found:
                acknowledgements.extend(ack_found)
                filenames.extend([filename] * len(ack_found))

    print(f"Found {len(acknowledgements)} acknowledgements.")
    if not acknowledgements:
        print("No acknowledgements found in the input directory.")
        return
    
    # Apply NER to each XML acknowledgment
    for ack, filename in zip(acknowledgements, filenames):
        print(f"File: {filename}")
        print(f"Acknowledgment: {ack}")
        entities = ner_pipeline(ack)
        print("Entities:")
        for entity in entities:
            print(f"- {entity['entity']}: {entity['word']}")
        print("="*50)

if __name__ == "__main__":
    main()
