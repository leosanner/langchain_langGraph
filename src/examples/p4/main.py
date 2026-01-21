from typing import TypedDict, Sequence, Annotated
from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.constants import START, END
from langgraph.graph import StateGraph, add_messages
from rich import print
from rich.markdown import Markdown

llm = init_chat_model("ollama:qwen2.5:1.5b")


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


def call_llm(state: AgentState) -> AgentState:
    llm_response = llm.invoke(state["messages"])
    return {"messages": [llm_response]}


builder = StateGraph(
    state_schema=AgentState,
    context_schema=None,
    input_schema=AgentState,
    output_schema=AgentState,
)

builder.add_node("call_llm", call_llm)
builder.add_edge(START, "call_llm")
builder.add_edge("call_llm", END)

graph = builder.compile()

if __name__ == "__main__":
    current_messages: Sequence[BaseMessage] = []

    print("\n" * 50)

    while True:
        user_input = input("Digite sua mensagem: ")

        if user_input.lower() in ["q", "exit"]:
            print(Markdown("---"))
            break

        print(Markdown("---"))
        human_message = HumanMessage(user_input)
        current_messages = [*current_messages, human_message]

        result = graph.invoke({"messages": current_messages})

        current_messages = result["messages"]
        llm_response = result["messages"][-1].content
        print(Markdown(llm_response))

        print(Markdown("---"))
