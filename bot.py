import asyncio

import discord
from aio_timers import Timer

TOKEN = 'NzUwNzc2NjA2NjE5OTkyMDk2.X0_dMw.1uSAnxF-fOkQ6fFhOIR5mpovpTs'
AUTHOR_ID = 272355597524140034
END_TIMEOUT = 5
POLL_TIMOUT = 1
MINUTES = 5


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
        if message.content.startswith('!') and message.author.id == AUTHOR_ID:
            command = message.content[1:]
            await self.commands[command](message.author.voice.channel)

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
        self.end_timer = Timer(END_TIMEOUT * MINUTES, self.unmute, callback_args=(channel,))

    async def change_vc_permissions(self, channel, mute=True):
        for member in channel.members:
            await member.edit(mute=mute)

    async def on_group_join(self, channel, user):
        print(f'channel:{channel}, user: {user}')


client = AmongUsBot()
client.run(TOKEN)
