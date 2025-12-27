# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import networkx as nx
import google.generativeai as genai 
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# --- 1. CONFIGURATION ---
# TODO: Paste your Google Gemini API Key here inside the quotes
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure the AI
genai.configure(api_key=GOOGLE_API_KEY)

# --- 2. MIDDLEWARE ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- 3. DATA MODELS ---
class PipelineNode(BaseModel):
    id: str
    type: str
    data: Dict[str, Any]

class PipelineEdge(BaseModel):
    id: str
    source: str
    target: str

class Pipeline(BaseModel):
    nodes: List[PipelineNode]
    edges: List[PipelineEdge]

# --- 4. ENDPOINT A: THE DAG CHECKER (Required) ---
@app.post("/pipelines/parse")
async def parse_pipeline(pipeline: Pipeline):
    num_nodes = len(pipeline.nodes)
    num_edges = len(pipeline.edges)

    G = nx.DiGraph()
    for node in pipeline.nodes:
        G.add_node(node.id)
    for edge in pipeline.edges:
        G.add_edge(edge.source, edge.target)

    is_dag = nx.is_directed_acyclic_graph(G)

    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "is_dag": is_dag,
    }

# --- 5. ENDPOINT B: THE AI RUNNER (The Fix) ---
@app.post("/pipelines/execute")
async def execute_pipeline(pipeline: Pipeline):
    try:
        # 1. Find the input text
        input_text = "Explain quantum physics like I'm 5" # Default backup
        for node in pipeline.nodes:
            # Check various places where text might be stored
            if 'text' in node.data and node.data['text']: 
                input_text = node.data['text']
                break
            if 'inputName' in node.data and node.data['inputName']:
                input_text = node.data['inputName']
                break
            if 'label' in node.data and node.data['label']:
                input_text = node.data['label']
                break

        # 2. Call Google Gemini
        # We use 'gemini-1.5-flash' as it is the current standard.
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(input_text)
            return {"result": response.text}
        except Exception as e_flash:
            # If flash fails, try the older 'gemini-pro'
            print(f"Flash model failed: {e_flash}. Trying gemini-pro...")
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(input_text)
            return {"result": response.text}

    except Exception as e:
        # If everything fails, return the error message so the popup shows it
        return {"error": str(e)}