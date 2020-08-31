import discord
from discord.ext import commands
import matchupdata
import framedata

client = commands.Bot(command_prefix = '3s.')

@client.event
async def on_ready():
    print('Bot is ready')

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pinging @ {round(client.latency * 1000)}ms')

# @client.command()
# async def mu(ctx, *, c1, c2):
#     await ctx.send(arg)

# @client.command()
# async def frames(ctx, *, char, move):
    

client.run('NzUwMDE0NzEzNzIyODMwOTkw.X00Xog.rumLMCfbnCjEpnqPxQ8rOcuf0ns')