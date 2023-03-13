# general imports
from dotenv import load_dotenv
import os

# open AI imports
import openai
import gradio as gr

# discord imports
import discord
from discord.ext import commands, tasks

# getting API Keys
load_dotenv()

openai.api_key = os.getenv('openAIKey')
Disc_TOKEN = os.getenv('discordKey')

messages = [
    {"role": "system", "content": "You are a egoistic bot that reply sracastically."},
    ]

##Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = "$", intents = intents)

@bot.event
async def on_ready():
    print("Bot is Live")

@bot.command()
async def chad (ctx,input):
    reply=chadbot_initialiser(input)
    await ctx.send(reply)

@bot.command()
async def support (ctx, member:discord.Member = None):
    if member == None:
        member = ctx.author

    name = member.display_name

    embed = discord.Embed(title="Who Made This?", description = "", color = discord.Color.random())
    embed.set_author(name=f"{name}")
    embed.add_field(name = "Creator", value = "IndianGrandpa")
    embed.add_field(name = "Co-Creator", value = "[Nuggetierer](https://twitter.com/NuggetiererReal)", inline = False)
    embed.set_footer(text = f"{name} Thanks for Supporting Us")

    await ctx.send(embed = embed)

# open AI
def chadbot_initialiser(input):
    if input:
        messages.append({"role": "user", "content": input})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "system", "content": "You are a egoistic bot that reply sracastically."})
        return reply

bot.run(Disc_TOKEN)
