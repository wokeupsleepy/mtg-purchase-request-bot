import discord
from discord import ui
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os

load_dotenv()

discord_key = os.getenv("DISCORD_KEY")

intents = discord.Intents.default()

intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix='?', description="this is just a test bot", intents=intents)
bot = client.tree

def writeToFile(line, file="log.txt"):
    f = open(file, "a")
    f.write("\n")
    f.write(line)
    f.close()
    

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    try:
        synced = await bot.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello see this updated message!')

@bot.command(name="poopy")
async def poopy(interaction: discord.Interaction):
    """This is another test action"""
    await interaction.response.send_message("so silly")

@bot.command(name="add")
async def add(interaction: discord.Interaction, left: int, right: int):
    """Adds two numbers together."""
    await interaction.response.send_message(left + right)

@bot.command(name="say")
@app_commands.describe(output_phrase = "what you want?")
async def say(interaction: discord.Interaction, output_phrase: str):
    """test output phrase"""
    outputLine = f"{interaction.user.name} instructed bot to say '{output_phrase}'"
    writeToFile(outputLine)
    await interaction.response.send_message(outputLine)

@bot.command(name="purchase_request")
@app_commands.describe(card_name = "This is the name of the card you want.")
@app_commands.describe(quantity = "This is how many copies you want, the default value is 1.")
@app_commands.describe(printing = "This is the set you want singles to be from, by default the set won't matter.")
async def purchase_request(interaction: discord.Interaction, card_name: str, quantity: int=1, printing: str=""):
    """Use this to make a purchase request"""
    returnMessage = ""
    if card_name == "":
        returnMessage = f"No card has been selected, purchase request has not been made."
    else:
        returnMessage = f"{interaction.user.name} requested {quantity} copy/copies of {card_name}"

    if printing != "":
        returnMessage = returnMessage + f" from the set: {printing}"

    purchaseRequestCsv = f"{interaction.user.name},{card_name},{quantity},{printing}"
    writeToFile(purchaseRequestCsv,"purchase_requests.csv")

    await interaction.response.send_message(returnMessage)

client.run(discord_key)