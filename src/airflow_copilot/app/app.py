from fastapi import FastAPI, Request, Header, Response
from airflow_copilot.bot.bot import TeamsBot
from botbuilder.schema import Activity, ActivityTypes, Attachment
import logging as logs
from fastapi.responses import JSONResponse
from airflow_copilot.config.settings import get_environment


app = FastAPI()
env = get_environment()
log_level = str(env.log_level).upper()
logs.info(f"Log Level for API Call is {log_level}")
logs.basicConfig(
level=getattr(logs, log_level, logs.INFO),  # <-- ensures info-level and above are shown
format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
datefmt="%Y-%m-%d %H:%M:%S"
)

logs.info("🚀 FastAPI app is starting up")
@app.get("/health")
def health_check():
    return JSONResponse(content={"status": "ok"})

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
