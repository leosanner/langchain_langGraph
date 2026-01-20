from typing import Annotated, Literal
from langgraph.graph import StateGraph
from langgraph.constants import START, END
import operator
from dataclasses import dataclass


@dataclass
class State:
    nodes_path: Annotated[list[str], operator.add]
    current_number: int = 0


def node_a(state: State) -> State:
    print(f"Estado recebido pelo node A: {state=}")

    return State(nodes_path=["A"], current_number=state.current_number)


def node_b(state: State) -> State:
    print(f"Estado recebido pelo node B: {state=}")

    return State(nodes_path=["B"], current_number=state.current_number)


def node_c(state: State) -> State:
    print(f"Estado recebido pelo node B: {state=}")

    return State(nodes_path=["C"], current_number=state.current_number)


def the_conditional(state: State) -> Literal["B", "C"]:
    if state.current_number >= 50:
        return "C"

    return "B"


builder = StateGraph(State)
builder.add_node("A", node_a)
builder.add_node("B", node_b)
builder.add_node("C", node_c)

builder.add_edge(START, "A")
builder.add_conditional_edges("A", the_conditional, ["C", "B"])
builder.add_edge("C", END)
builder.add_edge("B", END)

graph = builder.compile()
# graph.get_graph().draw_mermaid_png(output_file_path="file.png")

response = graph.invoke(State(nodes_path=[], current_number=100))
print(f"{response=}")
