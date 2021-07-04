import requests
import os

import discord
from crypto import CoinMarketCrypto


TOKEN = os.getenv("DISCORD_TOKEN")
CRYPTO_KEY = os.getenv("CRYPTO_KEY")
CRYPTO_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'


class CryptoInfo:
    def __init__(self, crypto, min=1, max=5000, currency='USD', url=CRYPTO_URL):
        self.crypto = crypto.lower()
        self.F = CoinMarketCrypto(min, max, currency, url)
        self.data = self.F.quote[self.crypto]


class RenderPrices(discord.Client):
    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.content.startswith("!") and message.author.id != self.user.id:
            crypto_symbol = message.content[1:]
            try:
                # value = CoinMarketCrypto(crypto_symbol)
                print("Here is your message")
                value = CryptoInfo(crypto_symbol)
                await message.reply("The price for '%s' is $%f!" %(crypto_symbol.lower(), value.info), mention_author=True)
            except Exception as e:
                await message.reply("I'm sorry, but your input led to this exception: \t%s.\n\n" %(e))
                


client = RenderPrices()
client.run(TOKEN)
    





