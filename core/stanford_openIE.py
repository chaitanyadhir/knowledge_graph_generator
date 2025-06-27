import subprocess
import tempfile
import os
import re



def split_into_sentences(text: str) -> list[str]:
    """
    Cleans and splits raw input into proper sentences, filtering junk lines.
    """
    import re
    sentence_endings = re.compile(r'(?<=[.!?])\s+')
    raw_sentences = sentence_endings.split(text)

    cleaned = []
    for s in raw_sentences:
        line = s.strip()
        if not line:
            continue
        if len(line) < 20:  # Skip too-short lines
            continue
        if re.match(r'^[A-Z\s\-–]+$', line):  # All-caps headers
            continue
        if any(sym in line for sym in ['☐', '☒']):
            continue
        if line.lower() in ['none', 'not applicable', 'n/a']:
            continue
        cleaned.append(line)
    
    return cleaned

def extract_triples(text: str, corenlp_path: str) -> list[tuple[str, str, str]]:
    """
    Accepts raw text, splits it into sentences, returns (subject, predicate, object) triples
    using OpenIE backend from Stanford CoreNLP.
    """
    sentences = split_into_sentences(text)

    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".txt", encoding='utf-8') as input_file:
        for sentence in sentences:
            input_file.write(sentence + '\n')
        input_file_path = input_file.name

    output_file_path = input_file_path + "_triples.txt"
    java_path = r"C:\Java\jdk-11\bin\java.exe"  # Update if different

    cmd = [
        java_path, "-mx4g", "-cp", f"{corenlp_path}/*",
        "edu.stanford.nlp.naturalli.OpenIE",
        input_file_path
    ]
    with open(output_file_path, "w") as outfile:
        subprocess.run(cmd, stdout=outfile, stderr=subprocess.DEVNULL, text=True)

    triples = []
    with open(output_file_path, "r", encoding='utf-8', errors='ignore') as f:
        for line in f:
            parts = line.strip().split("\t")
            if len(parts) == 4:
                _, subj, pred, obj = parts
                triples.append((subj.strip(), pred.strip(), obj.strip()))

    os.remove(input_file_path)
    os.remove(output_file_path)

    return triples
