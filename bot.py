import asyncio
import configparser
import discord
from aio_timers import Timer

config = configparser.ConfigParser()
config.read('config.cfg')

TOKEN = config.get('discord_values', 'TOKEN')
AUTHOR_ID = config.get('discord_values', 'AUTHOR_ID')
END_TIMEOUT = config.get('config', 'END_TIMEOUT')
POLL_TIMOUT = config.get('config', 'POLL_TIMOUT')
MINUTES = config.get('config', 'MINUTES')

class AmongUsBot(discord.Client):
    async def on_ready(self):
        """
        Sets up the bots commands dictionary
        """
        print(f'{self.user} has joined')
        self.commands = {
            'mute': self.mute,
            'unmute': self.unmute,
        }
        self.muted = False
        self.end_timer = None
        # self.poll_timer = None

    async def on_message(self, message):
        """
        Call the corresponding command given by the Author

        :param message: Message sent in the discord server
        """
        print(f"message recieved - {message.content}")
        if message.content.startswith('!') and str(message.author.id) == AUTHOR_ID:
            command = message.content[1:]
            await self.commands[command](message.channel)

    async def mute(self, channel):
        """
        Mutes everyone in the voice channel
        Creates a timer in case no one is able to unmute everyone back

        :param channel: The channel the Author is currently in
        """
        print(f'Muting everyone in {channel}')
        self.muted = True
        await self.change_vc_permissions(channel)
        # await self.poll_timer_callback(channel)
        await self.end_timer_callback(channel)

    async def unmute(self, channel):
        """
        Unmutes everyone in the voice channel

        :param channel: The channel the author is currently in
        """
        print(f'Unmuting everyone in {channel}')
        # self.muted = False
        await self.change_vc_permissions(channel, False)
        self.end_timer.cancel()
        # self.poll_timer.cancel()

    # async def poll_timer_callback(self, channel):
    #     """
    #     Regulary checks whether everyone in the vc should be muted
    #     :param channel: The voice channel the author is in
    #     """
    #     if self.muted:
    #         await self.change_vc_permissions(channel)
    #         self.poll_timer = Timer(POLL_TIMOUT * MINUTES, self.poll_timer_callback, callback_args=(channel,))

    async def end_timer_callback(self, channel):
        """
        Regulary checks whether everyone in the vc should be muted
        :param channel: The voice channel the author is in
        """
        self.end_timer = Timer(END_TIMEOUT * MINUTES,
                               self.unmute, callback_args=(channel,))

    async def change_vc_permissions(self, channel, mute=True):
        for member in channel.members:
            print(member)
            await member.edit(mute=mute)

    async def on_group_join(self, channel, user):
        print(f'channel:{channel}, user: {user}')


client = AmongUsBot()
client.run(TOKEN)
