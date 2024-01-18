from rdflib import Graph, Namespace, RDF

# Load the TTL file into an RDF graph
g = Graph()
g.parse(r"C:\Users\Harish Pavan Rolla\class\web\sportsdata.ttl", format="turtle")

# Define the SPARQL namespace and prefixes
ns = Namespace("http://sportsOntology.org/resource/")
ont = Namespace("http://sportsOntology.org/ontology/")

# Predefined SPARQL queries
queries = {
    "Query 1": """
        SELECT ?player ?label WHERE {
            ?player rdf:type :Player ;
                    rdfs:label ?label .
        }
    """,
    "Query 2": """
        SELECT ?event ?label WHERE {
            ?event rdf:type :Event ;
                   rdfs:label ?label .
        }
    """
    # Add more predefined queries as needed
}

def run_sparql_query(query):
    # Execute the SPARQL query on the RDF graph
    results = g.query(query)

    # Print the query results
    for row in results.bindings:
        for var_name in row:
            var_value = row[var_name]
            print(f"{var_name}: {var_value}")
        print()

# Run a specific predefined query
query_name = "Query 1"
query = queries.get(query_name)
if query:
    run_sparql_query(query)
