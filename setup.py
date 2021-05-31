# Import Packages
import asyncio
import os

from dotenv import load_dotenv
import discord
from discord.ext import commands


# Load environment variables
load_dotenv()
token = os.getenv("TOKEN")
dev = os.getenv("DEV_ID")
activity = os.getenv("ACTIVITY")

# List of prefixes
# NOTE: PREFIXES ARE CASE SENSITIVE EVEN IF COMMANDS ARE SET TO CASE INSENSITIVE
prefixes = ['U!', 'u!']


# Defining Functions
def is_dev(context):
    return context.author.id == int(dev)


def get_prefix(client, message):
    return prefixes


# setting up the bot client
client = commands.Bot(command_prefix=get_prefix, case_insensitive=True, intents=discord.Intents.all())


# ping
@client.command(name="ping", description="Response time.")
async def ping(context):
    await context.send(f"Pong: {round(client.latency * 1000)}ms")


# load [cog_name]
@client.command(name="load", description="Load cog (Developer Only)")
@commands.check(is_dev)
async def load(context, extension):
    try:
        client.load_extension(f'cogs.{extension}')
        await context.message.add_reaction('👍')
    except Exception:
        await context.message.add_reaction('🚫')


# unload [cog_name]
@client.command(name="unload", description="Unload cog (Developer Only)")
@commands.check(is_dev)
async def unload(context, extension):
    try:
        client.unload_extension(f'cogs.{extension}')
        await context.message.add_reaction('👍')
    except Exception:
        await context.message.add_reaction('🚫')


# reload [cog_name]
@client.command(name="reload", description="Reload cog (Developer Only)")
@commands.check(is_dev)
async def reload(context, extension):
    try:
        client.unload_extension(f'cogs.{extension}')
        client.load_extension(f'cogs.{extension}')
        await context.message.add_reaction('👍')
    except Exception:
        await context.message.add_reaction('🚫')


# modules
@client.command(name="modules", description="List all the cogs (Developer Only)")
@commands.check(is_dev)
async def modules(context):
    msg = "List of Modules\n```txt\n"
    for module in os.listdir('./cogs'):
        if module.endswith('.py'):
            msg = msg + f"{module[:-3]}\n"
    msg = msg + "```"
    sent = await context.send(msg)
    await sent.add_reaction('⏹')

    def user_action(reaction, user):
        return reaction.message.id == sent.id \
               and user == context.author \
               and str(reaction.emoji) in ['⏹']

    try:
        reaction, user = await client.wait_for('reaction_add', timeout=45.0, check=user_action)

        if str(reaction) == '⏹':
            await sent.delete()
    except asyncio.TimeoutError:
        await sent.delete()


# listing and loading all the cogs
for file in os.listdir('./cogs'):
    if file.endswith('.py'):
        try:
            client.load_extension(f'cogs.{file[:-3]}')
            print(f"Loaded module: {file}")
        except Exception as e:
            print(f"Failed to load module: {file}, Error: {e}")


# error handling
@client.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandNotFound):
        return
    elif isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
        await context.send("Missing Required Argument(s)")
    else:
        return


# on ready event
@client.event
async def on_ready():
    print(f"LOGGED IN AS: {client.user}")
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(name=activity, type=discord.ActivityType.playing))


# running the bot client
client.run(token)
