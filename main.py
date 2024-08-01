import logging
from fastapi import FastAPI, Form, Request
import httpx
from dotenv import load_dotenv
import os
import json

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

GOOGLE_CHAT_WEBHOOK_URL = os.getenv("GOOGLE_CHAT_WEBHOOK_URL")

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.post("/send-to-google-chat/")
async def send_to_google_chat(request: Request):
    try:
        # Read payload from request
        form_data = await request.form()
        payload = form_data.get('payload')
        logger.debug("Received payload: %s", payload)

        if payload:
            slack_message_dict = json.loads(payload)
            logger.debug("Parsed slack message: %s", slack_message_dict)

            # Extract text from Slack message
            text = slack_message_dict.get('text', '')

            # Extract attachments from Slack message
            attachments = slack_message_dict.get('attachments', [])
            attachment_texts = []
            for attachment in attachments:
                attachment_text = attachment.get('text', '')
                fields = attachment.get('fields', [])
                field_texts = [f"*{field['title']}*: {field['value']}" for field in fields]
                attachment_texts.append(f"> {attachment_text}\n> " + "\n> ".join(field_texts))

            full_text = f"{text}\n" + "\n".join(attachment_texts)
            logger.debug("Constructed full text: %s", full_text)

            google_chat_message = {
                "text": full_text
            }
            logger.debug("Google Chat message: %s", google_chat_message)

            headers = {'Content-Type': 'application/json; charset=UTF-8'}
            async with httpx.AsyncClient() as client:
                response = await client.post(GOOGLE_CHAT_WEBHOOK_URL, json=google_chat_message, headers=headers)
                response.raise_for_status()
                logger.debug("Response status: %s", response.status_code)

            return {"status": "Message sent to Google Chat successfully"}
        else:
            logger.error("Invalid payload: payload is None")
            return {"status": "Invalid payload"}, 400
    except json.JSONDecodeError as e:
        logger.error("JSON decode error: %s", str(e))
        return {"status": "Invalid JSON payload"}, 400
    except Exception as e:
        logger.error("Error sending message to Google Chat: %s", str(e))
        return {"status": "Error sending message"}, 500
