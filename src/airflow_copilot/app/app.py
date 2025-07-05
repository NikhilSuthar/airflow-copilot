from fastapi import FastAPI, Request, Header, Response
from airflow_copilot.bot.bot import TeamsBot
from botbuilder.schema import Activity, ActivityTypes, Attachment
import logging as logs


app = FastAPI()
logs.basicConfig(
    level=logs.INFO,  # <-- ensures info-level and above are shown
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)

@app.post("/api/messages")
async def messages(request: Request, authorization: str = Header(default="")):
    ADAPTER = TeamsBot.get_adapter()
    content_type = request.headers.get("content-type", "").lower()
    

    if "application/json" not in content_type:
        return Response(status_code=415, content="Unsupported Media Type")

    body = await request.json()
    activity = Activity().deserialize(body)
    response = await ADAPTER.process_activity(activity, authorization, TeamsBot.on_turn)
    if response:
        return Response(content=response.body, status_code=response.status)
    return Response(status_code=200)
