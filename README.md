# mtg-purchase-request-bot

This requires Python 3 and pip.

Required packages:
discord.py (https://discordpy.readthedocs.io/en/stable/quickstart.html)
python-dotenv (https://pypi.org/project/python-dotenv/)
mtgsdk (https://github.com/MagicTheGathering/mtg-sdk-python)

Here are some docs: https://discordpy.readthedocs.io/en/stable/intro.html#installing

You'll need to register a Discord bot here: https://discord.com/developers/applications/. From the bot, you'll get some sort of "token". This would go into a ".env" file and look something like this: DISCORD_KEY=YOUR_KEY_HERE

Once everything is ready, run "python3 test.py" (or in my case, my PATH variable resolves Python to "py")