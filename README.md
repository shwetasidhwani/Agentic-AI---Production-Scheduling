# Multi-Agent System for Adaptive Production Scheduling

This repository contains a proof-of-concept Multi-Agent System (MAS) built utilizing **LangChain** and **LangGraph**. It represents a smart factory environment where multiple AI agents collaborate to dynamically adjust production schedules in response to unforeseen events (like machine breakdowns or rush orders).

## Architecture

1. **RAG Module (`rag/factory_data.py`)**:
   Uses `langchain_community.vectorstores.Chroma` to embed and search textual factory logs. It provides real-time context to the agents about machine statuses, maintenance histories, and inventory levels.
2. **Graph Context/State (`graph/state.py`)**:
   A `TypedDict` that flows through the LangGraph nodes, holding current events, agent proposals, and the active schedule.
3. **AI Agents (`agents/`)**:
   - **Machine Agent**: Analyzes the event against factory data directly relevant to a specific machine (e.g., capability, repair time).
   - **Production Line Agent**: Takes the machine's assessment and proposes line-level solutions (e.g., routing work to another line or adjusting conveyor speed).
   - **Scheduler Agent**: The global coordinator that takes all proposals and formulates the finalized production schedule.
4. **LangGraph Workflow (`graph/workflow.py`)**:
   Coordinates the sequential invocation of the RAG module and the agents.

## Setup Instructions

### Prerequisites
- Python 3.9+
- OpenAI API Key (The agents use `gpt-3.5-turbo` and `gpt-4-turbo-preview` by default).

### Installation
1. Navigate to the project folder (`c:\Users\Sidhwani\OneDrive\Desktop\MPR8\production_scheduling_mas`).
2. Create and activate a Virtual Environment (recommended).
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set your OpenAI API key. Create a `.env` file in the root directory and add:
   ```env
   OPENAI_API_KEY=your-api-key-here
   ```

### Execution
Run the main script to simulate events on the factory floor:
```bash
python main.py
```

### Mock Data
Mock factory logs are located in `data/factory_logs.txt`. The RAG system embeds these continuously to answer contextual questions during the agent evaluation loop.
