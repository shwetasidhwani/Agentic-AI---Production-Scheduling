import os
from dotenv import load_dotenv

# Load environment variables first, before importing modules that require them
load_dotenv()

from graph.workflow import build_graph
from graph.state import GraphState

def main():
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("ERROR: Please set GOOGLE_API_KEY in your environment or a .env file.")
        return

    print("=== LangGraph Multi-Agent Production Scheduling System ===")
    
    # Compile the graph
    app = build_graph()
    
    # Initial state
    initial_schedule = "Normal operation. All machines active. Line 1: 500 units/hr. Line 2: 450 units/hr."
    events = [
        "Machine D (Welding) overheating and shutting down. Need repair time estimate.",
        "Rush Order #992 received requiring Machine A and C by EOD."
    ]
    
    for event in events:
        print("\n" + "="*50)
        print(f"NEW EVENT: {event}")
        print("="*50)
        
        state = GraphState(
            messages=[],
            next_node="",
            current_event=event,
            factory_context="",
            schedule=initial_schedule,
            agent_proposals=[],
            is_resolved=False
        )
        
        # Run the graph
        config = {"recursion_limit": 10}
        
        # Invoke graph and stream output
        try:
            for output in app.stream(state, config=config):
                for node_name, state_update in output.items():
                    pass # Output is handled by print statements in nodes, but we could print state updates here
                    
            # Capture the final schedule from the final state object
            # Note: stream outputs intermediate states. We get the final state automatically inside `app.invoke`
            final_state = app.invoke(state, config=config)
            print("\n*** ALL AGENTS RESOLVED ***")
            print(f"FINAL SCHEDULE/ACTION:\n{final_state['schedule']}")
            
            # Update the global schedule for the next event 
            # In a real system, the new schedule persists
            initial_schedule = final_state['schedule']
            
        except Exception as e:
            print(f"\nError running graph: {e}")

if __name__ == "__main__":
    main()
