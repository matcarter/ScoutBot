'''
    TODO Create functions
        opgg(players) - returns url of op.gg lookup for players
        getinfo(players) - returns objects of players containing their information from Riot API
'''

import discord
import asyncio
import json

with open('config.json') as json_data_file:
    data = json.load(json_data_file)

token = data['token']
prefix = data['prefix']
key = data['key']

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    # Don't reply to ourself
    if message.author == client.user:
        return

    # Found a command
    if message.content.startswith(prefix):
        command = message.content[1:].lower()  # Remove prefix
        args = command.split(' ', 1)  # Get any arguments

        # No arguments found
        if len(args) == 1:
            args = command
        # Set arguments
        else:
            args = args[1]

        # Ping!
        if command == 'ping':
            msg = '{0.author.mention} Pong!'.format(message)
            await client.send_message(message.channel, msg)


client.run(token)