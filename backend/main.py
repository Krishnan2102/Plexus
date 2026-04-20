from fastapi import FastAPI
from langchain_neo4j import Neo4jGraph
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
from retriever import ask_plexus

load_dotenv()

app = FastAPI()
graph = Neo4jGraph()

# Allow your React frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/graph")
def get_graph_data():
    # This Cypher query fetches everything in a format React understands
    query = """
    MATCH (n)-[r]->(m)
    RETURN 
        {id: id(n), label: labels(n)[0], name: n.id} as source,
        {id: id(m), label: labels(m)[0], name: m.id} as target,
        type(r) as relationship
    LIMIT 100
    """
    results = graph.query(query)
    return {"data": results}

class ChatRequest(BaseModel):
    message: str

# Add this endpoint
@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    response = ask_plexus(request.message)
    return {"answer": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)