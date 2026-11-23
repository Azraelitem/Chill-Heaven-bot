import os
import discord
from discord.ext import commands
from datetime import datetime, timezone

TOKEN = os.getenv("DISCORD_TOKEN")
LOG_CHANNEL_ID = int(os.getenv("LOG_CHANNEL_ID", "0"))

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

async def send_log(guild, title, description, color=discord.Color.blurple()):
    channel = guild.get_channel(LOG_CHANNEL_ID)
    if channel is None:
        return
    embed = discord.Embed(title=title, description=description, color=color,
                         timestamp=datetime.now(timezone.utc))
    embed.set_footer(text="Custom Admin Logs")
    try:
        await channel.send(embed=embed)
    except discord.Forbidden:
        print("Bot nie ma uprawnienia do wysyłania wiadomości w kanale logów.")

@bot.event
async def on_ready():
    print(f"Zalogowano jako {bot.user} ({bot.user.id})")

@bot.event
async def on_member_join(member):
    await send_log(member.guild, "📥 Dołączył użytkownik",
                   f"{member.mention} (`{member}` / ID: {member.id})")

@bot.event
async def on_member_remove(member):
    # Rozróżnienie kicka od wyjścia wymaga sprawdzenia Audit Log; na razie zapisujemy opuszczenie serwera.
    await send_log(member.guild, "📤 Użytkownik opuścił serwer",
                   f"{member} (ID: {member.id})")

@bot.event
async def on_member_ban(guild, user):
    await send_log(guild, "🔨 Ban",
                   f"Użytkownik: {user} (ID: {user.id})", discord.Color.red())

@bot.event
async def on_member_unban(guild, user):
    await send_log(guild, "🔓 Unban",
                   f"Użytkownik: {user} (ID: {user.id})", discord.Color.green())

@bot.event
async def on_member_update(before, after):
    changes = []
    if before.nick != after.nick:
        changes.append(f"Nick: `{before.nick}` → `{after.nick}`")
    if before.roles != after.roles:
        old = [r.name for r in before.roles if r.name != "@everyone"]
        new = [r.name for r in after.roles if r.name != "@everyone"]
        changes.append(f"Role przed: {', '.join(old) or 'brak'}\nRole po: {', '.join(new) or 'brak'}")
    if before.timed_out_until != after.timed_out_until:
        changes.append(f"Timeout do: {after.timed_out_until or 'zdjęty'}")
    if changes:
        await send_log(after.guild, "🛠️ Zmiana profilu/roli",
                       f"Użytkownik: {after.mention} (ID: {after.id})\n" + "\n".join(changes))

@bot.event
async def on_message_delete(message):
    if message.guild is None or message.author.bot:
        return
    content = message.content or "(brak tekstu / wiadomość zawierała załączniki)"
    await send_log(message.guild, "🗑️ Usunięto wiadomość",
                   f"Autor: {message.author} (ID: {message.author.id})\n"
                   f"Kanał: {message.channel.mention}\nTreść: {content[:1500]}",
                   discord.Color.orange())

@bot.event
async def on_message_edit(before, after):
    if before.guild is None or before.author.bot or before.content == after.content:
        return
    await send_log(before.guild, "✏️ Edytowano wiadomość",
                   f"Autor: {before.author} (ID: {before.author.id})\n"
                   f"Kanał: {before.channel.mention}\n"
                   f"Przed: {(before.content or '(pusto)')[:1000]}\n"
                   f"Po: {(after.content or '(pusto)')[:1000]}")

@bot.event
async def on_guild_channel_create(channel):
    await send_log(channel.guild, "➕ Utworzono kanał",
                   f"Kanał: {channel.mention} (ID: {channel.id})")

@bot.event
async def on_guild_channel_delete(channel):
    await send_log(channel.guild, "➖ Usunięto kanał",
                   f"Nazwa: {channel.name} (ID: {channel.id})", discord.Color.orange())

@bot.event
async def on_guild_channel_update(before, after):
    changes = []
    if before.name != after.name:
        changes.append(f"Nazwa: `{before.name}` → `{after.name}`")
    if getattr(before, "category", None) != getattr(after, "category", None):
        changes.append(f"Kategoria: {getattr(before.category, 'name', 'brak')} → {getattr(after.category, 'name', 'brak')}")
    if changes:
        await send_log(after.guild, "📝 Zmieniono kanał",
                      f"Kanał: {after.mention}\n" + "\n".join(changes))

if not TOKEN:
    raise SystemExit("Ustaw zmienną DISCORD_TOKEN (token bota) przed uruchomieniem.")
bot.run(TOKEN)
