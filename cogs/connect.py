from disnake.ext import commands
from disnake import ApplicationCommandInteraction
from disnake import ClientException
from disnake import VoiceChannel


class Connect(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # подключение бота
    @commands.slash_command()
    async def join(self, inter: ApplicationCommandInteraction, channel: VoiceChannel = None):
        if channel is None:
            if inter.author.voice:
                channel = inter.author.voice.channel
                await inter.response.send_message('Бот успешно подключился к голосовому каналу', ephemeral=True)
            else:
                await inter.response.send_messages('Вы не находитесь в голосовом канале', ephemeral=True)
        try:
            await channel.connect()
        except ClientException as e:
            await inter.response.send_message(f'Ошибка подключения {e}', ephemeral=True)
        except Exception as e:
            await inter.response.send_messages(f'Ошибка подключения {e}', ephemeral=True)

    # отключение бота
    @commands.slash_command()
    async def leave(self, inter: ApplicationCommandInteraction):
        voice_client = inter.guild.voice_client
        if self.bot.voice_clients:
            try:
                await voice_client.disconnect()
                await inter.response.send_message('Успешно отключился от голосового канала', ephemeral=True)
            except Exception as e:
                await inter.response.send_message(f'Ошибка отключения {e}', ephemeral=True)
        else:
            await inter.response.send_messages(f'Бот не подключён к голосовому каналу', ephemeral=True)


def setup(bot: commands.Bot):
    bot.add_cog(Connect(bot))