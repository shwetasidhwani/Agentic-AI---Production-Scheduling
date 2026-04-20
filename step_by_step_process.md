# LangGraph Multi-Agent Production Scheduling System: Step-by-Step Process

This document details the step-by-step execution flow of the production scheduling multi-agent system (MAS) built with LangGraph, LangChain, and Ollama.

## 1. Initialization and Setup
- **Environment Setup**: The system loads environment variables (e.g., from a `.env` file) using `dotenv`. This sets up any necessary API keys (if applicable) and configurations.
- **Graph Compilation**: `main.py` calls `build_graph()` from `graph/workflow.py`. This instantiates all the agents, the RAG retriever, and wires them together into a sequential `StateGraph`. The graph is then compiled into a runnable application.
- **Initial State Definition**: An initial `GraphState` is defined, containing the starting "Normal operation" schedule, an empty list for agent proposals, and the factory events to process.

## 2. Event Processing Loop
The main script iterates through a predefined list of factory events (e.g., "Machine D overheating", "Rush Order #992"). For each event, it triggers a full execution of the LangGraph workflow.

### Step 2.1: Graph Invocation
The state object is populated with the `current_event` and pushed into the graph via `app.invoke(state)` (or via streaming).

### Step 2.2: RAG Node (`retrieve_context_node`)
- **Action**: This is the entry point of the graph. It uses the `FactoryDataRetriever` (RAG module).
- **Process**: The module takes the `current_event` string and performs a similarity search against the local `Chroma` vector store using `OllamaEmbeddings` (`nomic-embed-text`).
- **State Update**: The retrieved relevant historical logs and real-time factory data are injected into the graph state under the `factory_context` key.

### Step 2.3: Machine Agent Node (`machine_agent_node`)
- **Action**: Once the context is retrieved, the graph transitions to the `MachineAgent`.
- **Process**: The agent reads the `current_event` and the newly updated `factory_context`. Using the `ChatOllama` LLM (`llama3.2`), it evaluates the local, machine-level impact of the event (e.g., estimating repair times or local capacity constraints).
- **State Update**: The agent appends its assessment to the `agent_proposals` list inside the state.

### Step 2.4: Production Line Agent Node (`line_agent_node`)
- **Action**: The graph hands off the state to the `ProductionLineAgent`.
- **Process**: This agent prompts the LLM with the `current_event`, `factory_context`, AND the previous machine-level proposals. It synthesizes this to determine line-level impacts (e.g., routing work elsewhere, adjusting conveyor speeds).
- **State Update**: The agent appends its broader line-level proposal to the `agent_proposals` list.

### Step 2.5: Scheduler Agent Node (`scheduler_agent_node`)
- **Action**: The final intelligence node in the workflow, invoking the `SchedulerAgent`.
- **Process**: This top-level orchestrator agent reviews everything: the event, the context, the current operational schedule, and the combined proposals from both the Machine and Production Line agents. 
- **State Update**: It generates a comprehensive, updated factory schedule that resolves the disruption. It overwrites the `schedule` key in the state with this final output and marks `is_resolved = True`.

## 3. Completion and Recursion
- **Graph End**: The graph reaches the defined `END` node.
- **Output**: `main.py` captures the final state, prints the `FINAL SCHEDULE/ACTION` to the console, and updates the baseline schedule for the next event in the loop.
- **Next Event**: The loop repeats, processing the next event using the freshly updated schedule as the baseline.
