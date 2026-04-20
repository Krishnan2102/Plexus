import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_neo4j import Neo4jGraph

load_dotenv()

def verify_stack():
    print("--- Plexus System Check ---")
    
    
    try:
        graph = Neo4jGraph()
        print("Neo4j Connection: SUCCESS")
    except Exception as e:
        print(f"Neo4j Connection: FAILED ({e})")

    
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
        response = llm.invoke("Say 'Plexus Online'")
        print(f"Gemini API: SUCCESS ({response.content})")
    except Exception as e:
        print(f"Gemini API: FAILED ({e})")

if __name__ == "__main__":
    verify_stack()
