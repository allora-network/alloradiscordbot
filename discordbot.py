import requests, responses
from dotenv import load_dotenv
import os 
from discord import Client, Intents, Message
from responses import get_response

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN') # need to change this to correct token

intents = Intents.default()

intents.message_content = True # NOQA

client = Client(intents=intents)

async def send_message(message: Message,  user_message: str) -> None:
    if not user_message:
        print("Please enter a message")
        return
    
    if is_private :=user_message[0]=="?":
        user_message = user_message[1:] #slice to remove the question mark

    try:
        print("Sending message to API")
        response = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response) # if private send to author otherwise send to channel
    except Exception as e:
        print(e)

# handle startup for the bot
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

# handles incoming messages
@client.event
async def on_message(message: Message):
    # Ignore messages from the bot itself to avoid infinite recursion.
    if message.author == client.user:
        return

    # Check if the message starts with '!ask'
    if message.content.startswith("!ask"):
        # remove the '!ask' prefix and  extra whitespace.
        query = message.content[len("!ask"):].strip()

        #  check if the user provided a query after the command.
        if not query:
            await message.channel.send("Please enter a message after !ask.")
            return

        print(f'{message.author} asked: {query} in {message.channel}')
        await send_message(message, query)

# main entry point

def main():
    client.run(token = TOKEN)

if __name__ == "__main__":
    main()