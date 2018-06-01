import discord
import asyncio
import random
import time
from PIL import Image



colors = {
    "amaranth":(229, 43, 80),
    "amber":(255, 191, 0),
    "amethyst":(153, 102, 204),
    "apricot":(251, 206, 177),
    "aquamarine":(127, 255, 212),
    "azure":(0, 127, 255),
    "baby-blue":(137, 207, 240),
    "beige":(245, 245, 220),
    "black":(0, 0, 0),
    "blue":(0, 0, 255),
    "blue-green":(0, 149, 182),
    "blue-violet":(138, 43, 226),
    "blush":(222, 93, 131),
    "bronze":(205, 127, 50),
    "brown":(150, 75, 0),
    "burgundy":(128, 0, 32),
    "byzantium":(112, 41, 99),
    "carmine":(150, 0, 24),
    "cerise":(222, 49, 99),
    "cerulean":(0, 123, 167),
    "champagne":(247, 231, 206),
    "chartreuse-green":(127, 255, 0),
    "chocolate":(123, 63, 0),
    "cobalt-blue":(0, 71, 171),
    "coffee":(111, 78, 55),
    "copper":(184, 115, 51),
    "coral":(248, 131, 121),
    "crimson":(220, 20, 60),
    "cyan":(0, 255, 255),
    "desert-sand":(237, 201, 175),
    "electric-blue":(125, 249, 255),
    "emerald":(80, 200, 120),
    "erin":(0, 255, 63),
    "gold":(255, 215, 0),
    "gray":(128, 128, 128),
    "green":(0, 255, 0),
    "harlequin":(63, 255, 0),
    "indigo":(75, 0, 130),
    "ivory":(255, 255, 240),
    "jade":(0, 168, 107),
    "jungle-green":(41, 171, 135),
    "lavender":(181, 126, 220),
    "lemon":(255, 247, 0),
    "lilac":(200, 162, 200),
    "lime":(191, 255, 0),
    "magenta":(255, 0, 255),
    "magenta-rose":(255, 0, 175),
    "maroon":(128, 0, 0),
    "mauve":(224, 176, 255),
    "navy-blue":(0, 0, 128),
    "ocher":(204, 119, 34),
    "olive":(128, 128, 0),
    "orange":(255, 165, 0),
    "orange-red":(255, 69, 0),
    "orchid":(218, 112, 214),
    "peach":(255, 229, 180),
    "pear":(209, 226, 49),
    "periwinkle":(204, 204, 255),
    "persian-blue":(28, 57, 187),
    "pink":(255, 192, 203),
    "plum":(142, 69, 133),
    "prussian-blue":(0, 49, 83),
    "puce":(204, 136, 153),
    "purple":(128, 0, 128),
    "raspberry":(227, 11, 92),
    "red":(255, 0, 0),
    "red-violet":(199, 21, 133),
    "rose":(255, 0, 127),
    "ruby":(224, 17, 95),
    "salmon":(250, 128, 114),
    "sangria":(146, 0, 10),
    "sapphire":(15, 82, 186),
    "scarlet":(255, 36, 0),
    "silver":(192, 192, 192),
    "slate-gray":(112, 128, 144),
    "spring-bud":(167, 252, 0),
    "spring-green":(0, 255, 127),
    "tan":(210, 191, 140),
    "taupe":(72, 60, 50),
    "teal":(0, 128, 128),
    "turquoise":(64, 224, 208),
    "violet":(238, 130, 238),
    "viridian":(64, 130, 109),
    "white":(255, 255, 255),
    "yellow":(255, 255, 0),
    "blurple":(114, 137, 218)
}


class Pixel:
    def __init__(self, msg):
        self.faulty = False
        self.rgb = None

        data = msg.lower().strip("p ").split(" ")
        self.xy = int(data[0]), int(data[1])
        if len(data) == 3:
            if not (self.xy[0] in range(100) or self.xy[1] in range(100)):
                self.faulty = True
                pass
            try: self.rgb = colors[data[2].lower()]
            except KeyError: self.faulty = True
        elif len(data) == 5:
            self.rgb = int(data[2]), int(data[3]), int(data[4])
            if not (self.rgb[0] in range(256) or self.rgb[1] in range(256) or self.rgb[2] in range(256)):
                self.faulty = True
                pass
        else:
            self.faulty = True
            pass


client = discord.Client()

@client.event
async def on_ready():
    print("====================== Ready ======================")

@client.event
async def on_message(message):
    if message.author != client.user:
        print(message.content)
        if message.content.lower().startswith("p "):
            pixeldata = Pixel(message.content)
            if pixeldata.faulty:
                await client.send_message(message.channel, message.author.mention + " Invalid pixel. Check how many spaces you have. X and Y must be below 99 (between and including 0 and 99), colors must contain no spaces and must be valid.")
            else:
                canvasim = Image.open("canvas.png")
                #canvasim = canvasim.convert("RGB")#Re-Enable if you get the too many arguments error
                canvas = canvasim.load()
                canvas[pixeldata.xy[0],pixeldata.xy[1]] = pixeldata.rgb
                canvasim.save("canvas.png")
                canvasim.resize((1000,1000), Image.NEAREST).save("canvasupscaled.png")
                with open('canvasupscaled.png', 'rb') as f:
                    await client.send_file(message.channel, f)
        elif "view colors" in message.content.lower():
            colorlist = ""
            for x in colors.keys():
                colorlist += "\n"+x.replace(" ", "-").lower()
            await client.send_message(message.author, "List of avaliable colors:" + colorlist)
        elif "view canvas" in message.content.lower():
            with open('canvasupscaled.png', 'rb') as f:
                await client.send_file(message.channel, f)

        elif str(message.author) in open("admins.txt").read():
            #Only run these commands if an admin said them
            pass


with open("key.txt") as f:
    client.run(f.read())
