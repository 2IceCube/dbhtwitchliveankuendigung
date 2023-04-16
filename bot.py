import discord
import requests
import json
import time

with open('config.json') as f:
    config = json.load(f)

DISCORD_TOKEN = config['discord']['token']
DISCORD_CHANNEL_ID = config['discord']['channel_id']
TWITCH_CLIENT_ID = config['twitch']['client_id']
TWITCH_OAUTH_TOKEN = config['twitch']['oauth_token']
TWITCH_USER_NAME = config['twitch']['username']

def check_live_status():
    url = f'https://api.twitch.tv/helix/streams?user_login={TWITCH_USER_NAME}'
    headers = {
        'Client-ID': TWITCH_CLIENT_ID,
        'Authorization': f'Bearer {TWITCH_OAUTH_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    json_data = json.loads(response.text)
    if json_data['data']:
        return True
    else:
        return False
async def send_message():
    channel = client.get_channel(DISCORD_CHANNEL_ID)
    await channel.send('@everyone Hey, ich bin jetzt live auf Twitch! Schau doch mal vorbei: https://www.twitch.tv/2icecube')
client = discord.Client()
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
async def check_live():
    await client.wait_until_ready()
    while not client.is_closed():
        if check_live_status():
            await send_message()
        time.sleep(60)

client.loop.create_task(check_live())
client.run(DISCORD_TOKEN)
