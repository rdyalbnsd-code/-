import discord
from discord.ext import commands
from datetime import timedelta

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
user_messages = {}

@bot.event
async def on_ready():
    print(f"تم تشغيل البوت بنجاح: {bot.user.name}")

@bot.event
async def on_message(message):
    if message.author.bot or message.author.guild_permissions.manage_messages:
        await bot.process_commands(message)
        return

    user_id = message.author.id
    current_time = message.created_at

    if user_id not in user_messages:
        user_messages[user_id] = []

    user_messages[user_id].append(current_time)
    user_messages[user_id] = [t for t in user_messages[user_id] if (current_time - t).total_seconds() < 5]

    if len(user_messages[user_id]) > 5:
        try:
            await message.author.timeout(timedelta(minutes=10), reason="السبام المتكرر")
            await message.channel.purge(limit=5, check=lambda m: m.author == message.author)
            await message.channel.send(f"⚠️ {message.author.mention} تم إعطاؤك ميوت تلقائي لمدة 10 دقائق بسبب السبام!")
        except:
            pass
        return

    await bot.process_commands(message)

# انتبه للسطر بالأسفل بدقة 👇
bot.run("MTU0NDAzOTQ1MjgxNTY1NDkzNA.G87fBY.kRV51h-PDlXEZEVyWTHjeHqh7aVpcQBK4LoRaI")
