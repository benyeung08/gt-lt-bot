import discord
import json
import os

from discord import File
from discord.ext import commands
from typing import Optional
from PIL import ImageFont
from easy_pil import Editor, load_image_async

#if you want to give role to the user at any specific level upgrade then you can do like this
#enter the name of the role in a list
level = ["Level-5+", "Level-10+", "Level-15+"]

#add the level number at which you want to give the role
level_num = [5, 10, 15]

class Level(commands.Cog, description="等級系統"):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print("Leveling Cog Ready!")

  #this will increase the user's xp everytime they message
  @commands.Cog.listener()
  async def on_message(self, message):

    #the bot's prefix is ? that's why we are adding this statement so user's xp doesn't increase when they use any commands
    if not message.content.startswith("><"):

      #checking if the bot has not sent the message
      if not message.author.bot:
        with open("datas/levels.json", "r") as f:
          data = json.load(f)
        
        #checking if the user's data is already there in the file or not
        if str(message.author.id) in data:
          xp = data[str(message.author.id)]['xp']
          lvl = data[str(message.author.id)]['level']

          #increase the xp by the number which has 100 as its multiple
          increased_xp = xp+25
          new_level = int(increased_xp/100)

          data[str(message.author.id)]['xp']=increased_xp

          with open("datas/levels.json", "w") as f:
            json.dump(data, f)

          if new_level > lvl:
            try:
                await message.channel.send(f"{message.author.mention} 你升級到等級 {new_level} 了呢!!!")
            except:
                print(f"{message.author} 升級到等級 {new_level} 訊息傳送失敗")

            data[str(message.author.id)]['level']=new_level
            data[str(message.author.id)]['xp']=0

            with open("datas/levels.json", "w") as f:
              json.dump(data, f)
            try:
              for i in range(len(level)):
                if new_level == level_num[i]:

                  mbed = discord.Embed(title=f"嘿! {message.author.mention} 你達到等級 **{level[i]}** 了!", color = message.author.colour)
                  mbed.set_thumbnail(url=message.author.avatar_url)
                  await message.channel.send(embed=mbed)
            except:
                print(f"{message.author} 升級到等級 {new_level} 嵌入傳送失敗")
        else:
          data[str(message.author.id)] = {}
          data[str(message.author.id)]['xp'] = 0
          data[str(message.author.id)]['level'] = 1

          with open("datas/levels.json", "w") as f:
            json.dump(data, f)

  @commands.command(name="rank")
  async def rank(self, ctx: commands.Context, user: Optional[discord.Member]):
    """查看等級"""
    userr = user or ctx.author

    with open("datas/levels.json", "r") as f:
      data = json.load(f)

    try:
      xp = data[str(userr.id)]["xp"]
      lvl = data[str(userr.id)]["level"]

      next_level_xp = (lvl+1) * 100
      xp_need = next_level_xp
      xp_have = data[str(userr.id)]["xp"]

      percentage = int(((xp_have * 100)/ xp_need))

      if percentage < 1:
       percentage = 0
    
      ## Rank card
      background = Editor(f"images/levels/zIMAGE.png")
      profile = await load_image_async(str(userr.avatar_url))
 
      profile = Editor(profile).resize((150, 150)).circle_image()
    
      fonts_directory = os.path.join(os.path.dirname(__file__), "../fonts")
      fonts_path = {"msjh": os.path.join(fonts_directory, "msjh", "msjh.ttf"),}

      msjh = ImageFont.truetype(fonts_path["msjh"], size=40)
      msjh_small = ImageFont.truetype(fonts_path["msjh"], size=30)

      #you can skip this part, I'm adding this because the text is difficult to read in my selected image
      ima = Editor("images/levels/zBLACK.png")
      background.blend(image=ima, alpha=.5, on_top=False)

      background.paste(profile.image, (30, 30))

      background.rectangle((30, 220), width=650, height=40, fill="#646464", radius=20)
      background.bar(
        (30, 220),
        max_width=650,
        height=40,
        percentage=percentage,
        fill="#fff",
        radius=20,
      )
      background.text((200, 40), str(userr.name), font=msjh, color="#fff")

      background.rectangle((200, 100), width=350, height=2, fill="#fff")
      background.text(
        (200, 130),
        f"Level : {lvl}   "
        + f" XP : {xp} / {(lvl+1) * 100}",
        font=msjh_small,
        color="#fff",
      )

      card = File(fp=background.image_bytes, filename="images/levels/zCARD.png")
      await ctx.send(file=card)
    except:
      await ctx.send(file=discord.File(r'images/levels/zERROR.png'))
def setup(client):
  client.add_cog(Level(client))