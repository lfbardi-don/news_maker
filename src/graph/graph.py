from langgraph.graph.state import CompiledStateGraph, StateGraph, START, END

from graph.state import GraphState
from graph.nodes.manager import manager, route
from graph.nodes.screen_writer import screen_writer
from graph.nodes.anchor import anchor
from graph.nodes.reporter import reporter
from graph.nodes.ask_topic import ask_topic

def build_graph() -> CompiledStateGraph:
    graph = StateGraph(GraphState)

    graph.add_node("input", ask_topic)
    graph.add_node("manager", manager)
    graph.add_node("screen_writer", screen_writer)
    graph.add_node("anchor", anchor)
    graph.add_node("reporter", reporter)

    graph.add_edge(START, "input")
    graph.add_edge("input", "manager")

    graph.add_conditional_edges(
        "manager",
        route,
        {
            "screen_writer": "screen_writer",
            "anchor": "anchor",
            "reporter": "reporter",
            END: END,
        },
    )

    graph.add_edge("screen_writer", "manager")
    graph.add_edge("anchor", "manager")
    graph.add_edge("reporter", "manager")

    return graph.compile()
