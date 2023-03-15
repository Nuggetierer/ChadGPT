# general imports
from dotenv import load_dotenv
import os

# memory class
from msgHistory import msgHist

# open AI imports
import openai
import gradio as gr

# discord imports
import discord
from discord.ext import commands, tasks

# getting API Keys
"""
load_dotenv is a python package that allows to look into a .env file to get hidden keys or values
"""
load_dotenv()

openai.api_key = os.getenv('openAIKey')
Disc_TOKEN = os.getenv('discordKey')

# initial prompt Message
messages = [
    {"role": "system", "content": "You are a egoistic bot that reply sracastically."},
    ]

# building dictionary to store past inputs
userMsgHistory = []

# Discord
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = "$", intents = intents)

@bot.event
async def on_ready():
    print("Bot is Live")

# command error messages
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"This command is on cooldown for {round(error.retry_after,2)} seconds!")

"""
Basic ChadGPT call
- Basis for future GPT calls
"""
@bot.command()
async def chad (ctx,input):
    reply=chadbot_initialiser(input)
    await ctx.send(reply)

"""
ChadGPT call with Embed
- Cooldown 20 seconds
- Embed with Prompt and Reply
"""
@bot.command()
@commands.cooldown(1,20, commands.BucketType.user)
async def chadEmbed (ctx,*,input):
    # collect reply
    reply=chadbot_initialiser(input)

    #building the embed
    embed = discord.Embed(title="ChadGPT", description="", color = discord.Color.random())
    embed.add_field(name = "Prompt", value = input, inline=False)
    embed.add_field(name = "Reply", value = reply, inline=False)
    embed.set_footer(text= "Replies are not representative of OpenAIs model")

    await ctx.send(embed = embed)

@bot.command()
@commands.cooldown(1,20, commands.BucketType.user)
async def chadEmbed2 (ctx,*,input):
    # check if user has a message history
    

    # figure out a way to throw error when too many words i.e. over x amount of token

    # collect reply
    reply=chadbot_initialiser(input)

    #building the embed
    embed = discord.Embed(title="ChadGPT", description="", color = discord.Color.random())
    embed.add_field(name = "Prompt", value = input, inline=False)
    embed.add_field(name = "Reply", value = reply, inline=False)
    embed.set_footer(text= "Replies are not representative of OpenAIs model")

    await ctx.send(embed = embed)

"""
Support command to represent creators
- Vibu Vignesh = IndianGrandpa
- Teh Zhi Xian = Nuggetierer
"""
@bot.command()
async def support (ctx, member:discord.Member = None):
    if member == None:
        member = ctx.author

    name = member.display_name

    embed = discord.Embed(title="Who Made This?", description = "", color = discord.Color.random())
    embed.set_author(name=f"{name}")
    embed.add_field(name = "Creator", value = "[IndianGrandpa](https://www.linkedin.com/in/vibu-vignesh-b6922b211/)")
    embed.add_field(name = "Co-Creator", value = "[Nuggetierer](https://twitter.com/NuggetiererReal)", inline = False)
    embed.set_footer(text = f"{name} Thanks for Supporting Us")

    await ctx.send(embed = embed)

# open AI
"""
Command to make a chadbot request

Note: We may be expanding to different personality, may adjust the way personality is built by declaring system content
at the start of the function instead of after this way we dont have to build message prompt first
"""
def chadbot_initialiser(input):
    if input:
        messages.append({"role": "user", "content": input})
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content

        # reminding chatGPT the context
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "system", "content": "You are a egoistic bot that reply sracastically."})
        return reply

"""
provides chadbot a way to remember the message history

Note: We might go over the limit of tokens

Warnings
- need to create if user is not in DB
- need to have a way to clear history
- potentially create a second instance?
"""
def chadbot_memory(input, msgHist):
    msgHist.messages += f"{msgHist.userID}: {input}\n"

    reply = chadbot_initialiser(msgHist.messages)

    msgHist.messages += f"ChadGPT: {reply}\n"

    return reply

bot.run(Disc_TOKEN)
