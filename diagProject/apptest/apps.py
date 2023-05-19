import openai
import json
import re
from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = openai_api_key

def parse_text(text):
    node_dict = {}
    root = None
    nodes = []

    lines = text.split('\n')
    node = None
    for line in lines:
        if "Parent" in line:
            parent_name = line.split(':')[-1].strip()
            if node is not None:
                node["parent"] = parent_name
                if root is None and parent_name == "":
                    root = node
        elif "Name" in line:
            node_name = line.split(':')[-1].strip()
            node = {"name": node_name, "children": []}
            nodes.append(node)
        elif "Description" in line and node is not None:
            description = line.split(':')[-1].strip()
            node["description"] = description
        elif "Children" in line and node is not None:
            children_names = line.split(':')[-1].strip().split(', ')
            for child_name in children_names:
                if child_name:
                    child = {"name": child_name, "children": []}
                    node["children"].append(child)
                    nodes.append(child)

    for node in nodes:
        if "name" in node:
            node_dict[node["name"]] = node
        else:
            print("Error: 'name' key not found in the node:", node)

    return root, node_dict



def build_tree(node, node_dict):
    for child in node["children"]:
        child.update(node_dict[child["name"]])
        build_tree(child, node_dict)

def generate_mind_map_data(theme, schema_type):
    prompt = f'Créez une carte mentale sur le thème "{theme}" en utilisant la structure suivante pour chaque noeud :\n---\nNode:\n- Name: [Nom du noeud]\n- Description: [Description du noeud]\n- Parent: [Nom du noeud parent]\n- Children: [Noms des noeuds enfants, séparés par des virgules]\n---'

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0.5,
    )

    mind_map_data = response.choices[0].text.strip()
    print("Response raw text:", mind_map_data)

    root, node_dict = parse_text(mind_map_data)
    build_tree(root, node_dict)

    print("root:", root)
    print("node dict:", node_dict)

    return root

theme = "Organiser un événement dans une boîte de nuit"
schema_type = "carte mentale"

json_data = generate_mind_map_data(theme, schema_type)

print("Fichier JSON généré :", json_data)  # Ajoutez cette ligne
print("test1")

with open("output.json", "w") as outfile:
    json.dump(json_data, outfile, indent=2)
