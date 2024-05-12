#Defining namespaces

namespace = ("http://example.org/")

#Defining the entities and their uris
entities = {
    "Paper": [],
    "Author": [],
    "Organization": [],
    "Project": [],
    "Topic": [],
    "Similarity": [],
    "TopicPercentage": []
}
def generate_uri(namespace, entity, id):
    return f"{namespace}{entity}/{id}"

for entity, ids in entities.items():
    for id in ids:
        print(generate_uri(namespace, entity, id))
