from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS
from rdflib.tools.rdf2dot import rdf2dot
import pydot
import os

# Definición de la carpeta para los grafos (ruta relativa a tu directorio de usuario)

current_path = os.getcwd()
graphs_folder = os.path.join(current_path, "GrafosRDF")
# Crear la carpeta si no existe
if not os.path.exists(graphs_folder):
    os.makedirs(graphs_folder)


# Definición de la ruta del archivo .dot


# Definición del namespace RDF
ex = Namespace("http://prueba.org/")

# Creación del grafo RDF
g = Graph()

# Definición de entidades URI
paper_uri = ex.paper
topic_uri = ex.topic
topic_percentage_uri = ex.topic_percentage
author_uri = ex.author
organization_uri = ex.organization
project_uri = ex.project
country_uri = ex.country
similarity_uri = ex.similarity

# Definición de relaciones
paper_belongs_to_topic_uri = ex.belongs_to_topic
paper_has_topic_percentage_uri = ex.has_topic_percentage
topic_related_to_topic_percentage_uri = ex.related_to_topic_percentage
paper_written_by_author_uri = ex.written_by_author
paper_published_by_organization_uri = ex.published_by_organization
similarity_relates_to_paper_uri1 = ex.similarity_relates_to_paper1
similarity_relates_to_paper_uri2 = ex.similarity_relates_to_paper2
author_belongs_to_organization_uri = ex.belongs_to_organization
author_participates_in_project_uri = ex.participates_in_project
organization_participates_in_project_uri = ex.participates_in_project
organization_located_in_country_uri = ex.located_in_country

# Definición de instancias RDF
g.add((paper_uri, RDF.type, ex.paper))
g.add((topic_uri, RDF.type, ex.topic))
g.add((topic_percentage_uri, RDF.type, ex.topic_percentage))
g.add((author_uri, RDF.type, ex.author))
g.add((organization_uri, RDF.type, ex.organization))
g.add((project_uri, RDF.type, ex.project))
g.add((country_uri, RDF.type, ex.country))
g.add((similarity_uri, RDF.type, ex.similarity))

# Agregar tripletas al grafo RDF para establecer la relación
g.add((paper_uri, paper_belongs_to_topic_uri, topic_uri))
g.add((paper_uri, paper_has_topic_percentage_uri, topic_percentage_uri))
g.add((topic_uri, topic_related_to_topic_percentage_uri, topic_percentage_uri))
g.add((paper_uri, paper_written_by_author_uri, author_uri))
g.add((paper_uri, paper_published_by_organization_uri, organization_uri))
g.add((similarity_uri, similarity_relates_to_paper_uri1, paper_uri))
g.add((similarity_uri, similarity_relates_to_paper_uri2, paper_uri))
g.add((author_uri, author_belongs_to_organization_uri, organization_uri))
g.add((author_uri, author_participates_in_project_uri, project_uri))
g.add((organization_uri, organization_participates_in_project_uri, project_uri))
g.add((organization_uri, organization_located_in_country_uri, country_uri))



# Serializar el grafo en formato XML
rdf_file_path = os.path.join(graphs_folder, "graph.rdf")
g.serialize(destination=rdf_file_path, format='xml')

dot_file_path = os.path.join(graphs_folder, "graph.dot")

# Convertir RDF a DOT y guardarlo
with open(dot_file_path, 'w') as f:
    rdf2dot(g, f)

# Convertir DOT a PNG usando pydot
(graph,) = pydot.graph_from_dot_file(dot_file_path)
png_file_path = os.path.join(graphs_folder, "graph.png")
graph.write_png(png_file_path)
print(f"Guardado: {png_file_path}")
files = os.listdir(graphs_folder)
print("Archivos en la carpeta:", files)