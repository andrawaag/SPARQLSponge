import os
import re
from SPARQLWrapper import SPARQLWrapper, JSON

# Extract the issue body (assuming it's structured as per the template)
issue_body = os.getenv('GITHUB_ISSUE_BODY', '')

# Extract the SPARQL query from the issue body
sparql_query_match = re.search(r'### SPARQL query\n\s*(.*)\n###', issue_body, re.DOTALL)
if sparql_query_match:
    sparql_query = sparql_query_match.group(1).strip()
    print(sparql_query)
else:
    sparql_query = ''
    print("boe")

# If no SPARQL query was found, exit with failure
if not sparql_query:
    print("No SPARQL query found in the issue.")
    exit(1)

# Define the SPARQL endpoint (you can extract this from the issue body as well)
sparql_endpoint = "https://query.wikidata.org/sparql"  # Example endpoint

# Function to validate SPARQL query
def validate_sparql_query(query, endpoint_url):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        sparql.query().convert()  # This performs the query to check for syntax errors
        return True, "SPARQL query is valid."
    except Exception as e:
        return False, str(e)

# Validate the SPARQL query
valid_query, validation_message = validate_sparql_query(sparql_query, sparql_endpoint)

if not valid_query:
    print(f"SPARQL query is invalid: {validation_message}")
    exit(1)
else:
    print(f"SPARQL query is valid.")
    exit(0)
