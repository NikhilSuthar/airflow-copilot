
from langchain_core.messages import RemoveMessage, AnyMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.chat_models import init_chat_model
from airflow_copilot.reducer.GraphState import GraphState
import logging as logs
from airflow_copilot.config.settings import get_environment

env = get_environment()
log_level = str(env.log_level).upper()
logs.basicConfig(
level=getattr(logs, log_level, logs.INFO),  # <-- ensures info-level and above are shown
format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
datefmt="%Y-%m-%d %H:%M:%S"
)

class Summarization(object):
    env = get_environment()
    @staticmethod
    def get_summary(message, summary = "") -> str:
        logs.info("::::Request received for the summarization.")
        if len(message) > 0:
            model = init_chat_model(model=Summarization.env.summarization_model_name, 
                                    model_provider=Summarization.env.summarization_provider_name, 
                                    temperature=0, 
                                    api_key=Summarization.env.api_key)
            system_prompt =  ("You are a summarization assistant that summarizes long multi-turn conversations between a user and an AI assistant.")
            if str(summary).strip() == "":
                logs.debug(f"No Previous Summary Found.")
                human_msg =  ("""Read the given below conversation and generate a concise summary capturing the key details, user intent, and any relevant decisions or responses.
                                Conversation:
                                {message}
                                """)
            else:
                logs.debug(f"Previous Summary Found (length={len(summary)}). Extending with new messages.")
                human_msg = ("""An existing summary is provided below. Your task is to update or extend this summary based on the new conversation, ensuring it remains concise and coherent.
                                Existing Summary:"
                                {summary}
                                New Conversation:
                                {message}
                                """)
        else:
            logs.debug(f"::::No Input Message found for the summarization.")
            return ""
    
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", human_msg)
        ])

        chain = prompt | model | StrOutputParser()
        new_summary = chain.invoke({"message":message,"summary":summary})
        logs.debug(f"summary is {new_summary}")
        return new_summary
        
    @staticmethod
    def summarize_message(state:  GraphState):
        MIN_MSG_TO_RETAIN = Summarization.env.min_msg_to_retain
        MIN_MSG_TO_SUMMARIZE = Summarization.env.min_msg_to_summarize


        if MIN_MSG_TO_RETAIN is None or MIN_MSG_TO_SUMMARIZE is None or \
            MIN_MSG_TO_RETAIN == 0 or MIN_MSG_TO_SUMMARIZE == 0:
            logs.warning(f"::Properties MIN_MSG_TO_SUMMARIZE or MIN_MSG_TO_RETAIN is not set, Skip summarization.")
            return {
                "messages": state["messages"],
                "summary": ""
            }
        else:
            summary = state.get("summary", "")
            messages = state["messages"]
            logs.debug(f"Input message are {messages}")
            logs.debug(f"Length of input message before summarization is {len(messages)}")
            if len(messages) <= (MIN_MSG_TO_RETAIN + MIN_MSG_TO_SUMMARIZE):
                logs.debug("::::No summarization needed.")
                return {
                    "messages": messages,
                    "summary": summary
                }
            else:
                logs.debug("::::Checking summarization")
                last_human_msg = 0
                idx = -1
                for msg in messages[:-MIN_MSG_TO_RETAIN]:
                    idx = idx + 1
                    if isinstance(msg, HumanMessage):
                        last_human_msg =  idx
                to_be_summarize = messages[:last_human_msg]
                logs.debug(f"To be summarize message are {to_be_summarize}")
                logs.debug("::::Go for summarization")
                response =  Summarization.get_summary(to_be_summarize, summary)
                logs.debug(f"final message are {messages}")
                state = {   
                            "messages":[RemoveMessage(m.id) for m in to_be_summarize],
                            "summary":f"Summary of prior conversation: {response}"
                        }
                return state