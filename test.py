from datetime import datetime, timezone
import discord
from discord import ui
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import os
from CardNameChecker import * 

# NOTE: This here is just some set up
load_dotenv()
discord_key = os.getenv("DISCORD_KEY")
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = commands.Bot(command_prefix='?', description="this is just a test bot", intents=intents)
bot = client.tree

purchaseRequestFileName = "purchase_requests"

def constructFileNameForUser(user: str):
    return f"{purchaseRequestFileName}_{user}.csv"

# NOTE: These are the actual bot functions
def writeToFile(line, file="log.txt"):

    try:
        createFileIfNotExists = open(file, "x")
    except Exception as e:
        fileAlreadyExists = "nothing needed here, I just need a way to make the file if it doesn't exist already"

    file = open(file, "r+")
    lineCounter = 0 
    # Reading from file
    fileContents = file.read()
    colist = fileContents.split("\n")
    
    for i in colist:
        if i:
            lineCounter += 1

    # NOTE: This is sort of a bad way to generate an ID, I think we should have some sort of metadata file
    file.write(f"{lineCounter}|{line}")
    file.write("\n")
    file.close()
    
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
        utc_time = datetime.now(timezone.utc)
        await message.channel.send(f'Hello, this is a quick heartbeat ping, the current time is: {utc_time}')

@bot.command(name="test")
async def test(interaction: discord.Interaction):
    """This is another test slash action"""
    await interaction.response.send_message("You can't see me *John Cena handwave*")

# NOTE: I think maybe I should implement some sort of rate-limiting? Maybe it's a setting that can be done on the Discord developer page side?
@bot.command(name="say")
@app_commands.describe(output_phrase = "This will write to a log file that I (Tom) will read")
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
    user = interaction.user.name
    returnMessage = ""
    try:
        if card_name.strip() == "":
            returnMessage = f"No card name has been supplied, purchase request has not been made."
            raise Exception(returnMessage)
        else:
            checkerInstance = CardNameChecker()
            discoveredCards = checkerInstance.find_cards_by_name_set(card_name, printing)
            # NOTE TODO: We may need to handle cases where there are multiple distinct names, figure this out later; for example, there is the card "Fury" and other cards with "Fury" in its name
            firstCardName = discoveredCards[0].name

            if len(discoveredCards) <= 0:
                raise Exception("No card found for given parameters; review your inputs")
            else:            
                returnMessage = f"{user} requested {quantity} copy/copies of {firstCardName}"
                if printing != "":
                    returnMessage = returnMessage + f" from the set: {printing}"
                purchaseRequestCsv = f'{user}|"{firstCardName}"|{quantity}|"{printing}"'
                writeToFile(purchaseRequestCsv, constructFileNameForUser(user))

        await interaction.response.send_message(returnMessage)
    except Exception as e:
        await interaction.response.send_message(f"ERROR in purchase_request: {e}")


@bot.command(name="get_requests")
@app_commands.describe(user = "Specify the user you want records for")
async def get_requests(interaction: discord.Interaction, user: str):
    try:
        if len(user) > 32 or '/' in user or '\\' in user:
            raise Exception("Invalid username")
        
        requestsFileName = constructFileNameForUser(interaction.user.name)
        """Use this to list out all purchase requests, this is useful for finding what you've asked for."""
        file = open(requestsFileName, "r")
        # NOTE: We can maybe format this if necessary
        fileContents = file.read()
        file.close()

        if user != "":
            fileLines = fileContents.split("\n")
            userRequests = []
            
            for line in fileLines:
                # NOTE: In lineArray, the set of values goes ID, user, cardname, quantity, printing/set
                lineArray = line.split("|")
                if len(lineArray) > 1:
                    if lineArray[1] == user:
                        userRequests.append(line)
            
            userRequestsContents = ""
            for request in userRequests:
                userRequestsContents += request
                userRequestsContents += "\n"
            
            await interaction.response.send_message(userRequestsContents)
        else:
            await interaction.response.send_message(fileContents)
    except Exception as e:
        await interaction.response.send_message(e)

client.run(discord_key)