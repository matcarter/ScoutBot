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
modules = data['modules']

description = 'A bot to scout League of Legends accounts'

# Initialize the bot
bot = commands.Bot(command_prefix=prefix, description=description)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


# Handle errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        await ctx.send('Command not found!')
        await ctx.send('Use !help to see known commands')


@bot.command(description='Pong!')
async def ping(ctx):
    """Pong!"""
    await ctx.send('Pong!')


@bot.command(description='Return an op.gg lookup of inputted players')
async def opgg(ctx, *args):
    """Pull up op.gg for players"""
    url = 'http://na.op.gg/'

    if len(args) == 1:
        url += 'summoner/userName=' + args[0]
    elif len(args) > 1:
        url += 'multi/query=' + args[0]
        for i in range(1, len(args)):
            url += '%2C' + args[i]

    await ctx.send(url)


if __name__ == "__main__":
    for module in modules:
        try:
            bot.load_extension('modules.' + module)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(module, exc))

    bot.run(token)
