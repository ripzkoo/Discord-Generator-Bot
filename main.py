# discord.gg/generators

import nextcord, os, random, datetime, asyncio
from nextcord.ext import commands

free_gen_channel = 5374638235 # Channel ID here

free_cooldowns = {}

intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents, help_command=None)

server_name = "ENTER YOUR SERVER NAME HERE"
server_logo = "ENTER YOUR SERVER'S LOGO LINK HERE"

@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.playing,name=server_name))
    print("Running")

@bot.slash_command(name="gen", description="Generate free accounts!")
async def gen(inter, stock):
    user = inter.user
    user_id = inter.user.id

    if user_id in free_cooldowns:
        remaining_cooldown = free_cooldowns[user_id]
        embed = nextcord.Embed(title="Cooldown", description=f"You still have {remaining_cooldown} seconds remaining.",
                               color=nextcord.Color.red())
        await inter.send(embed=embed, ephemeral=True)
        return
    if inter.channel.id != free_gen_channel:
        embed = nextcord.Embed(title="Wrong Channel! Use <#free_gen_channel>", color=nextcord.Color.red())
        await inter.send(embed=embed, ephemeral=True)
        return
    
    stock = stock.lower() + ".txt"
    if stock not in os.listdir("freestock//"):
        embed = nextcord.Embed(title="The stock that you are trying to generate does not exist.", color=nextcord.Color.red())
        await inter.send(embed=embed, ephemeral=True)
        return
    
    with open(f"freestock//{stock}") as file:
        lines = file.read().splitlines()
        if len(lines) == 0:
            embed = nextcord.Embed(title="Out of stock!", description="Please wait until we restock!", color=nextcord.Color.red())
            await inter.send(embed=embed, ephemeral=True)
            return
    
    account = random.choice(lines)
    combo = account.split(':')
    User = combo[0]
    Pass = combo[1]
    Password = Pass.rstrip()
    
    embed = nextcord.Embed(title=server_name, color=nextcord.Color.yellow())
    embed.set_footer(text=server_name, icon_url=server_logo)
    embed.set_thumbnail(url=server_logo)
    embed.add_field(name="Username:", value=f"```{str(User)}```")
    embed.add_field(name="Password:", value=f"```{str(Password)}```")
    embed.add_field(name="Combo:", value=f"```{str(User)}:{str(Password)}```", inline=False) 
    await user.send(embed=embed)
    
    name = (stock[0].upper() + stock[1:].lower()).replace(".txt", "")
    
    embed1 = nextcord.Embed(title=f"{name} Account Generated!", description="> Check your DMs for your account!", color=nextcord.Color.green())
    embed1.set_footer(text=server_name, icon_url=server_logo)
    embed1.set_thumbnail(url=server_logo)
    await inter.send(embed=embed1) 
    lines.remove(account)
    with open(f"freestock//{stock}", "w", encoding='utf-8') as file:
        file.write("\n".join(lines))

    free_cooldowns[user_id] = 30
    await asyncio.sleep(1)
    while free_cooldowns[user_id] > 0:
        free_cooldowns[user_id] -= 1
        await asyncio.sleep(1)

    del free_cooldowns[user_id]

@bot.slash_command(name="stock", description="View free stock!")
async def freestock(inter: nextcord.Interaction):   
    embed = nextcord.Embed(title="Account Stock", color=nextcord.Color.green(), timestamp=datetime.datetime.utcnow())
    embed.set_footer(text=server_name, icon_url=server_logo)
    embed.set_thumbnail(url=server_logo)
    embed.description = ""
    for filename in os.listdir("freestock/"):
        with open(f"freestock/{filename}") as f: 
            amount = len(f.read().splitlines())
            name = (filename[0].upper() + filename[1:].lower()).replace(".txt","") 
            embed.description += f"* **{name}**: `{amount}`\n"
    await inter.send(embed=embed, ephemeral=True)

@bot.slash_command(name="help", description="Show all available commands!")
async def help(ctx):
    embed = nextcord.Embed(title=server_name, color=nextcord.Color.red())
    embed.set_footer(text=server_name, icon_url=server_logo)
    embed.set_thumbnail(url=server_logo)
    embed.add_field(name="/help", value="Shows this command", inline=False)
    embed.add_field(name="/gen", value="Generate free accounts", inline=False)
    embed.add_field(name="/stock", value="View free stock", inline=False)
  
    await ctx.send(embed=embed)

bot.run("")

# discord.gg/generators
