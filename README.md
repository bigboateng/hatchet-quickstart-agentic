
# Hatchet Slack Bot Example

This project demonstrates a Slack bot application using FastAPI for the backend API, Hatchet for task management and workflow orchestration, and OpenAI for generating responses. It showcases the power and flexibility of Hatchet in managing complex workflows for Slack bot interactions.

## Key Features

- Multiple workflows: Separate workflows for handling different types of Slack events
- OpenAI integration: Generates responses using OpenAI's GPT-3.5 model
- Slack integration: Communicates with Slack using the Slack SDK

## Quick Start

To get the project running quickly:

1. Clone the repository

### Setting Up the Slack App and Bot

1. **Set up ngrok for port forwarding**:
   ngrok is needed to expose your local development server to the internet. This allows Slack to send events to your local machine for testing and development purposes. Without ngrok, Slack would not be able to reach your local server since it is behind a firewall and not accessible from the internet.

   - Install ngrok from https://ngrok.com/.
   - Run ngrok to forward requests to your local server (note: we have not started the server yet, but that's fine):
     ```bash
     ngrok http 8000
     ```
   - Copy the generated ngrok URL and update the `request_url` fields in the `slack-manifest.yml` file

2 . **Create a new Slack app**:
   - Go to the Slack API website (https://api.slack.com/apps) and create a new app.
   - Choose "From an app manifest" and select your workspace.

3 **Use the provided Slack manifest**:
   - Copy the contents of the `slack-manifest.yml` file in the repository.
   - Paste it into the Slack app manifest editor and create the app.

4. **Add the bot to your workspace and create a new channel**:\
   - Go to your Slack workspace and add the newly created bot to your workspace.
   - Create a new channel in your Slack workspace.
   - Invite the bot to the newly created channel.

5. Copy the pre-filled environment file:
   ```bash
   cp backend/.env.template backend/.env
   ```
   
6. Set up your Hatchet API Key, Slack Bot Token, and OpenAI API Key in the `.env` file (see Environment Setup section)
7. Run the start-all script:
   ```bash
   ./start-all.sh
   ```
8. **Interact with the bot**:
   - You can now send messages in Slack, and the bot should respond.
   - The messages can vary from generic questions to meeting-related inquiries.
   - The bot will use the various workflows to generate appropriate responses.



This will start the FastAPI server, Hatchet worker, and set up the Slack bot.

## Manual Setup

If you prefer to start services individually:

1. Install dependencies (if not already installed):
   ```bash
   cd backend
   poetry install  # Run this only if you haven't installed dependencies yet
   ```

2. Start the FastAPI server:
   ```bash
   cd backend
   poetry run start-api
   ```

3. Start the Hatchet worker:
   ```bash
   cd backend
   poetry run start-worker
   ```

## Usage

Once the services are running, you can interact with the Slack bot by sending messages in the channel you created which has the bot in it, and the bot will respond.

## Project Structure

- `backend/`: FastAPI server and Hatchet workflows

## Environment Setup

Before running the project, you need to configure your environment variables. We've provided a `.env.template` file to guide you through the process.

### Steps to Set Up the Environment

1. **Copy the `.env.template` file to create a `.env` file**:

   ```bash
   cp backend/.env.template backend/.env
   ```

2. **Get your Hatchet API Key**:
   - Navigate to your settings tab in the Hatchet dashboard.
   - Look for the section called "API Keys".
   - Click "Create API Key" and input a name for the key.
   - Copy the generated API key.

3. **Get your Slack Bot Token**:
   - Navigate to your Slack app settings.
   - Look for the section called "OAuth & Permissions".
   - Copy the Bot User OAuth Token.

4. **Fill in the values for the environment variables**:

   `HATCHET_CLIENT_TOKEN`: Paste your Hatchet API key here.
   `SLACK_BOT_TOKEN`: Paste your Slack Bot Token here.
   `OPENAI_API_KEY`: Paste your OpenAI API key here.

5. Save the `.env` file. Ensure that it remains in the backend directory, as this is where the application expects it.



### Important Notes

Do not commit your `.env` file to version control. The `.env` file contains sensitive information like tokens and passwords. We've already included `.env` in the `.gitignore` file to prevent it from being accidentally committed.

