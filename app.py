from core.load_data import extract_text
from core.stanford_openIE import *
from core.neo4j_format import *
import time

start = time.time()
corenlp_path = r"C:\projects\Knowledge_graph\Stan\stanford-corenlp-4.2.0"
input_path="input/wipro.pdf"

text=extract_text(input_path)
text=text[:20000].lower()

triples = extract_triples(text, r"C:\projects\Knowledge_graph\Stan\stanford-corenlp-4.2.0")
print(f"Total triples: {len(triples)}")

export_triples_to_neo4j_format(triples)

end = time.time()
print(f"Duration:   {end - start:.2f} seconds")

