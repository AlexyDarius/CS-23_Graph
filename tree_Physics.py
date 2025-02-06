import json
import networkx as nx
from pyvis.network import Network

def load_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_graph(data):
    G = nx.DiGraph()
    
    for subpart, sections in data.items():
        G.add_node(subpart, label=subpart, title=subpart, shape='box', color='blue')
        
        for section in sections:
            cs_number = section["CS Number"]
            cs_name = section["CS Name"]
            cs_id = f"CS-{cs_number}"
            G.add_node(cs_id, label=cs_number, title=cs_name, shape='ellipse', color='green')
            G.add_edge(subpart, cs_id)
            
            if "CS Requirements" in section:
                for req in section["CS Requirements"]:
                    req_id = req["Requirement ID"]
                    content = req["Content"]
                    G.add_node(req_id, label=req_id, title=content, shape='dot', color='purple')
                    G.add_edge(cs_id, req_id)
                    
            if "AMCs" in section:
                for amc in section["AMCs"]:
                    amc_number = amc["AMC Number"]
                    amc_name = amc["AMC Name"]
                    amc_id = f"AMC-{amc_number}"
                    G.add_node(amc_id, label=amc_number, title=amc_name, shape='diamond', color='red')
                    G.add_edge(cs_id, amc_id)
                    
                    if "Requirements" in amc:
                        for amc_req in amc["Requirements"]:
                            amc_req_id = amc_req["Requirement ID"]
                            amc_req_content = amc_req["Content"]
                            G.add_node(amc_req_id, label=amc_req_id, title=amc_req_content, shape='triangle', color='orange')
                            G.add_edge(amc_id, amc_req_id)
    
    return G

def visualize_graph(G, output_file="Amd6/method2/cs_amc_tree.html"):
    net = Network(notebook=True, directed=True)

    # Convert NetworkX graph to Pyvis
    net.from_nx(G)

    net.show(output_file)

if __name__ == "__main__":
    json_file_path = "Amd6/method2/content/outputs/CS23_AMD4.json"  # Update with actual path
    data = load_json(json_file_path)
    G = build_graph(data)
    visualize_graph(G)
