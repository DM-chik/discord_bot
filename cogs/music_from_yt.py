import disnake
import yt_dlp.utils
from disnake.ext import commands
from disnake import ApplicationCommandInteraction

ffmpeg_path = "E:\\ffmpeg-7.1.1-essentials_build\\bin\\ffmpeg.exe"

ytdl_format_options = {
    'format': 'bestaudio/best',
    'nonplaylist': True,
    'quiet': True,
}
ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}
ytdl = yt_dlp.YoutubeDL(ytdl_format_options)


class Music_from_yt(commands.Cog):
    def __init__(self, bot: commands.Bot):
        bot.self = bot

    @commands.slash_command()
    async def play(self, inter: ApplicationCommandInteraction, url: str):
        await inter.response.defer()
        voice_client = inter.guild.voice_client
        if not voice_client:
            if inter.author.voice:
                voice_client = await inter.author.voice.channel.connect()
            else:
                await inter.response.send_message("Вы не в голосовом канале!", ephemeral=True)
                return
        info = ytdl.extract_info(url, download=False)
        url2 = info['url']
        title = info.get('title', 'Музыка')
        source = await disnake.FFmpegOpusAudio.from_probe(url2, **ffmpeg_options, executable=ffmpeg_path)
        try:
            voice_client.play(source, after=lambda e: print(f'Закончил воспроизведение {title}'))
            await inter.edit_original_response(f'Воспроизведение {title}')
        except Exception as k:
            await inter.response.send_message(f'Ошибка воспроизведения: {k}')


def setup(bot: commands.Bot):
    bot.add_cog(Music_from_yt(bot))
