from langchain_core.messages import  AnyMessage
from langgraph.graph.message import add_messages
from typing import Annotated, TypedDict


class GraphState(TypedDict):
    messages: Annotated[list[AnyMessage],add_messages]
    summary: str