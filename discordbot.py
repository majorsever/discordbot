import discord
from discord.ext import commands
import json
import os
from threading import Thread
from flask import Flask

# ------------------- Intents -------------------
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ------------------- Roles -------------------
ROLE_LIST = [
    "Algebra",
    "Precalculus",
    "Calculus 1",
    "Calculus 2",
    "Calculus 3",
    "Linear Algebra",
    "ODE",
    "PDE",
    "Complex Variables",
    "Proof Writing",
    "Abstract Algebra",
    "Analysis",
    "Probability and Statistics",
    "Trigonometry"
]

EMOJI = "✅"  # Same emoji for all roles

# File to store message IDs
MESSAGE_STORE_FILE = "reaction_messages.json"

# Load stored message IDs if file exists
if os.path.exists(MESSAGE_STORE_FILE):
    with open(MESSAGE_STORE_FILE, "r") as f:
        MESSAGE_ROLE_MAP = json.load(f)
else:
    MESSAGE_ROLE_MAP = {}

# ------------------- Flask Web Server (for uptime) -------------------
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8000)

Thread(target=run).start()

# ------------------- Bot Events -------------------
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# Command to setup reaction-role messages
@bot.command()
@commands.has_permissions(administrator=True)
async def setupreaction(ctx):
    global MESSAGE_ROLE_MAP
    try:
        for role_name in ROLE_LIST:
            message = await ctx.send(f"React with {EMOJI} to get the **{role_name}** role!")
            await message.add_reaction(EMOJI)
            MESSAGE_ROLE_MAP[str(message.id)] = role_name

        # Save message IDs to file
        with open(MESSAGE_STORE_FILE, "w") as f:
            json.dump(MESSAGE_ROLE_MAP, f)

        await ctx.send("✅ Reaction role messages have been set up!")
    except Exception as e:
        await ctx.send(f"❌ Error: {e}")
        print(e)

# ------------------- Reaction Events -------------------
@bot.event
async def on_raw_reaction_add(payload):
    role_name = MESSAGE_ROLE_MAP.get(str(payload.message_id))
    if not role_name or str(payload.emoji) != EMOJI:
        return

    guild = bot.get_guild(payload.guild_id)
    role = discord.utils.get(guild.roles, name=role_name)
    member = guild.get_member(payload.user_id)
    if role and member:
        await member.add_roles(role)
        print(f"Gave {role.name} to {member.name}")

@bot.event
async def on_raw_reaction_remove(payload):
    role_name = MESSAGE_ROLE_MAP.get(str(payload.message_id))
    if not role_name or str(payload.emoji) != EMOJI:
        return

    guild = bot.get_guild(payload.guild_id)
    role = discord.utils.get(guild.roles, name=role_name)
    member = guild.get_member(payload.user_id)
    if role and member:
        await member.remove_roles(role)
        print(f"Removed {role.name} from {member.name}")

# ------------------- Run Bot -------------------
# Make sure your token is set as an environment variable:
# export TOKEN="YOUR_BOT_TOKEN" (Mac/Linux)
# set TOKEN="YOUR_BOT_TOKEN" (Windows)
bot.run(os.environ["TOKEN"])

# MTQyMDE2OTA2Nzc3NTUyOTA1MA.GbRUPy.sVCdqU_7XwNboq4fvzy3RLinQYJsCdJL7Yxc0s









