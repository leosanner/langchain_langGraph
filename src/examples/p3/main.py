from typing import Annotated, List, Literal
from dataclasses import dataclass
import operator
import random
from langgraph.graph import StateGraph
from langgraph.constants import START, END


@dataclass
class State:
    called_nodes: Annotated[List[str], operator.add]
    token_limit: int = 512
    total_tokens: int = 0


def node_a(state: State) -> State:
    tokens = random.randint(480, 520)

    return State(called_nodes=["A"], total_tokens=tokens)


def node_b(state: State) -> State:
    return State(called_nodes=["B"], total_tokens=state.total_tokens)


def node_c(state: State) -> State:
    return State(called_nodes=["C"], total_tokens=state.total_tokens)


def condition(state: State) -> Literal["B", "C"]:
    token_limit = state.token_limit
    total_tokens = state.total_tokens

    if total_tokens > token_limit:
        return "B"

    return "C"


builder = StateGraph(State)

builder.add_node("A", node_a)
builder.add_node("B", node_b)
builder.add_node("C", node_c)

builder.add_edge(START, "A")
builder.add_conditional_edges("A", condition, {"B": "B", "C": "C"})
builder.add_edge("B", END)
builder.add_edge("C", END)

model = builder.compile()
response = model.invoke(State(called_nodes=[]))

print(response)
