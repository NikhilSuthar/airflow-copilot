from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    TurnContext,
)
from langgraph.checkpoint.postgres import PostgresSaver
from botbuilder.schema import Activity, ActivityTypes, Attachment
from airflow_copilot.agent.agent import airflow_agent as agt
from botbuilder.core import ActivityHandler, TurnContext, CardFactory, MessageFactory
import logging as logs
from airflow_copilot.bot.card import delete_card, airflow_credential
from airflow_copilot.config.settings import get_environment
from airflow_copilot.config.CredentialStore import save_user_credentials,test_credential
import time
from botbuilder.core.teams import TeamsInfo
import re
from typing import Union


logs = logs.getLogger(__name__)

class TeamsBot(object):


    @staticmethod
    def extract_clean_code(response: Union[str, list]) -> str:
        # If the response is a list (e.g., multiple lines), join into a single string
        if isinstance(response, list):
            response = "\n".join(response)

        # Safety: Ensure it's now a string
        if not isinstance(response, str):
            raise TypeError(f"Expected string or list of strings, got {type(response)}")

        # Try to extract the first Python code block
        match = re.search(r"```python\s*(.*?)```", response, re.DOTALL)
        if match:
            # Return the cleaned code block
            code = match.group(1).strip()
            return f"```python\n{code}\n```"

        # If no code block found, return raw response
        return response.strip()

    

    @staticmethod
    def get_adapter():
        """
        Create a BotFrameworkAdapter with the provided configuration.
        """
        env = get_environment()
        settings = BotFrameworkAdapterSettings(env.microsoft_app_id, env.microsoft_app_password)
        adapter = BotFrameworkAdapter(settings)
        adapter.on_turn_error = TeamsBot.on_error
        return adapter

    @staticmethod
    async def on_error(context: TurnContext, error: Exception):
        logs.error(f"[on_turn_error] unhandled error: {error}")
        await context.send_activity("The bot encountered an error or bug.")
        await context.send_activity("To continue to run this bot, please fix the bot source code.")
    
    @staticmethod
    async def on_teams_card_action_invoke(turn_context: TurnContext, user_id: str):
        payload = turn_context.activity.value
        if payload.get("type") == "delete_history":
            await TeamsBot.delete_langgraph_user_data(user_id=user_id)
            msg = "🌿 **History cleaned!**\n*Thanks for keeping things green and speedy!*"
            await turn_context.send_activity(msg)

        elif payload.get("type") == "cancel":
            msg = "🗃️ **No cleanup today!**\n*We’re keeping your chat just the way you left it.*"
            await turn_context.send_activity(msg)

        elif payload.get("type") == "submit_airflow_credentials":
            if not payload.get("airflow_user", "").strip():
                msg = "⚠️ Please enter a valid **username**."
            elif not payload.get("airflow_pass", "").strip():
                msg = "⚠️ Please enter a valid **password**."
            else:
                success = await save_user_credentials(
                    thread_id=user_id,
                    username=payload["airflow_user"],
                    password=payload["airflow_pass"]
                )

                if success:
                    # Temporary wait message
                    msg = "💬 **Credentials saved!**\n*Testing your connection...* 🔄"
                    await turn_context.send_activity(msg)
                    time.sleep(2)
                    response = await test_credential(user_id=user_id)
                    status = str(response).lower().split("|", 1)[0]

                    if status == "success":
                        msg = "✅ **Test successful!**\n*You're all set to start your Airflow conversation.* 🚀"
                    else:
                        msg = f"❌ **Test failed.**\n*Please double-check your credentials.*\n> {str(response).lower().split('|', 1)[1]}"
                else:
                    msg = (
                        "⚠️ **Oops—couldn't save your credentials.**\n"
                        "*Make sure your Fernet key is configured correctly and try again.* 🔐"
                    )
            await turn_context.send_activity(msg)

        else:
            await turn_context.send_activity("⚠️ Unknown action type. Please try again.")


    @staticmethod
    async def delete_langgraph_user_data(user_id: str):
        # ✨ Your custom logic here to delete LangGraph conversation thread
        logs.info(f"Deleting conversation for user {user_id}")
        env = get_environment()
        with PostgresSaver.from_conn_string(env.db_uri) as checkpointer:
            checkpointer.delete_thread(user_id)


   
    @staticmethod
    async def on_turn(turn_context: TurnContext):
        user_name = turn_context.activity.from_property.name
        teams_user = await TeamsInfo.get_member(turn_context, turn_context.activity.from_property.id)
        user_id = teams_user.email

        user_input = turn_context.activity.text
        msg_value = turn_context.activity.value
        logs.info(f"**Processing Msg {user_input} from user {user_id}")
        await turn_context.send_activity(Activity(type=ActivityTypes.typing))
        if msg_value is not None:
            await TeamsBot.on_teams_card_action_invoke(turn_context=turn_context,user_id = user_id)
            return

        if str(user_input).strip().replace(' ','').lower() == 'refreshhistory':
            card = delete_card
            await turn_context.send_activity(
                MessageFactory.attachment(CardFactory.adaptive_card(card))
            )
            return
        elif str(user_input).strip().replace(' ','').lower().startswith('updatemyairflowcred'):
            card = airflow_credential
            await turn_context.send_activity(
                MessageFactory.attachment(CardFactory.adaptive_card(card))
            )
            return
        elif (user_input is not None):
            await turn_context.send_activity(Activity(type=ActivityTypes.typing))
            response = await agt.airflow_connect(user_id=user_id, user_input=user_input, user_name=user_name)
            response = TeamsBot.extract_clean_code(response)
            logs.debug(f"Response get {response}")
            logs.info(f"Response sent to user {user_id}")
            message = Activity(
                type=ActivityTypes.message,
                text=response,
                text_format="markdown"
            )
            await turn_context.send_activity(message)
            return
        

        