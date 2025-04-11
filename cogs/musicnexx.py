import discord
import asyncio
import yt_dlp
import json
from discord.ext import commands
from discord.ui import Button, View
from datetime import datetime
from main import Seemu  # Assuming you have Seemu class in main.py

# Load config from data.json
with open('data.json', 'r') as f:
    config = json.load(f)

DISCORD_TOKEN = config.get("DISCORD_TOKEN")

# Initialize queues
queues = {}
yt_dl_options = {"format": "bestaudio/best"}
ytdl = yt_dlp.YoutubeDL(yt_dl_options)

ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -filter:a "volume=0.25"'
}

# Dictionary to keep track of the user controlling the music
active_users = {}

class MusicNexx(commands.Cog):
    def __init__(self, bot: Seemu):
        self.bot = bot

    async def play_next(self, ctx):
        if ctx.guild.id in queues and queues[ctx.guild.id]:
            url = queues[ctx.guild.id].pop(0)
            await self.play_song(ctx, url)
        else:
            await ctx.voice_client.disconnect()

    async def play_song(self, ctx, url):
        try:
            if ctx.voice_client is None:
                await ctx.author.voice.channel.connect()

            data = await asyncio.get_event_loop().run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
            song_url = data['url']
            song_title = data['title']
            song_thumbnail = data.get('thumbnail', "https://example.com/default-thumbnail.jpg")
            song_duration = data['duration']
            song_artist = data.get('uploader', 'Unknown Artist')

            # Limit title to first four words
            limited_title = ' '.join(song_title.split()[:4])

            player = discord.FFmpegOpusAudio(song_url, **ffmpeg_options)
            ctx.voice_client.play(player, after=lambda e: self.bot.loop.create_task(self.play_next(ctx)))

            # Create embed with song details
            embed = discord.Embed(
                title="🎶 Now Playing 🎶",
                description=limited_title,
                color=discord.Color.from_rgb(255, 229, 236)
            )
            embed.set_thumbnail(url=song_thumbnail)
            embed.add_field(name="**Duration**", value=f"{song_duration // 60}:{song_duration % 60}", inline=False)
            embed.add_field(name="**Artist**", value=song_artist, inline=False)
            embed.add_field(name="**Requested by**", value=ctx.author.display_name, inline=False)
            embed.add_field(name="**Requested at**", value=datetime.now().strftime('%H:%M:%S'), inline=False)
            embed.add_field(
                name="Enjoy the music!",
                value="Use the buttons below to control playback.",
                inline=False
            )
            embed.set_footer(text="Music Bot | Enjoy your time!", icon_url=ctx.author.avatar.url)

            # Send the embed with control buttons
            await ctx.send(embed=embed, view=ControlButtons(ctx, ctx.author))

        except Exception as e:
            print(f"Error while playing song: {e}")
            await ctx.send("An error occurred while playing the song.")

    @discord.app_commands.command(name="play", description="Play a song from a URL")
    async def play(self, interaction: discord.Interaction, url: str):
        ctx = await self.bot.get_context(interaction)

        # Acknowledge the interaction immediately
        await interaction.response.defer(thinking=True)

        # Check if the user is in a voice channel
        if not interaction.user.voice:
            await interaction.followup.send("You need to be in a voice channel to play music.", ephemeral=True)
            return
        
        # Check if a different user is controlling the music session
        controlling_user = active_users.get(ctx.guild.id)
        if controlling_user and controlling_user != interaction.user.id:
            await interaction.followup.send(
                "This music session is currently being controlled by another user. Please wait or join a different voice channel.",
                ephemeral=True
            )
            return

        # Set the user who controls the music session
        active_users[ctx.guild.id] = interaction.user.id

        if ctx.voice_client is None:
            await interaction.user.voice.channel.connect()

        if ctx.voice_client.is_playing():
            if ctx.guild.id not in queues:
                queues[ctx.guild.id] = []
            queues[ctx.guild.id].append(url)
            await interaction.followup.send("Added to the queue.")
        else:
            await self.play_song(ctx, url)

class ControlButtons(View):
    def __init__(self, ctx, controlling_user):
        super().__init__()
        self.ctx = ctx
        self.controlling_user = controlling_user

    @discord.ui.button(label="Play", style=discord.ButtonStyle.success)
    async def play_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.controlling_user.id:
            await interaction.response.send_message("You cannot control the music playback.", ephemeral=True)
            return

        if self.ctx.voice_client.is_paused():
            self.ctx.voice_client.resume()
        elif not self.ctx.voice_client.is_playing():
            await self.ctx.invoke(self.ctx.bot.get_command("play_next"))
        await interaction.response.defer()

    @discord.ui.button(label="Pause", style=discord.ButtonStyle.primary)
    async def pause_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.controlling_user.id:
            await interaction.response.send_message("You cannot control the music playback.", ephemeral=True)
            return

        if self.ctx.voice_client.is_playing():
            self.ctx.voice_client.pause()
        await interaction.response.defer()

    @discord.ui.button(label="Skip", style=discord.ButtonStyle.secondary)
    async def skip_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.controlling_user.id:
            await interaction.response.send_message("You cannot control the music playback.", ephemeral=True)
            return

        if self.ctx.voice_client.is_playing():
            self.ctx.voice_client.stop()
        await interaction.response.defer()

    @discord.ui.button(label="Stop", style=discord.ButtonStyle.danger)
    async def stop_button(self, interaction: discord.Interaction, button: Button):
        if interaction.user.id != self.controlling_user.id:
            await interaction.response.send_message("Only the user who started the session can stop it.", ephemeral=True)
            return

        if self.ctx.voice_client:
            queues.pop(self.ctx.guild.id, None)
            active_users.pop(self.ctx.guild.id, None)
            await self.ctx.voice_client.disconnect()
        await interaction.response.defer()

# Setup the cog in the main bot file
async def setup(bot: Seemu):
    await bot.add_cog(MusicNexx(bot))
