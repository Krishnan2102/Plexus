from langchain_neo4j import Neo4jGraph, GraphCypherQAChain
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()

graph = Neo4jGraph()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)


CYPHER_GENERATION_TEMPLATE = """
Task: Generate a Cypher statement to query a graph database.
Instructions:
Use only the provided relationship types and properties in the schema.
IMPORTANT: The name of an entity is stored in the 'id' property. 
If you need to look up a person, place, or organization, use n.id.
The 'text' property contains the original document snippet.

Schema:
{schema}

Question: {question}
Cypher Query:"""

CYPHER_PROMPT = PromptTemplate(
    input_variables=["schema", "question"], 
    template=CYPHER_GENERATION_TEMPLATE
)


chain = GraphCypherQAChain.from_llm(
    llm=llm, 
    graph=graph, 
    verbose=True, 
    allow_dangerous_requests=True,
    cypher_prompt=CYPHER_PROMPT
)

def ask_plexus(question: str):
    try:
        response = chain.invoke({"query": question})
        return response["result"]
    except Exception as e:
        return f"Error: {str(e)}"
