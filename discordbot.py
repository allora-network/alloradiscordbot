import os
from dotenv import load_dotenv
import requests, responses
from discord import Client, Intents, Message
from responses import get_response
from flask import Flask
from threading import Thread

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')  # Ensure you have the correct token in your .env file

# Set up Discord intents and client
intents = Intents.default()
intents.message_content = True  # Enable access to message content
client = Client(intents=intents)

# Create a Flask app for the health check endpoint
app = Flask(__name__)

# health check
@app.route("/")
def health_check():
    return "ok", 200

def run_flask():
    # Run the Flask app on host 0.0.0.0 and port 3000 (or change as needed)
    app.run(host="0.0.0.0", port=3000)

async def send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print("Please enter a message")
        return

    # Check if message is intended to be private (starts with '?')
    is_private = user_message[0] == "?"
    if is_private:
        user_message = user_message[1:]  # Remove the '?' from the message

    try:
        print("Sending message to API")
        response = get_response(user_message)
        # Send a private message to the user if needed, otherwise send to the channel
        if is_private:
            await message.author.send(response)
        else:
            await message.channel.send(response)
    except Exception as e:
        print(e)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message: Message):
    # ignore messages from the bot itself to prevent infinite loops
    if message.author == client.user:
        return

    # check if message starts with '!ask'
    if message.content.startswith("!ask"):
        query = message.content[len("!ask"):].strip()  # Remove the prefix and extra whitespace

        if not query:
            await message.channel.send("Please enter a message after !ask.")
            return

        print(f'{message.author} asked: {query} in {message.channel}')
        await send_message(message, query)

def main():
    # we create a thread so we run health check and discord websocket at the same time
    flask_thread = Thread(target=run_flask)
    flask_thread.start()

    # Run the Discord bot
    client.run(TOKEN)

if __name__ == "__main__":
    main()
