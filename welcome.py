import discord

TOKEN = os.getenv("DISCORD_TOKEN")



class Welcome(discord.Client):    
    async def on_ready(self):
        print("Hello! You're currently logged in as", self.user.name, self.user.id)
        print("-------")
    
    async def on_member_join(self, member):
        guild = member.guild
        if guild.system_channel is not None:
            to_send = "Welcome {0.mention} to {1.name}! I am a bot that is erroneously named 'LATEX'".format(member, guild)
            await guild.system_channel.send(to_send)


client = Welcome()
client.run(TOKEN)