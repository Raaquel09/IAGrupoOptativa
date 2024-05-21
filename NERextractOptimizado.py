import os
import xml.etree.ElementTree as ET
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
import json

# Function to parse acknowledgments from TEI XML files
def parse_tei_acknowledgements(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        ns = {'tei': 'http://www.tei-c.org/ns/1.0'}

        acknowledgements = []
        for ack_elem in root.findall(".//tei:div[@type='acknowledgement']", ns):
            ack_text = "".join(p_elem.text.strip() if p_elem.text else '' for p_elem in ack_elem.findall(".//tei:p", ns))
            acknowledgements.append(ack_text.strip())

        return acknowledgements
    except Exception as e:
        print(f"Error parsing TEI XML file {file_path}: {e}")
        return []

# Function to extract named entities from a text using the NER pipeline
def extract_named_entities(text, ner_pipeline):
    entities = ner_pipeline(text)
    structured_entities = [{'entity': ent['entity_group'], 'text': ent['word']} for ent in entities]
    return structured_entities

# Main function
def main():
    # Initialize the tokenizer and model for token classification
    tokenizer = AutoTokenizer.from_pretrained("Jean-Baptiste/roberta-large-ner-english")
    model = AutoModelForTokenClassification.from_pretrained("Jean-Baptiste/roberta-large-ner-english")
    
    # Initialize the NER pipeline
    ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

    # Get the input directory from the user
    input_dir = input("Enter the input directory path containing TEI XML files: ")

    # Initialize a list to hold all extracted data
    all_data = []

    # Iterate over all files in the input directory
    for file_name in os.listdir(input_dir):
        if file_name.endswith(".tei.xml"):
            file_path = os.path.join(input_dir, file_name)
            acknowledgements = parse_tei_acknowledgements(file_path)
            for ack_text in acknowledgements:
                entities = extract_named_entities(ack_text, ner_pipeline)
                if ack_text and entities:
                    file_data = {
                        "file_name": file_name,
                        "acknowledgment": ack_text,
                        "entities": entities
                    }
                    all_data.append(file_data)

    # Save the extracted data to a JSON file
    with open("extracted_acknowledgments2.json", "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=4)

    print(f"Extracted data from {len(all_data)} files and saved to 'extracted_acknowledgments2.json'")

# Run the main function
if __name__ == "__main__":
    main()
