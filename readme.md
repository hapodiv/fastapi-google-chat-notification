# FastAPI Google Chat Notification

This project is a FastAPI application that receives Slack-like webhook payloads and sends notifications to Google Chat.

## Table of Contents

- [FastAPI Google Chat Notification](#fastapi-google-chat-notification)
  - [Table of Contents](#table-of-contents)
  - [Setup](#setup)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Running the Application](#running-the-application)
  - [Testing the Application](#testing-the-application)
  - [Example Payload](#example-payload)
  - [Logging](#logging)

## Setup

### Prerequisites

- Python 3.x
- pip

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/hapodiv/fastapi-google-chat-notification.git
   cd fastapi-google-chat-notification
   ```

2. **Create a virtual environment:**

   ```sh
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   - On Windows:

     ```sh
     venv\Scripts\activate
     ```

   - On macOS and Linux:

     ```sh
     source venv/bin/activate
     ```

4. **Install the dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

5. **Copy the example environment file and set the environment variables:**

   ```sh
   cp .env.example .env
   ```

   Edit the `.env` file to set the actual values for `UVICORN_PORT` and `GOOGLE_CHAT_WEBHOOK_URL`.

## Running the Application

To run the FastAPI application, use the following command:

```sh
uvicorn main:app --reload --port $(grep UVICORN_PORT .env | cut -d '=' -f2)
```

The application will be available at `http://127.0.0.1:<UVICORN_PORT>`.

## Testing the Application

You can test the application using `curl` or any other API testing tool. Here is an example using `curl`:

```sh
curl --location 'http://127.0.0.1:<UVICORN_PORT>/send-to-google-chat/' \
--header 'content-type: application/x-www-form-urlencoded' \
--data-urlencode "payload=$(< payload.json)"
```

Replace `<UVICORN_PORT>` with the port number specified in your `.env` file.

## Example Payload

Here is an example of a payload that you can use for testing. Save this JSON content into a file named `payload.json`:

```json
{
  "text": "[[Hapo] hapo-pms] tuannd updated \\u003chttps://pms.haposoft.com/issues/15601|Feature #15601: Tích hợp bắn thông báo sang Google chat\\u003e",
  "link_names": 1,
  "username": "HapoBot",
  "channel": "hapo-pms",
  "attachments": [
    {
      "text": "test hook",
      "fields": [
        {
          "title": "Status",
          "value": "Doing",
          "short": true
        }
      ]
    }
  ],
  "icon_url": "https://blog.haposoft.com/content/images/size/w256h256/2021/10/haposoft-icon-180x180.png"
}
```

## Logging

The application logs will be printed to the console. Ensure you have logging enabled in your `.env` file if required.
