# W10D4 - Human-in-the-Loop with LangGraph

## Overview
This project implements a three-node LangGraph workflow with classification,
conditional routing, and human-in-the-loop approval.

## Graph Architecture

1. classify: Classifies input into greeting, calculation, coding, question, or unsafe.
2. route: Pauses the graph using LangGraph interrupt() and waits for human approval.
3. respond: Generates a response only when the request is approved and safe.

## Conditional Routing
- Unsafe request: Ends without generating a response.
- Approved safe request: Moves to the respond node.
- Rejected or invalid decision: Ends without generating a response.

## Technologies
- Python
- LangGraph
- Pytest
- LangGraph InMemorySaver checkpointer

## Setup