# W10D5 - Stateful Customer Support Agent

## Overview

This project implements a stateful customer support agent using the
approved AI/ML 3M stack.

## Technologies

- CrewAI: Multi-agent customer support review.
- LangGraph: Stateful customer support workflow.
- SQLite: Persistent conversation checkpoints.
- MLflow: Experiment and performance tracking.
- Ragas: Evaluation dataset structure.
- Pytest: Automated testing.
- MLOps: Reproducible workflow, testing, tracking, and evaluation.

## Architecture

### CrewAI Agents

1. Support Triage Analyst
2. Support Resolution Specialist
3. Support Quality Reviewer

### LangGraph Nodes

1. classify - identifies the customer issue.
2. retrieve - retrieves relevant support policy.
3. respond - runs CrewAI and creates the response.

## Supported Categories

- Delivery
- Refund
- Payment
- Account
- Product
- General

## Features

- Local rule-based issue classification.
- Local support knowledge base.
- Multi-agent CrewAI review.
- Persistent customer conversation history.
- SQLite checkpoint storage.
- MLflow experiment tracking.
- Ragas-compatible evaluation dataset.
- Automated pytest tests.
- No paid API keys required.

## Installation