# Import Packages
from asyncio import sleep
import os

from dotenv import load_dotenv
from discord.ext import commands

# Load environment variables
load_dotenv()
guild_id = int(os.getenv("GUILD_ID"))
rgb_role_id = int(os.getenv("RGB_ROLE_ID"))

# Display role separately (Set this value to False if you don't want the role to be displayed separately)
hoist = True


# Create cog class
class Colours(commands.Cog):
    # Initialize class
    def __init__(self, client):
        self.client = client

    # Start changing role colour every 3 minutes
    # NOTE: CHANGING ROLE COLOUR FASTER THAN 180 SECONDS WILL RATE LIMIT THE BOT AND IT WILL BE BLOCKED BY DISCORD
    @commands.Cog.listener()
    async def on_ready(self):
        # Fetch role
        rgb_role = self.client.get_guild(guild_id).get_role(rgb_role_id)

        # Adding colours
        colours = [
            0x9fe3fe, 0x9cd0ff, 0x9dbefe, 0x9db6ff, 0xb0affd, 0xbca0f7, 0xd49eff, 0xdf9aff, 0xdf9aff, 0xf49cd3,
            0xfc9ec9, 0xfdacb1, 0xf9ada0, 0xffb3a6, 0xf6c99b, 0xfceaa7, 0xf7fca8, 0xe4fba5, 0xd3ffa3, 0xc4f8ab,
            0xcdffae, 0xbfffc3, 0xb2fedb]

        # Changing role colour in forever loop
        while True:
            for colour in colours:
                await rgb_role.edit(colour=colour, hoist=hoist)
                await sleep(180)


# Setup cog
def setup(client):
    client.add_cog(Colours(client))
