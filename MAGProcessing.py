# import statements
import pprint
from rdflib import ConjunctiveGraph, Namespace, URIRef
import time
import json

# import open alex concept tagger
import multiprocessing as mp
import mag_functions as F

# create a new ConjunctiveGraph object and populate it with graph content
FoS = ConjunctiveGraph()
FoS.parse("FoS.nt", format="nt")
print("FoS populated.")

papers = ConjunctiveGraph()
papers.parse("Papers.nt", format="turtle")
print("Papers populated.")

papersAbs = ConjunctiveGraph()
papersAbs.parse("PaperAbstracts.nt", format="turtle")
print("PaperAbs populated.")

papersFoS = ConjunctiveGraph()
papersFoS.parse("PaperFoS.nt", format="turtle")
print("PapersFoS populated.")

journals = ConjunctiveGraph()
journals.parse("Journals.nt", format="turtle")
print("Journals populated.")

# Get the unique paper URIs with the prefix 'http://mag.graph/entity/' (up to 10,000)
paper_uris = set()
count = 0

for s in papers.subjects(predicate=None, object=None):
    if str(s).startswith('http://mag.graph/entity/'):
        paper_uris.add(str(s))
        count += 1
        if count >= 10000:
            break
print("10000 papers found.")

# Define the desired paper predicates
predicates = [
    URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),  # Paper type
    URIRef('http://purl.org/dc/terms/title'),  # Paper title
    URIRef('http://mag.graph/property/appearsInJournal'),  # Journal appearance
]

# Create a dictionary to store all paper information
papers_result = {}
count = 0

for paper in paper_uris:
    if count % 100 == 0:
        print(f"{count} papers finished querying.")

    count += 1

    # Create a dictionary to store each result
    values = {}
    
    for predicate in predicates:
        try:
            result = list(papers.objects(subject=URIRef(paper), predicate=predicate))
            if result:
                # If in journal, query for journal name
                if predicate == URIRef('http://mag.graph/property/appearsInJournal'):
                    try:
                        result = [list(journals.objects(subject=URIRef(paper), predicate=URIRef('http://xmlns.com/foaf/0.1/name')))[0]]
                    except:
                        print(f"failed to query for journal {result}")
                values[str(predicate)] = str(result[0])
        except:
            print(f"{predicate} query failed for {paper}")
     
    papers_result[paper] = values
    
    # Query for abstract of paper
    try:
        abstract = list(papersAbs.objects(subject=URIRef(paper)))
        if abstract:
            papers_result[paper]['abstract'] = str(abstract[0])
    except Exception:
        print(f"abstract query failed for {paper}")
        
    # Query for disciplines
    try:
        disciplines_results = list(papersFoS.objects(subject=URIRef(paper), predicate=URIRef('http://purl.org/spar/fabio/hasDiscipline')))
        disciplines = {}
        for discipline in disciplines_results:
            try:
                disciplines.add(list(FoS.objects(subject=discipline, predicate=URIRef('http://xmlns.com/foaf/0.1/name')))[0])
            except:
                print(f"failed to query {discipline}")
                
        if disciplines:
            papers_result[paper]['concept_tags'] = disciplines
    except:
        print(f"discipline query failed for {paper}")

# Given each paper and respective information, fetch proper concept tags
count = 0

for paper in papers_result:
    if count % 100 == 0:
        print(f"{count} papers finished querying.")

    count += 1
    information = {
        "title": papers_result[paper].get('http://purl.org/dc/terms/title'),
        "doc_type": papers_result[paper].get('http://www.w3.org/1999/02/22-rdf-syntax-ns#type'),
        "journal": papers_result[paper].get('http://mag.graph/property/appearsInJournal'),
        "abstract": papers_result[paper].get('abstract'),
        "inverted_abstract": False
    }

    try:
        start_time = time.time()
        results = F.get_tags([information], 1)[1][0]
        results['time'] = time.time() - start_time
    except:
        print(f"{paper}: tag failed")
        results = {"tags": None, "scores": None, "tag_ids": None}

    papers_result[paper]['results'] = results

# Open the file in write mode and dump the dictionary with indents
with open("MAG_results.json", "w") as json_file:
    json.dump(papers_result, json_file, indent=4)

print(f"Data successfully dumped into MAG_results.json.")
