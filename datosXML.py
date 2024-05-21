import os
import xml.etree.ElementTree as ET
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, DC
import json
import requests

def instance_entities(directory):
    id = 0
    papers = []
    authors = []
    orgs = []

    namespace = {'tei': 'http://www.tei-c.org/ns/1.0'}
    for archivo in os.listdir(directory):
        if archivo.endswith('.xml'):
            ruta_archivo = os.path.join(directory, archivo)

            tree = ET.parse(ruta_archivo)
            root = tree.getroot()

            title_element = root.find('.//tei:title', namespace)
            title = title_element.text if title_element is not None else 'unknown'

            author_element = root.find('.//tei:analytic/tei:author/tei:persName', namespace)
            if author_element is not None:
                forename_element = author_element.find('tei:forename', namespace)
                surname_element = author_element.find('tei:surname', namespace)
                author_name = forename_element.text if forename_element is not None else 'unknown'
                author_surname = surname_element.text if surname_element is not None else 'unknown'
                author = f"{author_name} {author_surname}"
            else:
                author_name = 'unknown'
                author_surname = 'unknown'
                author = 'unknown'

            organization_element = root.find('.//tei:orgName[@type="institution"]', namespace)
            org = organization_element.text if organization_element is not None else 'unknown'

            tei_header = root.find('tei:teiHeader', namespace)
            lang = tei_header.attrib.get('{http://www.w3.org/XML/1998/namespace}lang', 'unknown')

            date_element = root.find('.//tei:date[@type="published"]', namespace)
            date = date_element.text if date_element is not None else 'unknown'

            keywords_element = root.find('.//tei:keywords', namespace)
            keywords = [term_element.text for term_element in keywords_element.findall('tei:term', namespace)] if keywords_element is not None else 'unknown'



            papers.append({
                "document": ruta_archivo,
                "title": title,
                "author": author,
                "organization": org,
                "language": lang,
                "date": date,
                "id": id,
                "Topic": 0,
                "Similaritys": []
            })

            authors.append({
                "name": author_name,
                "surname": author_surname,
                "organization": org,
                "paperId": id,
                "occupation": "unknown"
            })

            orgs.append({
                "name": org,
                "country": "unknown",
            })

            id += 1

        else:
            print("Only .xml files are supported:", archivo)

    return [papers, authors, orgs]

def get_ror_organization(name):
    search_url = "https://api.ror.org/organizations"
    params = {"query": name}
    response = requests.get(search_url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data['number_of_results'] > 0:
            return data['items'][0]
        else:
            print(f"No se encontró la organización: {name}")
            return None
    else:
        print(f"Error en la solicitud: {response.status_code}")
        return None

def search_wikidata_author(name):
    search_url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "format": "json",
        "language": "en",
        "search": name,
        "type": "item"
    }

    response = requests.get(search_url, params=params)

    if response.status_code == 200:
        try:
            data = response.json()
            if 'search' in data and data['search']:
                for result in data['search']:
                    if result['label'].lower() == name.lower():
                        return result['id']
                return data['search'][0]['id']
            else:
                print(f"No se encontró el autor: {name}")
                return None
        except json.JSONDecodeError as e:
            print(f"Error al decodificar la respuesta JSON: {e}")
            return None
    else:
        print(f"Error en la solicitud: {response.status_code}")
        return None

def get_wikidata_occupations(entity_id):
    sparql_query = f"""
    SELECT ?occupationLabel WHERE {{
      wd:{entity_id} wdt:P106 ?occupation.
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
    }}
    """
    sparql_endpoint = "https://query.wikidata.org/sparql"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(sparql_endpoint, params={"query": sparql_query, "format": "json"}, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            occupations = [item['occupationLabel']['value'] for item in data['results']['bindings']]
            return occupations
        except json.JSONDecodeError as e:
            print(f"Error al decodificar la respuesta JSON: {e}")
            return None
    else:
        print(f"Error en la solicitud SPARQL: {response.status_code}")
        return None

def enrich_entities(orgs, authors):
    for org in orgs:
        org_name = org["name"]
        ror_org = get_ror_organization(org_name)
        if ror_org:
            org["country"] = ror_org["country"]["country_name"]

    for author in authors:
        author_name = author["name"] + " " + author["surname"]
        entity_id = search_wikidata_author(author_name)
        if entity_id:
            occupations = get_wikidata_occupations(entity_id)
            if occupations:
                author["occupation"] = occupations
            else:
                print(f"No se encontró la ocupación para el autor: {author_name}")
        else:
            print(f"No se encontró entidad en Wikidata para el autor: {author_name}")

    return [orgs, authors]

def instance_rdf_xmls(directory, papers, authors, organizations):
    if not os.path.exists(directory):
        os.makedirs(directory)

    for i, paper in enumerate(papers):
        g = Graph()
        ex = Namespace("http://prueba.org/")
        
        # Definir el URI del papel con el ID
        paper_uri = URIRef(f"http://prueba.org/paper_{i}")

        # Añadir el ID del papel como propiedad en el grafo RDF
        g.add((paper_uri, ex.paperID, Literal(paper["id"])))

        # Añadir otros detalles del papel
        g.add((paper_uri, RDF.type, ex.Paper))
        g.add((paper_uri, DC.title, Literal(paper["title"])))
        g.add((paper_uri, DC.language, Literal(paper["language"])))
        g.add((paper_uri, DC.date, Literal(paper["date"])))

        org_uri = URIRef(f"http://prueba.org/organization_{i}")
        g.add((org_uri, RDF.type, FOAF.Organization))
        g.add((org_uri, FOAF.name, Literal(paper["organization"])))

        org_name = paper["organization"]
        for org in organizations:
            if org["name"] == org_name:
                country = org["country"]
                if country != "unknown":
                    g.add((org_uri, ex.country, Literal(country)))
                break

        g.add((paper_uri, DC.publisher, org_uri))

        for author in authors:
            if author["paperId"] == paper["id"]:
                author_uri = URIRef(f"http://prueba.org/author_{author['paperId']}")
                g.add((author_uri, RDF.type, FOAF.Person))
                g.add((author_uri, FOAF.givenName, Literal(author["name"])))
                g.add((author_uri, FOAF.familyName, Literal(author["surname"])))
                g.add((author_uri, FOAF.member, Literal(author["organization"])))
                if author["occupation"] != "unknown":
                    for occupation in author["occupation"]:
                        g.add((author_uri, ex.occupation, Literal(occupation)))
                g.add((paper_uri, DC.creator, author_uri))
        
        for sim in paper["Similaritys"]:
            similarity_uri = URIRef(f"http://prueba.org/similarity_{i}_{sim[0]}")
            target_paper_uri = URIRef(f"http://prueba.org/paper_{sim[0]}")
            g.add((similarity_uri, RDF.type, ex.Similarity))
            g.add((similarity_uri, ex.sourcePaper, paper_uri))
            g.add((similarity_uri, ex.targetPaper, target_paper_uri))
            g.add((similarity_uri, ex.similarityValue, Literal(sim[1])))

        paper_filename = f"paper_{i}.rdf"
        paper_filepath = os.path.join(directory, paper_filename)
        g.serialize(destination=paper_filepath, format='xml')




def instance_topics(directory,papers):
    with(open(directory)) as f:
        data = json.load(f)
    
    for paper, document in zip(papers, data):
        topic = document.get("topic", -1)
        paper["Topic"] = topic
        
def instance_similaritys(directory, papers):
    with open(directory, 'r') as f:
        data = json.load(f)
    
    for i, document in enumerate(data):
        similarities = document.get("similarities", {})
        similarity_list = []

        for paper_id, similarity_rate in enumerate(similarities.values(), start=1):
            similarity_percent = similarity_rate * 100
            similarity_list.append([paper_id, similarity_percent])

        # Actualiza el campo "Similaritys" en el documento correspondiente en la lista papers
        papers[i]["Similaritys"] = similarity_list

    return papers







current_path = os.getcwd()
xml_directory = os.path.join(current_path, "ValidationCorpus")

papers, authors, orgs = instance_entities(xml_directory)

orgs, authors = enrich_entities(orgs, authors)

rdf_directory = os.path.join(current_path, "rdfxmls")


similarityjson_directory = os.path.join(current_path,"Abstract_And_topics.json")

instance_topics(similarityjson_directory,papers)
papers = instance_similaritys(similarityjson_directory,papers)

instance_rdf_xmls(rdf_directory, papers, authors, orgs)

for paper in papers:
    
    print(f"Archivo: {paper['document']},Title: {paper['title']}, Author: {paper['author']}, Organization: {paper['organization']}, Language: {paper['language']}, Date : {paper['date']}, Id : {paper['id']} , Topic: {paper['Topic']}, Similaritys: {paper['Similaritys']}")