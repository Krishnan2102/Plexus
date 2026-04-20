import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_neo4j import Neo4jGraph
from dotenv import load_dotenv

load_dotenv()


graph = Neo4jGraph()
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)


# Refined schema for better Corporate Intelligence
allowed_nodes = ["Organization", "Person", "Location", "Event", "Asset"]
allowed_rels = [
    "SUBSIDIARY_OF", 
    "PARTNERED_WITH", 
    "ALLOCATED_FUNDS_TO", 
    "OPERATES_IN", 
    "CONFLICTS_WITH",
    "REPRESENTS"
]


transformer = LLMGraphTransformer(
    llm=llm,
    allowed_nodes=allowed_nodes,
    allowed_relationships=allowed_rels,
    
    strict_mode=True 
)

def run_ingestion(file_path):
    print(f"📄 Loading: {file_path}")
    loader = PyPDFLoader(file_path)
    pages = loader.load()

   
    graph_documents = transformer.convert_to_graph_documents(pages[:5]) 
    
    print(f"🔗 Adding {len(graph_documents)} extracted items to Neo4j...")
    graph.add_graph_documents(
        graph_documents, 
        baseEntityLabel=True, 
        include_source=True
    )
    print(" Ingestion Complete!")

if __name__ == "__main__":
   
    target_pdf = "./data/test_report.pdf" 
    if os.path.exists(target_pdf):
        run_ingestion(target_pdf)
    else:
        print("❌ PDF not found. Drop a file in backend/data/test_report.pdf")
