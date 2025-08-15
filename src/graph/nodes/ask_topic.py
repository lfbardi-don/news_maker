from ..state import GraphState

def ask_topic(state: GraphState) -> dict:
    topic = input("Enter the news topic: ")
    return { "topic": topic }