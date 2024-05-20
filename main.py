import os 
import random 
import discord
from dotenv import load_dotenv 
from discord.ext import commands

load_dotenv() 
TOKEN = os.getenv('DISCORD_TOKEN')  

# Define Intents for the Bot (modify based on your bot's needs)
intents = discord.Intents.default()
intents.message_content = True  # This intent is needed to process message content


# Initialize Bot and Denote The Command Prefix
bot = commands.Bot(command_prefix="!", intents=intents)

cog_files = ['cogs.moderation']

async def load_cogs(bot):  # Define an async function for loading cogs
    for cog_file in cog_files:
        try:
            await bot.load_extension(cog_file)  # Use await for async loading
            print(f"{cog_file} has loaded.")
        except Exception as e:
            print(f"Failed to load cog {cog_file}: {e}")

async def main():
    async with bot:
        await bot.load_extension('my_extension')
        await bot.start(TOKEN)
# Runs when Bot Succesfully Connects
@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')


bot.run(TOKEN)