import os
import hashlib
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import XSD

# Function to generate MD5 hash from a string (SPARQL query in this case)
def generate_md5_hash(input_string):
    return hashlib.md5(input_string.encode()).hexdigest()

# Retrieve the issue body from the environment variable
issue_body = os.getenv('GITHUB_ISSUE_BODY', '')

# Parse the issue form fields directly from the issue body
lines = issue_body.splitlines()

data = {}
current_field = None

for line in lines:
    # Identify new field titles (assuming '### Field Name')
    if line.startswith('### '):
        current_field = line.strip('### ').strip()
        data[current_field] = ''
    elif current_field:
        # Append values to the current field
        data[current_field] += line.strip()

# Extract the SPARQL query to generate the MD5 hash (assuming the key for the query is "SPARQL query")
sparql_query = data.get("SPARQL query", "")

# If no SPARQL query is found, we can't generate RDF
if not sparql_query:
    print("No SPARQL query found. Exiting.")
    exit(1)

# Generate MD5 hash of the SPARQL query
hash_subject = generate_md5_hash(sparql_query)

# Initialize RDF graph
g = Graph()

# Define a custom namespace for the issue fields
namespace = Namespace("http://example.org/issue/")

# Define a subject using the MD5 hash of the SPARQL query
issue_subject = URIRef(f"http://example.org/issues/{hash_subject}")

# Iterate through the form data and convert to RDF
for field, value in data.items():
    predicate = URIRef(namespace + field.replace(" ", "_"))  # Convert field name to a URI predicate
    object_literal = Literal(value, datatype=XSD.string)     # Convert value to xsd:string literal
    g.add((issue_subject, predicate, object_literal))

# Serialize the RDF graph to Turtle format (or other formats like XML, JSON-LD, etc.)
rdf_output_file = 'issue_output.ttl'
with open(rdf_output_file, 'wb') as rdf_file:
    rdf_file.write(g.serialize(format='turtle'))

print(f"RDF data saved to {rdf_output_file}")
