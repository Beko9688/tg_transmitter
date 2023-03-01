import os
from telethon import TelegramClient, events, utils
from dotenv import load_dotenv

load_dotenv()

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
CHATS = [int(i) for i in os.getenv('CHATS').split(',')]
USERS = [int(i) for i in os.getenv('USERS_ID').split(',')] + [str(i) for i in os.getenv('USERNAMES').split(',')]
KEYWORDS = os.getenv('KEYWORDS')


client = TelegramClient('session_name', API_ID, API_HASH)


@client.on(events.NewMessage(chats=CHATS))
async def handle_message(event):
    print(event.message)
    message = event.message

    if any(item.lower() in message.message.lower() for item in KEYWORDS):
        for user in USERS:
            entity = await client.get_entity(user)
            from_chat_id = utils.get_peer_id(message.peer_id)
            await client.forward_messages(entity=entity, messages=[message.id], from_peer=from_chat_id)


with client:
    client.run_until_disconnected()
