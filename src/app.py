from .graph.graph import build_graph
from .graph.state import GraphState

def main() -> None:
    graph = build_graph()

    initial_state = GraphState()

    graph.invoke(initial_state)

if __name__ == "__main__":
    main()
