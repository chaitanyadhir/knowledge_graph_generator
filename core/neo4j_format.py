import csv
import os

def export_triples_to_neo4j_format(triples, output_dir="output"):
    """
    Writes two CSV files in Neo4j format: one for nodes, one for relationships.
    """
    os.makedirs(output_dir, exist_ok=True)

    node_set = set()
    edges = []

    # Collect unique nodes and relationships
    for subj, pred, obj in triples:
        subj, pred, obj = subj.strip(), pred.strip(), obj.strip()
        if not subj or not obj or not pred:
            continue
        node_set.add((subj, "Entity"))
        node_set.add((obj, "Entity"))
        edges.append((subj, obj, pred))

    # Write nodes.csv
    with open(os.path.join(output_dir, "nodes.csv"), "w", newline="", encoding="utf-8") as f_nodes:
        writer = csv.writer(f_nodes)
        writer.writerow(["id", "label"])
        for node_id, label in sorted(node_set):
            writer.writerow([node_id, label])

    # Write relationships.csv
    with open(os.path.join(output_dir, "relationships.csv"), "w", newline="", encoding="utf-8") as f_rels:
        writer = csv.writer(f_rels)
        writer.writerow(["start_id", "end_id", "relation"])
        for start_id, end_id, relation in edges:
            writer.writerow([start_id, end_id, relation])

    print(f"Exported to: {output_dir}/nodes.csv and relationships.csv")
