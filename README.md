# VectorShift Frontend Technical Assessment

## Assignment Overview

This repository contains the solution to the **VectorShift Frontend Technical Assessment**. The project consists of a frontend built using **React** and a backend implemented with **FastAPI**. 

The goal of this project is to create a flexible and reusable node abstraction, enhance styling, improve text node logic, and integrate the frontend with the backend. **Additionally, this project implements real-time AI execution using the Google Gemini API.**

## Project Structure

### How to Run

1. **Frontend**:
   - Navigate to the `/frontend` folder.
   - Run the following commands:
     ```bash
     npm install
     npm start
     ```
   - The frontend will start on `http://localhost:3000`.

2. **Backend**:
   - Navigate to the `/backend` folder.
   - Install the required Python libraries (FastAPI, Uvicorn, NetworkX, Google Generative AI):
     ```bash
     pip install fastapi uvicorn networkx google-generativeai
     ```
   - Run the server:
     ```bash
     uvicorn main:app --reload
     ```
   - The backend will start on `http://localhost:8000`.

## Part 1: Node Abstraction

A reusable and flexible node abstraction was created to simplify building new nodes. This abstraction allows you to easily add new nodes by defining the following:

- **Input Handles** and **Output Handles**
- Customizable fields (e.g., text inputs, dropdowns)
- Shared UI components across different node types

### New Nodes Created:
- Checkbox Node
- Color Picker Node
- Input Node
- String Concatenate Node
- Multiplier Node

## Part 2: Styling

Styling was applied using **TailwindCSS** and **NextUI** to create a modern and clean interface. The design prioritizes usability, with proper visual cues for node connections and interactive components.

### Features:
- Drag-and-drop pipeline builder
- Interactive components with smooth transitions and hover effects

## Part 3: Text Node Logic

The **Text Node** was improved with the following functionality:

1. **Dynamic Resizing**: The node adjusts its width and height based on the text input to improve visibility.
2. **Variable Detection**: Users can define variables inside double curly braces (`{{ variable }}`). The node automatically generates input handles for these variables, allowing them to interact with other nodes.

## Part 4: Backend Integration & AI Execution

The frontend is integrated with the **FastAPI** backend to perform two critical functions upon submission:

### 1. Structure Validation (DAG Check)
The backend uses **NetworkX** to analyze the graph structure:
- Calculates the number of nodes and edges.
- Checks if the pipeline forms a **Directed Acyclic Graph (DAG)** to prevent infinite loops.

### 2. AI Pipeline Execution (Bonus Feature)
If the graph is valid, the backend executes the pipeline logic using the **Google Gemini LLM (gemini-1.5-flash)**. It extracts text from input nodes, sends it to the AI, and returns the generated response to the frontend.

### Backend Endpoints:

#### 1. Parse Pipeline (Validation)
```http
POST /pipelines/parse
Response:

JSON

{
    "num_nodes": 4,
    "num_edges": 3,
    "is_dag": true
}
2. Execute Pipeline (AI Run)
HTTP

POST /pipelines/execute
Response:

JSON

{
    "result": "The capital of France is Paris."
}
Technologies Used
Frontend:
React

React Flow

NextUI

TailwindCSS

Zustand (state management)

React Toastify (for notifications)

Backend:
FastAPI

NetworkX (for DAG validation)

Google Generative AI (Gemini 1.5 Flash for LLM processing)

Future Improvements
Add more customizable node types.

Improve validation of user inputs in nodes.

Enhance error handling for pipeline submission.

Store API keys securely using .env variables in a production environment.