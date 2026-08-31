import discord
from discord.ext import commands
from datetime import timedelta
import asyncio

# إعداد صلاحيات البوت الأساسية
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

# قاموس لتتبع رسائل الأعضاء ومنع السبام
user_messages = {}

@bot.event
async def on_ready():
    print(f"تم تشغيل بوت الحماية بنجاح: {bot.user.name}")

@bot.event
async def on_message(message):
    # تجاهل رسائل البوتات والأعضاء المشرفين
    if message.author.bot or message.author.guild_permissions.manage_messages:
        await bot.process_commands(message)
        return

    user_id = message.author.id
    current_time = message.created_at

    if user_id not in user_messages:
        user_messages[user_id] = []

    # تسجيل وقت الرسالة الحالية وتنظيف الرسائل القديمة (التي مرت عليها أكثر من 5 ثوانٍ)
    user_messages[user_id].append(current_time)
    user_messages[user_id] = [t for t in user_messages[user_id] if (current_time - t).total_seconds() < 5]

    # إذا أرسل العضو أكثر من 5 رسائل خلال 5 ثوانٍ يتم معاقبته بميوت تلقائي
    if len(user_messages[user_id]) > 5:
        try:
            # تطبيق ميوت تلقائي (Timeout) لمدة 10 دقائق
            await message.author.timeout(timedelta(minutes=10), reason="إرسال رسائل مزعجة متكررة (سبام)")
            # حذف آخر رسائل السبام في القناة
            await message.channel.purge(limit=5, check=lambda m: m.author == message.author)
            await message.channel.send(f"⚠️ {message.author.mention} تم إعطاؤك ميوت تلقائي لمدة 10 دقائق بسبب السبام!")
        except Exception as e:
            print(f"حدث خطأ أثناء محاولة إعطاء الميوت: {e}")
        return

    await bot.process_commands(message)

# أمر ميوت يدوي للمشرفين
@bot.command()
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, minutes: int = 10, *, reason="غير محدد"):
    try:
        await member.timeout(timedelta(minutes=minutes), reason=reason)
        await ctx.send(f"🔒 تم إعطاء ميوت للعضو {member.mention} لمدة {minutes} دقيقة. السبب: {reason}")
    except Exception as e:
        await ctx.send("❌ لا أملك صلاحية لإعطاء هذا العضو ميوت (تأكد من رفع رتبة البوت فوق رتبة العضو في الإعدادات).")

# أمر فك الميوت يدوي للمشرفين
@bot.command()
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    try:
        await member.timeout(None)
        await ctx.send(f"🔓 تم فك الميوت عن {member.mention} بنجاح.")
    except Exception as e:
        await ctx.send("❌ تعذر فك الميوت عن هذا العضو.")

# ⚠️ ضع التوكن السري الخاص ببوتك هنا بين علامتي التنصيص
bot.run("MTU0NDAzOTQ1MjgxNTY1NDkzNA.GzZjyM.kM-9rJbZz7pGkrt-cnh7AUvhrd8hzpUaEkJVMM")
