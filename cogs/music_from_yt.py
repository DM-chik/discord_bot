import asyncio

import disnake
import yt_dlp.utils
from disnake.ext import commands
from disnake import ApplicationCommandInteraction

ffmpeg_path = "E:\\ffmpeg-7.1.1-essentials_build\\bin\\ffmpeg.exe"

ytdl_format_options = {
    'format': 'bestaudio/best',
    'extract_flat': 'in_playlist',
    'quiet': False,
    'no_warnings': True,
    'source_address': '0.0.0.0',
    'nocheckcertificate': True,
}
ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -threads 4 -ac 2 -b:a 96k'
}
ytdl = yt_dlp.YoutubeDL(ytdl_format_options)


class MusicQueue:
    def __init__(self):
        self.queue = []
        self.lock = asyncio.Lock()

    def add(self, items):
        self.queue.extend(items)

    def next(self):
        return self.queue.pop(0) if self.queue else None


class Music_from_yt(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.queues = {}
        self.current = {}

    def get_queue(self, guild_id):
        if guild_id not in self.queues:
            self.queues[guild_id] = MusicQueue()
        return self.queues[guild_id]

    async def play_next(self, inter, error=None):
        if error:
            print(f'Ошибка: {error}')
        queue = self.get_queue(inter.guild_id)
        if not queue.queue:
            return
        next_track = queue.next()
        if not next_track:
            return
        voice_client = inter.guild.voice_client
        if voice_client is None:
            return
        try:
            loop = self.bot.loop
            info = await loop.run_in_executor(None, ytdl.extract_info, next_track['url'], False)
            if 'entries' in info:
                info = info['entries'][0]
            else:
                print('Пустой плейлист')
            source = await disnake.FFmpegOpusAudio.from_probe(info['url'], **ffmpeg_options, executable=ffmpeg_path)
            self.current[inter.guild_id] = next_track
            voice_client.play(source, after=lambda e: self.bot.loop.create_task(self.play_next(inter, e)))
            channel = inter.channel.id
            await channel.send(f"▶️Сейчас играет: **{next_track['title']}**")
        except Exception as err:
            print(f'Ошибка воспроизведения: {err}')
            await self.play_next(inter)

    @commands.slash_command()
    async def play(self, inter: ApplicationCommandInteraction, url: str):
        await inter.response.defer()
        voice_client = inter.guild.voice_client
        if not voice_client:
            if inter.user.voice:
                voice_client = await inter.author.voice.channel.connect()
            else:
                return await inter.response.send_message("Вы не в голосовом канале!", ephemeral=True)
        try:
            loop = self.bot.loop
            data = await loop.run_in_executor(None, ytdl.extract_info, url, False)
        except Exception as err:
            return await inter.edit_original_response(f"🚫 Ошибка загрузки: {str(err)}")
        queue = self.get_queue(inter.guild_id)
        tracks = []
        if 'entries' in data:
            for entry in data['entries']:
                tracks.append({
                    'url': entry['url'],
                    'title': entry.get('title', 'Unknown Track'),
                })
            queue.add(tracks)
            await inter.edit_original_response(f"🎵 Добавлено **{len(tracks)}** треков в очередь!")
        else:
            track = {
                'url': url,
                'title': data.get('title', 'Unknown Track')
            }
            queue.add([track])
            await inter.edit_original_response(f"🎵 Добавлено в очередь: **{track['title']}**")
        if not voice_client.is_playing():
            await self.play_next(inter)


def setup(bot: commands.Bot):
    bot.add_cog(Music_from_yt(bot))
