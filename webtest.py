from flask import Flask, render_template, request
from rdflib import Graph, Namespace

app = Flask(__name__)

# Load the TTL file into an RDF graph
g = Graph()
g.parse(r"C:\Users\Harish Pavan Rolla\class\web\sportsdata.ttl", format="turtle")

# Define the SPARQL namespace and prefixes
ns = Namespace("http://sportsOntology.org/resource/")

# Predefined SPARQL queries
queries = {
    "Winning Players Count by Country": """
        PREFIX ns: <http://sportsOntology.org/resource/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ont: <http://sportsOntology.org/ontology/>

        SELECT ?country (COUNT(?player) AS ?playerCount)
        WHERE {
            ?country rdf:type ns:Country .
            ?country ns:hasPlayers ?player .
        }
        GROUP BY ?country
        ORDER BY DESC(?playerCount)
    """,
    "Event Count by Sport": """
        PREFIX ns: <http://sportsOntology.org/resource/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ont: <http://sportsOntology.org/ontology/>

        SELECT ?sport (COUNT(?event) AS ?eventCount)
        WHERE {
        ?event rdf:type ns:Event .
        ?event ns:hasSportType ?sport .
        }
        GROUP BY ?sport
    """,
    "Players Who Won Gold Medals": """
        PREFIX ns: <http://sportsOntology.org/resource/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ont: <http://sportsOntology.org/ontology/>

        SELECT ?player
        WHERE {
        ?player rdf:type ns:Player .
        ?player ns:wonMedal ?medal .
        ?medal rdf:type ns:Medal .
        FILTER(CONTAINS(STR(?medal), "Gold"))
        }
    """,
    "Medal Count by Country": """
        PREFIX ns: <http://sportsOntology.org/resource/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX ont: <http://sportsOntology.org/ontology/>

        SELECT ?country (COUNT(?goldMedal) AS ?goldCount) (COUNT(?silverMedal) AS ?silverCount) (COUNT(?bronzeMedal) AS ?bronzeCount)
        WHERE {
        ?country rdf:type ns:Country .
        ?country ns:hasPlayers ?player .
        ?player ns:wonMedal ?medal .
        ?medal rdf:type ns:Medal .
        
        OPTIONAL {
            ?medal ns:medalsGivenToPlayer ?player .
            FILTER(CONTAINS(STR(?medal), "Gold"))
            BIND(?medal AS ?goldMedal)
        }
        
        OPTIONAL {
            ?medal ns:medalsGivenToPlayer ?player .
            FILTER(CONTAINS(STR(?medal), "Silver"))
            BIND(?medal AS ?silverMedal)
        }
        
        OPTIONAL {
            ?medal ns:medalsGivenToPlayer ?player .
            FILTER(CONTAINS(STR(?medal), "Bronze"))
            BIND(?medal AS ?bronzeMedal)
        }
        }
        GROUP BY ?country
    """
    # Add more predefined queries as needed
}

def execute_sparql_query(query):
    # Execute the SPARQL query on the RDF graph
    results = g.query(query)
    result_string = ""

    # Format the query results as a string
    for row in results.bindings:
        for var_name in row:
            var_value = row[var_name]
            result_string += f"{var_name}: {var_value}\n"
        result_string += "\n"

    return result_string

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        query_name = request.form.get("query")
        query = ""

        if query_name == "other":
            query = request.form.get("custom-query")
        else:
            query = queries.get(query_name)

        if query:
            result_string = execute_sparql_query(query)
            return render_template("index.html", queries=queries, result_string=result_string)

    return render_template("index.html", queries=queries)

if __name__ == "__main__":
    app.run(debug=True)
    
    
    
"""
other example "Events by Sport (Concatenated)"
PREFIX ns: <http://sportsOntology.org/resource/>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX ont: <http://sportsOntology.org/ontology/>

SELECT ?sport (GROUP_CONCAT(DISTINCT ?event; SEPARATOR=", ") AS ?events)
WHERE {
  ?sport rdf:type ns:Sport .
  ?sport ns:hasBranch ?branch .
  ?branch ns:hasEvent ?event .
}
GROUP BY ?sport

"""
