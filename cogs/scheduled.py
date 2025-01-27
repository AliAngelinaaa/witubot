import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime, timedelta

class ScheduledMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scheduled_messages = []  # List to hold scheduled messages

    @commands.command(name='schedule')
    async def schedule_message(self, ctx, time: str, *, message: str):
        """Schedule a message to be sent at a specific time (format: HH:MM)"""
        now = datetime.now()
        scheduled_time = datetime.strptime(time, "%H:%M").replace(year=now.year, month=now.month, day=now.day)

        if scheduled_time < now:
            scheduled_time += timedelta(days=1)  # Schedule for the next day if the time has already passed

        delay = (scheduled_time - now).total_seconds()
        self.scheduled_messages.append((ctx.channel.id, message, delay))
        await ctx.send(f"Message scheduled for {scheduled_time.strftime('%H:%M')}.")

    @tasks.loop(seconds=60)
    async def check_scheduled_messages(self):
        """Check for scheduled messages and send them"""
        now = datetime.now()
        for i, (channel_id, message, delay) in enumerate(self.scheduled_messages):
            if delay <= 0:
                channel = self.bot.get_channel(channel_id)
                if channel:
                    await channel.send(message)
                self.scheduled_messages.pop(i)  # Remove the message after sending
            else:
                self.scheduled_messages[i] = (channel_id, message, delay - 60)  # Update delay

    @commands.Cog.listener()
    async def on_ready(self):
        self.check_scheduled_messages.start()  # Start the task loop when the bot is ready

async def setup(bot):
    await bot.add_cog(ScheduledMessages(bot))
