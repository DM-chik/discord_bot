import disnake
import os
from dotenv import load_dotenv
from disnake.ext import commands

load_dotenv()
intents = disnake.Intents.all()
bot = commands.Bot(command_prefix="!", test_guilds=[867424312897306676], intents=intents)
bot_token = os.getenv("bot_token")

cogs_list = []
for i in os.listdir("cogs"):
    cogs_list.append(i[:-3])
cogs_list.remove("__pycach")
for i in cogs_list:
    bot.load_extension(f'cogs.{i}')


@bot.event
async def on_ready():
    print(f"Бот {bot.user} готов!")


@bot.event
async def on_member_join(member):
    role = await disnake.utils.get(id_guild=867424312897306676, role_id=1278589046116978761)
    channel = bot.get_channel(867424313408618507)
    embed = disnake.Embed(
        title="Новый участник",
        description=f"{member.name}",
        color=0xffffff
    )
    await member.add_role(role)
    await channel.send(embed=embed)


bot.run(bot_token)
