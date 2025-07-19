from airflow_copilot.tool_registry.airflow_tools import AirflowTools
from airflow_copilot.agent.prompt import get_system_prompt
from typing import Literal
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage
from langgraph.prebuilt import ToolNode
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from airflow_copilot.reducer.AsyncSummarization import AsyncSummarization
from airflow_copilot.reducer.GraphState import GraphState
import logging as logs
from airflow_copilot.config.settings import get_environment
from airflow_copilot.config.settings import user_id_context


logs = logs.getLogger(__name__)

class airflow_agent(object):
    """
    This class represents an agent that can interact with the Airflow system.
    It is designed to handle tasks such as executing workflows, managing tasks,
    and interacting with the Airflow API.
    """

    
    @staticmethod
    async def airflow_connect(user_id: str, user_input: str, user_name: str) -> str:
        """
        Execute a workflow in Airflow by its ID.
        """
        try:
            env = get_environment()
            user_id_context.set(user_id)
            model = init_chat_model(model=env.model_name, model_provider=env.provider_name, temperature=0, api_key=env.api_key)
            system_prompt =  get_system_prompt(user_name=user_name)
            async with AsyncPostgresSaver.from_conn_string(env.db_uri) as checkpointer:
                tools =  AirflowTools.get_all_tools()
                tools_by_name = {tool.name: tool for tool in tools}
                llm_with_tools = model.bind_tools(tools)
                async def model_call(state:GraphState):
                    """LLM decides whether to call a tool or not"""
                    summary = state.get("summary", "")
                    messages = state["messages"]
                    if str(summary).strip() != "":
                        logs.debug(f"Summary got:-- {summary}")
                        logs.debug(f"Model Input Message are {messages}")
                        return {
                        "messages": [
                            await llm_with_tools.ainvoke(
                                [SystemMessage(content=system_prompt)] + 
                                [SystemMessage(content=summary)] +
                                messages
                            )
                            ] 
                        }
                    else:
                        logs.debug(f"No summmary found")
                        logs.debug(f"message are {messages}")
                        return {
                        "messages": [
                            await llm_with_tools.ainvoke(
                                [SystemMessage(content=system_prompt)] + state["messages"]
                            )
                            ]
                        }

                # Define the tool node that will be called when the LLM makes a tool call
                # This node will invoke the tool and return the result
                async def tool_node(state: dict):
                    """Performs the tool call"""
                    logs.debug("At Tool Node")
                    result = []

                    for tool_call in state["messages"][-1].tool_calls:
                        tool = tools_by_name[tool_call["name"]]
                        observation = await tool.ainvoke(tool_call["args"])
                        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
                    return {"messages": result}

                # Conditional edge function to route to the tool node or end based upon whether the LLM made a tool call
                def should_continue(state: GraphState) -> Literal["tools", END]: # type: ignore
                    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

                    messages = state["messages"]
                    last_message = messages[-1]
                    logs.debug(f"Last Message at Check --> {last_message}")
                    # If the LLM makes a tool call, then perform an action
                    if last_message.tool_calls:
                        return "Action"
                    else:        # Otherwise, we stop (reply to the user)
                        return END

                # Build workflow
                graph = StateGraph(GraphState)

                # Add nodes
                graph.add_node("summarize", AsyncSummarization.summarize_message)
                graph.add_node("model_call", model_call)
                graph.add_node("tools", tool_node)
                # Add edges to connect nodes
                graph.add_edge(START, "summarize")
                graph.add_edge("summarize","model_call")
                
                graph.add_conditional_edges(
                    "model_call",
                    should_continue,
                    {
                        "Action": "tools",
                        END: END
                    },
                )
                graph.add_edge("tools", "model_call")

                # Compile the agent
                app = graph.compile(checkpointer=checkpointer)
                # from IPython.display import display, Image
                # display(Image(app.get_graph(xray=True).draw_mermaid_png()))
                config = {
                "configurable": {
                    "thread_id": user_id 
                }
                }
                app.with_config(recursion_limit=5)
                response = await app.ainvoke({"messages": [HumanMessage(content=user_input)]},config=config, debug=False)
                llm_response = response["messages"][-1]
                llm_response = llm_response.content
                logs.debug(f"llm_response -- {llm_response}")
                return llm_response
        except Exception as e:
            import traceback
            traceback.print_exc()  # Logs full traceback to stdout
            return f"❌ Unhandled Error: {str(e)}"
