# Work with Python 3.6
import discord
import json
import WebScrape
import GenerateGraph
from discord import File

with open('Secret.json') as json_file:  
    data = json.load(json_file)
    TOKEN = data['discordKey']

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        # await message.channel.send(msg)
        testFile = File('options.csv')
        await message.channel.send(file = testFile)

    elif message.content.startswith('!recordanewmixtape'):
        msg = 'No {0.author.mention}, you do it'.format(message)
        await message.channel.send(msg)

    elif message.content.startswith('!tickers'):
        cmd = message.content
        cmd = cmd[9:]
        print('tickers command ticker: ' + cmd)
        try:
            tickers = WebScrape.printTickers(cmd)
            msg = ''
            for tick in tickers:
                msg = msg + tick + '\n'
        except:
            msg = 'Not a valid option\nLook at !listOptions'
            
        await message.channel.send(msg)

    elif message.content.startswith('!setOption'):
        cmd = message.content
        cmdParts = cmd.split()
        WebScrape.setOption(cmdParts[1], cmdParts[2])
        msg = '{0.author.mention} new option added '.format(message) + cmdParts[2]
        await message.channel.send(msg)

    elif message.content.startswith('!removeOption'):
        cmd = message.content
        cmdParts = cmd.split()
        WebScrape.removeOption(cmdParts[1])
        msg = '{0.author.mention} option was removed '.format(message) + cmdParts[1]
        await message.channel.send(msg)

    elif message.content.startswith('!listOptions'):
        options = WebScrape.getOptions()
        msg = ''
        if options == 'There are no current options setup use !setOptions to set a new option':
            msg = options
        else:
            for opt in options:
                msg = msg + opt + '\n'
        await message.channel.send(msg)

    elif message.content.startswith('!stock'):
        cmd = message.content
        cmdParts = cmd.split()
        GenerateGraph.makeGraph(cmdParts[1])
        graphFile = File('stock_information.html')
        await message.channel.send(file = graphFile)


    elif message.content.startswith('!help'):
        msg = 'Remember to seperate each part of the command with a space\n'
        msg = msg + '!setOption <link to screener> <name of option (one word)>\n'
        msg = msg + '!removeOption <name of option>\n'
        msg = msg + '!listOptions\n'
        msg = msg + '!tickers <name of option>\n'
        msg = msg + '!stock <stock ticker>\n'
        await message.channel.send(msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)