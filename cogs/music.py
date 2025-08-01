from disnake.ext import commands
from disnake import ClientException
from disnake import ApplicationCommandInteraction
from disnake import FFmpegOpusAudio

ffmpeg_path = "E:\\ffmpeg-7.1.1-essentials_build\\bin\\ffmpeg.exe"


class Music(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command()
    async def hello(self, inter):
        await inter.response.send_message('Хуй соси')

    # удаление запрещённых слов
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author != self.bot.user:
            for i in message.content.split():
                for j in open('bad_words', encoding="utf-8"):
                    if j.lower()[:-1] == i.lower():
                        await message.delete()
                        return await message.channel.send(f'{message.author.mention} долбаёб')

    @commands.slash_command()
    async def ping(self, inter):
        await inter.response.send_message(f'Понг! {round(self.bot.latency) * 1000}мс')

    @commands.slash_command()
    async def play_file(self, inter: ApplicationCommandInteraction, audio_file: str):
        if inter.author.voice is None:
            return await inter.response.send_message('Вы не находитесь в голосовом канале', ephemeral=True)
        channel = inter.author.voice.channel
        voice_client = inter.guild.voice_client
        if voice_client is None:
            try:
                voice_client = await channel.connect()
            except ClientException as e:
                return await inter.response.send_message(f'Ошибка подключения: {e}', ephemeral=True)
            except Exception as e:
                return await inter.response.send_message(f'Неизвестная ошибка подключения: {e}', ephemeral=True)
        if voice_client.channel != channel:
            return await inter.response.send_message('Я уже подключен к другому голосовому каналу', ephemeral=True)
        try:
            with open('sounds/' + audio_file, 'rb'):
                pass
        except FileNotFoundError:
            return await inter.response.send_message(f'Файл {audio_file} не найден', ephemeral=True)
        try:
            if voice_client.is_playing():
                voice_client.stop()
            audio_source = FFmpegOpusAudio('sounds/' + audio_file, executable=ffmpeg_path)
            voice_client.play(audio_source)
            await inter.response.send_message('Звуковой файл воспроизводиться', ephemeral=True)
        except Exception as e:
            await inter.response.send_message(f'Ошибка воспроизведения: {e}', ephemeral=True)

    @commands.slash_command()
    async def stop_playing(self, inter: ApplicationCommandInteraction):
        voice_client = inter.guild.voice_client
        if inter.author.voice is None:
            return await inter.response.send_message('Вы не находитесь в голосовом канале', ephemeral=True)
        if voice_client is None:
            return await inter.response.send_message('Бот не находится в голосовом канале', ephemeral=True)
        if inter.author.voice.channel != voice_client.channel:
            return await inter.response.send_message('Бот не находится в вашем голосовом канале', ephemeral=True)
        try:
            if voice_client.is_playing():
                voice_client.stop()
                await inter.response.send_message('Конец воспроизведения', ephemeral=True)
                return
            else:
                await inter.response.send_message('Сейчас ничего не играет', ephemeral=True)
                return
        except Exception as e:
            await inter.response.send_message(f'Ошибка остановки: {e}', ephemeral=True)
            return

    # калькулятор
    @commands.slash_command()
    async def score(self, inter, condition):
        await inter.response.send_message(eval(condition))


def setup(bot: commands.Bot):
    bot.add_cog(Music(bot))

