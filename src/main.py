import os
import json
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import Response
from dotenv import load_dotenv
from loguru import logger

from generator import generate_payload, get_byte_length

load_dotenv()

app = FastAPI()

HOSTNAME = os.getenv("HOSTNAME")
PORT = int(os.getenv("PORT", 3333))

TWIML_SIZE = 60 * 1024  # 60KB
COMPRESSIBILITY = "lipsum"  # determines the compressibility of the custom payload. Options: random | maximally | lipsum


@app.post("/incoming-call")
async def incoming_call():
    logger.info("Webhook: /incoming-call")

    greeting = "Say something."

    twiml = f"""<Response>
  <Connect>
    <ConversationRelay
      url="wss://{HOSTNAME}/relay"
      welcomeGreeting="{greeting}"
      transcriptionProvider="deepgram"
      speechModel="nova-3-general"
    >
      <Parameter name="target" value="__XXX__"/>
    </ConversationRelay>
  </Connect>
</Response>"""

    twiml_size = get_byte_length(twiml)
    payload_size = TWIML_SIZE - 500 - twiml_size

    target = generate_payload(payload_size, COMPRESSIBILITY)
    final_twiml = twiml.replace("__XXX__", target)

    logger.info(f"TwiML size (bytes): {get_byte_length(final_twiml)}")

    return Response(content=final_twiml, media_type="text/xml")


@app.post("/call-status")
async def call_status(request: Request):
    form_data = await request.form()
    call_sid = form_data.get("CallSid")
    call_status = form_data.get("CallStatus")

    logger.info(f"Call Status - SID: {call_sid}, Status: {call_status}")

    return Response(status_code=200)


@app.websocket("/relay")
async def relay_websocket(websocket: WebSocket):
    await websocket.accept()
    logger.info("Relay: initialized")

    try:
        while True:
            data = await websocket.receive_text()

            try:
                msg = json.loads(data)

                if msg.get("type") == "setup":
                    logger.info(f"Setup: {msg}")

                elif msg.get("type") == "prompt":
                    if not msg.get("last"):
                        continue

                    logger.info(f"Message: {msg}")

                    response = {
                        "type": "text",
                        "token": msg.get("voicePrompt"),
                        "last": True,
                    }

                    await websocket.send_text(json.dumps(response))

            except (json.JSONDecodeError, KeyError) as e:
                logger.info(f"Error processing message: {e}")

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")


if __name__ == "__main__":
    import uvicorn

    logger.info(f"Server running on http://localhost:{PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)
