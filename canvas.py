import discord
import asyncio
import random
import time
from PIL import Image

client = discord.Client()

colors = {
    "Amaranth":(229,43,80),
    "Amber":(255,191,0),
    "Amethyst":(153,102,204),
    "Apricot":(251,206,177),
    "Aquamarine":(127,255,212),
    "Azure":(0,127,255),
    "Baby blue":(137,207,240),
    "Beige":(245,245,220),
    "Black":(0,0,0),
    "Blue":(0,0,255),
    "Blue-green":(0,149,182),
    "Blue-violet":(138,43,226),
    "Blush":(222,93,131),
    "Bronze":(205,127,50),
    "Brown":(150,75,0),
    "Burgundy":(128,0,32),
    "Byzantium":(112,41,99),
    "Carmine":(150,0,24),
    "Cerise":(222,49,99),
    "Cerulean":(0,123,167),
    "Champagne":(247,231,206),
    "Chartreuse green":(127,255,0),
    "Chocolate":(123,63,0),
    "Cobalt blue":(0,71,171),
    "Coffee":(111,78,55),
    "Copper":(184,115,51),
    "Coral":(248,131,121),
    "Crimson":(220,20,60),
    "Cyan":(0,255,255),
    "Desert sand":(237,201,175),
    "Electric blue":(125,249,255),
    "Emerald":(80,200,120),
    "Erin":(0,255,63),
    "Gold":(255,215,0),
    "Gray":(128,128,128),
    "Green":(0,255,0),
    "Harlequin":(63,255,0),
    "Indigo":(75,0,130),
    "Ivory":(255,255,240),
    "Jade":(0,168,107),
    "Jungle green":(41,171,135),
    "Lavender":(181,126,220),
    "Lemon":(255,247,0),
    "Lilac":(200,162,200),
    "Lime":(191,255,0),
    "Magenta":(255,0,255),
    "Magenta rose":(255,0,175),
    "Maroon":(128,0,0),
    "Mauve":(224,176,255),
    "Navy blue":(0,0,128),
    "Ocher":(204,119,34),
    "Olive":(128,128,0),
    "Orange":(255,165,0),
    "Orange-red":(255,69,0),
    "Orchid":(218,112,214),
    "Peach":(255,229,180),
    "Pear":(209,226,49),
    "Periwinkle":(204,204,255),
    "Persian blue":(28,57,187),
    "Pink":(255,192,203),
    "Plum":(142,69,133),
    "Prussian blue":(0,49,83),
    "Puce":(204,136,153),
    "Purple":(128,0,128),
    "Raspberry":(227,11,92),
    "Red":(255,0,0),
    "Red-violet":(199,21,133),
    "Rose":(255,0,127),
    "Ruby":(224,17,95),
    "Salmon":(250,128,114),
    "Sangria":(146,0,10),
    "Sapphire":(15,82,186),
    "Scarlet":(255,36,0),
    "Silver":(192,192,192),
    "Slate gray":(112,128,144),
    "Spring bud":(167,252,0),
    "Spring green":(0,255,127),
    "Tan":(210,191,140),
    "Taupe":(72,60,50),
    "Teal":(0,128,128),
    "Turquoise":(64,224,208),
    "Violet":(238,130,238),
    "Viridian":(64,130,109),
    "White":(255,255,255),
    "Yellow":(255,255,0),
    "Blurple":(114,137,218),
}


"""
def pixel(numbers):
    try:
        data = numbers.split(" ")

        class properties:
            faulty = True
            if len(data) == 3:
                if data[2].lower() == "random":
                    r, g, b = colors[random.choice(list(colors))]
                for x in colors.keys():
                    if data[2].lower() == x.lower().replace(" ", "-"):

                        r, g, b = colors[x]

                        break
            else:
                r = int(data[2])
                g = int(data[3])
                b = int(data[4])
            faulty = False


            x = int(data[0])
            y = int(data[1])

        if properties.r > 256 or properties.g > 256 or properties.b > 256 or properties.x > 99 or properties.y > 99:
            properties.faulty = True
        else:
            properties.faulty = False
    except:
        try: properties.faulty = True
        except: return None

    return properties
"""

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
            for x in colors.keys():
                if x.lower().replace(" ", "-") == data[2]:
                    self.rgb = colors[x]
            if self.rgb == None:
                self.faulty = True
                pass
        elif len(data) == 5:
            self.rgb = int(data[2]), int(data[3]), int(data[4])
            if not (self.rgb[0] in range(256) or self.rgb[1] in range(256) or self.rgb[2] in range(256)):
                self.faulty = True
                pass
        else:
            self.faulty = True
            pass


def isnotbot(m):
    return not m.author == client.user

@client.event
async def on_ready():
    print("Logged in")

colorlist = ""
for x in colors.keys():
    colorlist += x.replace(" ", "-").lower()+"\n"

times = []

@client.event
async def on_message(message):
    print(message.content)

    if isnotbot(message):
        if "view colors" in message.content.lower():
            colorlist = ""
            for x in colors.keys():
                colorlist += "\n"+x.replace(" ", "-").lower()
            await client.send_message(message.author, "List of avaliable colors:" + colorlist)
        if "view canvas" in message.content.lower():
            with open('canvasupscaled.png', 'rb') as f:
                await client.send_file(message.channel, f)
        if message.content.lower().startswith("p "):
            t1 = time.time()
            canvas = Image.open("canvas.png")
            pixeldata = Pixel(message.content)
            if pixeldata.faulty:
                await client.send_message(message.channel, message.author.mention + " Invalid pixel. Check how many spaces you have. X and Y must be below 99 (between and including 0 and 99), colors must contain no spaces and must be valid.")
            else:
                canvas.putpixel(pixeldata.xy, pixeldata.rgb)
                canvas.save('canvas.png')
                canvasupscaled = canvas.resize((1000, 1000), Image.NEAREST)

                canvasupscaled.save('canvasupscaled.png')

                with open('canvasupscaled.png', 'rb') as f:
                    await client.send_file(message.channel, f)
            t2 = time.time()
            print("Time took:",t2-t1)
            times.append(t2-t1)
        if str(message.author) == "SoopaKhell#5097":
            if message.content.lower().startswith("getavgtime"):
                await client.send_message(message.channel, sum(times)/len(times))


with open("key.txt") as f:
    client.run(f.read())
