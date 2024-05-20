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

cog_files = ['moderation']

for cog_file in cog_files: # Cycle through the files in array
    bot.load_extension(cog_file) # Load the file
    print(f"{cog_file} has loaded.")

# Runs when Bot Succesfully Connects
@bot.event
async def on_ready():
    print(f'{bot.user} succesfully logged in!')


bot.run(TOKEN)