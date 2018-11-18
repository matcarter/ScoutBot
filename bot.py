
# TODO Create functions
#   opgg(players) - returns url of op.gg lookup for players
#   getinfo(players) - returns objects of players containing their information from Riot API


import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import json

# Load the config file
with open('config.json') as json_data_file:
    data = json.load(json_data_file)

# Store config details
token = data['token']
prefix = data['prefix']
key = data['key']

# Initialize the bot
bot = commands.Bot(command_prefix=prefix)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.event
async def on_message(message):
    if message.content.startswith(prefix):
        print('command: ' + message.content[1:])


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send('Command not found!')
        await ctx.send('Use !help to see known commands')


@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')


@bot.command()
async def test(ctx, *args):
    await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))


bot.run(token)
