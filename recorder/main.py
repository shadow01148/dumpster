import time
import aiocsv
import aiofiles
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='>', self_bot=True)
ID = 788246385988337664
whitelist = [1124441110517907619, 406995309000916993]

@bot.event
async def on_message(message):
    if isinstance(message.channel, discord.DMChannel):
        return
    if message.guild.id not in whitelist:
        return
    if message.embeds:
        return
    
    UNIX = int(time.time())

    author = message.author.name
    content = message.clean_content or "N/A"
    channel = message.channel.name
    channel_id = message.channel.id

    if isinstance(message.channel, discord.Thread):
        channel = "[FORUM] " + message.channel.name
    if isinstance(message.channel, discord.TextChannel):
        channel = "[CHANNEL]" + message.channel.name

    async with aiofiles.open(f"{message.guild.id}.csv", "a+", encoding="utf-8", newline="") as f:
        writer = aiocsv.AsyncWriter(f)
        if message.attachments:
            attachment = message.attachments[0].proxy_url
            data = [f"{channel}", f"{author}", f"{content}", f"{attachment}", f"{channel_id}", f"{UNIX}"]
            await writer.writerow(data)
        else:
            data = [f"{channel}", f"{author}", f"{content}", "N/A", f"{channel_id}", f"{UNIX}"]
            await writer.writerow(data)

@bot.event
async def on_message_delete(message):
    if isinstance(message.channel, discord.DMChannel):
        return
    if message.guild.id not in whitelist:
        return
    if message.embeds:
        return
    
    UNIX = int(time.time())

    author = message.author.name
    content = message.clean_content or "N/A"
    channel = message.channel.name
    channel_id = message.channel.id
    is_deleted = True

    if isinstance(message.channel, discord.Thread):
        channel = "[FORUM] " + message.channel.name
    if isinstance(message.channel, discord.TextChannel):
        channel = "[CHANNEL]" + message.channel.name

    async with aiofiles.open(f"{message.guild.id}.csv", "a+", encoding="utf-8", newline="") as f:
        writer = aiocsv.AsyncWriter(f)
        if message.attachments:
            attachment = message.attachments[0].proxy_url
            data = [f"{channel}", f"{author}", f"{content}", f"{attachment}", f"{channel_id}", f"{UNIX}", f"{is_deleted}"]
            await writer.writerow(data)
        else:
            data = [f"{channel}", f"{author}", f"{content}", "N/A", f"{channel_id}", f"{UNIX}", f"{is_deleted}"]
            await writer.writerow(data)


@bot.event
async def on_message_edit(before, after):
    if isinstance(before.channel, discord.DMChannel):
        return
    if before.guild.id not in whitelist:
        return
    if before.embeds or after.embeds:
        return
    UNIX = int(time.time())

    author = before.author.name
    before_content = before.clean_content or "N/A"
    after_content = after.clean_content or "N/A"
    channel = before.channel.name
    channel_id = before.channel.id

    is_edited = True

    if isinstance(before.channel, discord.Thread):
        channel = "[FORUM] " + before.channel.name
    if isinstance(before.channel, discord.TextChannel):
        channel = "[CHANNEL] " + before.channel.name

    async with aiofiles.open(f"{before.guild.id}.csv", "a+", encoding="utf-8", newline="") as f:
        writer = aiocsv.AsyncWriter(f)
        if before.attachments:
            attachment = before.attachments[0].proxy_url
            data = [f"{channel}", f"{author}", f"{before_content} --> {after_content}", f"{attachment}", f"{channel_id}", f"{UNIX}", f"{is_edited}"]
            await writer.writerow(data)
        else:
            data = [f"{channel}", f"{author}", f"{before_content} --> {after_content}", "N/A", f"{channel_id}", f"{UNIX}", f"{is_edited}"]
            await writer.writerow(data)


bot.run('TOKEN')
