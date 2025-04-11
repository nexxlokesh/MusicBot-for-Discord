import discord
from discord.ext import commands
import json

# Load the data from 'data.json'
with open('data.json', 'r') as f:
    config = json.load(f)

# Access values from the config
DISCORD_TOKEN = config.get("DISCORD_TOKEN")

# Validate environment variables
if not DISCORD_TOKEN:
    raise ValueError("DISCORD_TOKEN is not set in the data.json file.")

# List of cogs to load
exts = ["cogs.musicnexx"]

class Seemu(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents, **kwargs):
        super().__init__(command_prefix=command_prefix, intents=intents, **kwargs)

    async def setup_hook(self) -> None:
        # Load all extensions (cogs)
        for ext in exts:
            try:
                await self.load_extension(ext)
                print(f"{ext} loaded successfully.")
            except Exception as e:
                print(f"Failed to load {ext}: {e}")

        print("All cogs are loaded.")
        await self.tree.sync()  # Syncing the command tree

    async def on_ready(self):
        activity = discord.Game(name="Gaane sun lo") 
        await self.change_presence(activity=activity)
        print(f"Bot is ready as {self.user}")

# Run the bot
if __name__ == "__main__":
    intents = discord.Intents.all()  # Enable all intents

    bot = Seemu(command_prefix="!", intents=intents)

    try:
        bot.run(DISCORD_TOKEN)  # Start the bot using the token from data.json
    except discord.errors.LoginFailure:
        print("Invalid Discord token provided. Please check your data.json file.")
