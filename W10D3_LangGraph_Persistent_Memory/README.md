# W10D3 - LangGraph + Memory: Persistent Conversations

## Overview

This project implements a three-node conversational agent using LangGraph with persistent conversation memory.

It uses SQLite checkpointing to save conversation state and retrieve previous messages using a conversation thread ID.

## Architecture

START -> CLASSIFY -> ROUTE -> CONDITIONAL EDGE

- Approved and safe input -> RESPOND -> END
- Rejected input -> END
- Unsafe input -> END

The graph contains three application nodes:

1. Classify
2. Route
3. Respond

## Main Features

- Input classification
- Conditional routing
- Human-in-the-loop interruption
- Pause and resume execution
- Persistent conversation memory
- SQLite checkpoint storage
- Conversation history retrieval
- Automated testing

## Technologies

- Python
- LangGraph
- SQLite
- langgraph-checkpoint-sqlite
- pytest

## Project Structure

```text
W10D3_LangGraph_Persistent_Memory/
|
|-- src/
|   |-- __init__.py
|   |-- memory_graph.py
|
|-- tests/
|   |-- __init__.py
|   |-- test_memory.py
|
|-- data/
|-- output/
|-- main.py
|-- requirements.txt
|-- README.md
|-- SELF_REVIEW.md
|-- .gitignore
```

## Installation

Create and activate a virtual environment:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run the Application

```powershell
python main.py
```

Choose one of the options:

1. Start a new conversation.
2. Continue an existing conversation.
3. Exit.

Use the same conversation ID to retrieve previously saved messages.

## Human-in-the-Loop

LangGraph's interrupt() function pauses graph execution.

The human decision is supplied using:

```python
Command(resume="approve")
```

A rejected request stops the workflow.

Unsafe input is not allowed to reach the response node, even if approved.

## Persistent Memory

The project uses SQLite checkpointing through SqliteSaver.

Conversation state is associated with a thread ID.

The same thread ID can be used after restarting the application to retrieve the saved conversation.

Database location:

```text
data/conversations.db
```

## Run Tests

```powershell
pytest tests -v
```

Tests cover:

- Five input classifications
- Human approval
- Human rejection
- Conversation history storage
- Database reconnection and memory restoration
- Unsafe request routing

## Learning Outcomes

- Stateful graph construction
- Conditional edges
- Human-in-the-loop workflows
- Persistent conversation memory
- SQLite checkpointing
- Thread-based conversation management
- Automated testing

## Author

Kotapati Dhananjay

B.Tech Information Technology  
Garden City University

GitHub: https://github.com/KotapatiDhananjay

## Internship

AI/ML 3M Internship Program  
Week 10 - Day 3
'@ | Set-Content README.md -Encoding UTF8

@'
# W10D3 Self-Review Checklist

- [ ] Created three LangGraph application nodes.
- [ ] Implemented input classification.
- [ ] Implemented conditional routing.
- [ ] Tested five input categories.
- [ ] Implemented human-in-the-loop interruption.
- [ ] Tested pause and resume.
- [ ] Implemented SQLite persistent checkpointing.
- [ ] Stored conversation history.
- [ ] Retrieved conversation history using the same thread ID.
- [ ] Verified memory after database reconnection.
- [ ] Tested human rejection.
- [ ] Tested unsafe request routing.
- [ ] Ran all pytest tests successfully.
- [ ] Saved test output evidence.
- [ ] Completed two CIA Full Stack Mentor Mode interactions.
- [ ] Reviewed the code before committing.
- [ ] Created at least two descriptive Git commits.
- [ ] Pushed the feature branch.
- [ ] Created a Pull Request.
'@ | Set-Content SELF_REVIEW.md -Encoding UTF8

@'
venv/
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.env
.vscode/
.idea/
.DS_Store
Thumbs.db