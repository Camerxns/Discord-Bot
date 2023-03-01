import discord
import os
import json

if not os.path.exists("users.json"):
    with open("users.json", "w") as f:
        json.dump({}, f)

filename = "users.json"

if not os.path.exists(filename):
    with open(filename, "w") as f:
        json.dump({}, f)

with open(filename, "r") as f:
    users = json.load(f)

with open(filename, "w") as f:
    json.dump(users, f)


from dotenv import load_dotenv
load_dotenv()

with open("config.json", "r") as f:
    config = json.load(f)

my_secret = config["Token"]
print(my_secret)

from discord.ext import commands

client = commands.Bot(command_prefix='!',
intents=discord.Intents.all())

async def update_data(users, user):
    if not user.id in users:
        users[user.id] = {}
        users[user.id]["xp"] = 0
        users[user.id]["level"] = 1
    users[user.id]["xp"] += 1
    
    if users[user.id]["xp"] >= 5:
        users[user.id]["level"] += 1
        users[user.id]["xp"] = 0
        return True
    else:
        return False


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    with open("users.json", "r") as f:
        global users
        users = json.load(f)

@client.command()
async def rank(ctx, *, member: discord.Member = None):
    member = member or ctx.author
    user_id = str(member.id)

    with open("users.json", "r") as f:
        users = json.load(f)

    if user_id not in users:
        await ctx.send(f"{member.name} has not sent any messages yet.")
        return

    await ctx.send(f"Rank: {users[user_id]['level']}\nXP: {users[user_id]['xp']}")
  
@client.event
async def on_message(message):
      print(f"[{message.channel}] {message.author}: {message.content}")
      if message.author == client.user:
        return
      user_id = str(message.author.id)
      if user_id not in users:
        users[user_id] = {"xp": 0, "level": 1}
      users[user_id]["xp"] += 1
      with open("users.json", "w") as f:
        json.dump(users, f)
      if message.content == '!hello':
        await message.channel.send('Hello!')
      elif message.content == '!greet':
        await message.channel.send('Hello! How are you doing?')
      elif message.content == '!rank':
        if user_id in users:
            await message.channel.send(f"Rank: {users[user_id]['level']}\nXP: {users[user_id]['xp']}")
        else:
            await message.channel.send(f"{message.author.name} has not sent any messages yet.")

@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    guild = client.get_guild(payload.guild_id)
    role = discord.utils.get(guild.roles, id=1071544045467353252)
    user = guild.get_member(payload.user_id)

    if message_id == 1074021048774832189:
        guild = client.get_guild(payload.guild_id)
        if guild.me.guild_permissions.manage_roles:
            if user.top_role < role:
                await user.add_roles(role)
            else:
                print("The user does not have permission to be assigned the role.")
        else:
            print("The bot does not have permission to manage roles.")
    else:
        print("The reaction was not added to the correct message or the emoji was incorrect.")

    print(f"Reaction added to message {message_id}")

client.run(my_secret)
