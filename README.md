# Week 10 – AI/ML Internship Tasks

## Overview

This repository contains the hands-on projects completed during **Week 10 of the AI/ML Internship**. The tasks focus on building stateful AI agents and workflows using LangGraph, implementing human-in-the-loop systems, persistent conversation memory, and an integrated customer support agent.

The projects demonstrate practical applications of Python, LangGraph, CrewAI, SQLite, MLflow, and Ragas.

## Learning Objectives

- Understand stateful agent workflows using LangGraph.
- Build state machines with conditional edges.
- Implement persistent conversation memory.
- Create human-in-the-loop approval workflows.
- Develop a stateful customer support agent.
- Understand multi-agent collaboration using CrewAI.
- Track experiments and evaluate AI application outputs.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| LangGraph | Stateful agent workflows and graph execution |
| CrewAI | Multi-agent collaboration |
| SQLite | Persistent conversation storage |
| MLflow | Experiment tracking and monitoring |
| Ragas | AI evaluation framework |
| Pytest | Testing |
| Git & GitHub | Version control |
| VS Code | Development environment |

## Project Structure

```text
Cynaris_Internship_Week10_Tasks/
│
├── W10D1_LangGraph_Stateful_Agent_Graphs/
│   ├── src/
│   ├── tests/
│   ├── output/
│   ├── main.py
│   └── requirements.txt
│
├── W10D2_LangGraph_State_Machine/
│   ├── src/
│   ├── tests/
│   ├── output/
│   ├── main.py
│   └── requirements.txt
│
├── W10D3_LangGraph_Persistent_Memory/
│   ├── src/
│   ├── tests/
│   ├── output/
│   ├── main.py
│   └── requirements.txt
│
├── W10D4_LangGraph_Human_in_the_Loop/
│   ├── src/
│   ├── tests/
│   ├── output/
│   ├── main.py
│   └── requirements.txt
│
├── W10D5_Stateful_Customer_Support_Agent/
│   ├── src/
│   ├── tests/
│   ├── output/
│   ├── main.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

## Daily Tasks

### Day 1 – LangGraph: Stateful Agent Graphs

**Folder:** `W10D1_LangGraph_Stateful_Agent_Graphs`

**Objective:** Understand how stateful agent graphs work using LangGraph.

**Implementation:**
- Created a state structure to maintain information.
- Implemented classification, routing, and response nodes.
- Connected nodes to form an agent workflow.
- Implemented conditional routing.
- Tested different user inputs.

**Key Learning:** Understanding how state moves between nodes in a LangGraph workflow.

### Day 2 – LangGraph: State Machines & Conditional Edges

**Folder:** `W10D2_LangGraph_State_Machine`

**Objective:** Build a state machine using LangGraph conditional edges.

**Implementation:**
- Created a structured agent state.
- Implemented input classification.
- Added conditional edges to control workflow execution.
- Routed requests based on their categories.
- Tested different execution paths.

**Key Learning:** Understanding state transitions and conditional execution in AI workflows.

### Day 3 – LangGraph: Persistent Conversations

**Folder:** `W10D3_LangGraph_Persistent_Memory`

**Objective:** Implement persistent conversation memory.

**Implementation:**
- Created a conversation state.
- Used SQLite for storing conversation checkpoints.
- Implemented thread-based conversation management.
- Retrieved previous conversation history.
- Tested conversation persistence across application restarts.

**Key Learning:** Understanding how AI agents can retain conversation context across sessions.

### Day 4 – Human-in-the-Loop with LangGraph

**Folder:** `W10D4_LangGraph_Human_in_the_Loop`

**Objective:** Implement human approval in an AI agent workflow.

**Implementation:**
- Created classification, routing, and response nodes.
- Implemented workflow interruption using LangGraph.
- Added human approval and rejection decisions.
- Resumed graph execution based on human decisions.
- Created tests for approval, rejection, and routing.

**Key Learning:** Understanding how human feedback can control AI agent execution.

### Day 5 – Stateful Customer Support Agent

**Folder:** `W10D5_Stateful_Customer_Support_Agent`

**Objective:** Build a stateful customer support agent by combining multiple AI/ML technologies.

**Implementation:**
- Designed customer support agents using CrewAI.
- Used LangGraph to manage the support workflow.
- Implemented issue classification and knowledge retrieval.
- Added SQLite-based conversation memory.
- Integrated MLflow for experiment tracking.
- Prepared an evaluation workflow using Ragas-compatible data structures.
- Created automated tests.

**Key Learning:** Understanding how multiple AI technologies can work together to build a customer support automation system.

## Installation and Execution

Each daily project has its own folder and `requirements.txt` file.

### 1. Clone the repository

```bash
git clone https://github.com/KotapatiDhananjay/cynaris_internship_week10_tasks.git
cd cynaris_internship_week10_tasks
```

### 2. Navigate to a daily project

Example:

```bash
cd W10D1_LangGraph_Stateful_Agent_Graphs
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Run the project

```bash
python main.py
```

### 7. Run tests

```bash
python -m pytest tests -v
```

Repeat these steps for the required daily project folder.

## Testing

Pytest is used to test project functionality, including:

- State classification.
- Conditional routing.
- Agent responses.
- Human approval and rejection.
- Conversation memory.
- Customer support functionality.

Test results are stored in the respective project output folders when generated.

## Experiment Tracking and Evaluation

The Day 5 project includes:

- **MLflow:** Used to track application runs and evaluation results.
- **Ragas:** Used to prepare evaluation datasets and support AI response evaluation.
- **SQLite:** Used for persistent customer conversation storage.

The Day 5 evaluation workflow also includes a custom policy-overlap score; it should not be interpreted as a built-in Ragas evaluation metric.

## Key Outcomes

Through these projects, I gained practical experience in:

1. Building stateful AI agent workflows.
2. Designing graph-based state machines.
3. Implementing conditional routing.
4. Managing persistent conversation history.
5. Integrating human feedback into AI workflows.
6. Building multi-agent applications using CrewAI.
7. Tracking experiments using MLflow.
8. Testing and evaluating AI applications.

## API Key Requirements

The projects are designed to demonstrate local and offline workflows without requiring paid API keys or cloud LLM services.

## Author

**Kotapati Dhananjay**

B.Tech – Information Technology

GitHub: [KotapatiDhananjay](https://github.com/KotapatiDhananjay)

LinkedIn: [Kotapati Dhananjay](https://linkedin.com/in/kotapati-dhananjay-46ab283a7/)

---

*Week 10 – AI/ML Internship Projects*
