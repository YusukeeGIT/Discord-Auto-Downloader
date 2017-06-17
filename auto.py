import pip
try:
    import discord
except:
    pip.main(['install', 'git+https://github.com/Rapptz/discord.py@async'])
    sleep(2)
    import discord
import asyncio
import unicodedata

import json
import os
import re
import subprocess
import random
from time import localtime, strftime
from pathlib import Path
import platform
try:
    import requests
except :
    import pip
    pip.main(['install', 'requests'])
    import requests
try:
    import imgurpython
    from imgurpython import ImgurClient
except:
    pip.main(['install', 'imgurpython'])
    sleep(2)
    import imgurpython
    from imgurpython import ImgurClient

from sys import modules

client = discord.Client()

def setup():
    f = open("credentials.txt", 'w+')
    email = input('Email: ')
    password = input('Password: ')
    f.write(email+':'+password)
    f.close()

try:
    f = open('credentials.txt', 'r')
    login_info = f.read().split(':')
    f.close()
except:
    print('ERROR: \'credentials.txt\' not found!')
    setup()
    sleep(2)
    sys.exit(0)

try:
    f = open('imgur.txt', 'r')
    imgur_info = f.read().split(':')
    f.close()
    imgur = ImgurClient(imgur_info[0],imgur_info[0])
except:
    print('Register a imgur key at: https://api.imgur.com/oauth2/addclient')
    print('''Select 'OAuth2 without url' ''')
    f = open("imgur.txt", 'w+')
    ID = input('Client ID: ')
    Secret = input(' Client Secret: ')
    f.write(ID+':'+Secret)
    f.close()
    sleep(2)
    sys.exit(0)

@client.async_event
async def on_ready():
    subprocess.call('cls',shell=True)
    print('------')
    print('Auto Downloader (By Moe Sea Cow)\nCurrently logged in as ['+client.user.name+' (ID: "'+client.user.id+'")]')
    print('Number of Servers Connected: '+str(len(list(client.servers)))+'\nNumbers of DMs: '+str(len(list(client.private_channels))))
    print('------')
    await client.change_presence(afk=True)


@client.async_event
async def on_message(message):
    if "Windows" in platform.system():
        dash = '\\'
    elif "Linux" in platform.system():
        dash = '/'
    currentTime = strftime("%H:%M:%S", localtime())    
    if (not message.author.bot) and (not checkIgnore(message)):
        imgurlink = re.findall("(https?)\:\/\/(?:i\.)?(www\.)?(?:m\.)?imgur\.com\/(gallery\/|a\/|r\/[a-z]+)?(?:\/)?([a-zA-Z0-9]+)(#[0-9]+)?(?:\.gifv)?", message.content)
        imgurmatch = re.match("(https?)\:\/\/(?:i\.)?(www\.)?(?:m\.)?imgur\.com\/(gallery\/|a\/|r\/[a-z]+)?(?:\/)?([a-zA-Z0-9]+)(#[0-9]+)?(?:\.gifv)?", message.content)
        twimglink = re.findall("(https?)\:\/\/(www\.)?(?:m\.)?(pbs.twimg\/+)\.com\/(media\/+)?(?:\/)?([a-zA-Z0-9_.:]+)(#[0-9]+)?(?:\.gifv)?", message.content)
        twimgmatch = re.match("(https?)\:\/\/(www\.)?(?:m\.)?(pbs.twimg\/+)\.com\/(media\/+)?(?:\/)?([a-zA-Z0-9_.:]+)(#[0-9]+)?(?:\.gifv)?", message.content)
        try:
            if imgurmatch:
                try:
                    for lnk in imgurlink:
                        name = str(message.server.name)+dash+str(message.channel.name)+dash+'@imgur'+dash+str(imgur.get_album(lnk[3]).id)
                        print('['+str(currentTime)+']: Download imgur image from: '+message.server.name+': '+message.channel.name)
                        countImages = 0
                        allImages = len(imgur.get_album_images(lnk[3]))
                        for pic in imgur.get_album_images(lnk[3]):
                            countImages = countImages+1
                            if pic.animated:
                                thing = str(pic.link).split('/')
                                fileNameWithExtension = str(thing[-1].split('.')[-2])+'.'+str(thing[-1].split('.')[-1])
                                print('---('+str(countImages)+'/'+str(allImages)+') Downloading album - '+fileNameWithExtension)
                                await download_file(str(pic.link), str(name), str(thing[-1].split('.')[-2]), str(thing[-1].split('.')[-1]), dash)
                            else:
                                thing = str(pic.link).split('/')
                                fileNameWithExtension = str(thing[-1].split('.')[-2])+'.'+str(thing[-1].split('.')[-1])
                                print('---('+str(countImages)+'/'+str(allImages)+') Downloading album - '+fileNameWithExtension)
                                await download_file(str(pic.link), str(name), str(thing[-1].split('.')[-2]), str(thing[-1].split('.')[-1]), dash)
                except:
                    for lnk in imgurlink:
                        name = str(message.server.name)+dash+str(message.channel.name)+dash+'@imgur'+dash+str(imgur.get_image(lnk[3]).id)
                        print('['+str(currentTime)+']: Download imgur image from: '+message.server.name+': '+message.channel.name)
                        pic = imgur.get_image(lnk[3])
                        if pic.animated:
                            thing = str(pic.link).split('/')
                            await download_file(str(pic.link), str(name), str(thing[-1].split('.')[-2]), str(thing[-1].split('.')[-1]), dash)
                        else:
                            thing = str(pic.link).split('/')
                            await download_file(str(pic.link), str(name), str(thing[-1].split('.')[-2]), str(thing[-1].split('.')[-1]), dash)
            elif (not message.channel.is_private) and ((message.embeds) or (message.attachments)) and (not imgurmatch):
                name = str(message.server.name)+dash+str(message.channel.name)
                print('['+str(currentTime)+']: Download image from: '+message.server.name+': '+message.channel.name)
                if message.embeds:
                    for pic in message.embeds:
                        thing = str(pic['url']).split('/')
                        #Twitter images link replace to :large and remove :large from file extension
                        url = str(pic['url'])
                        fileType = str(thing[-1].split('.')[-1])
                        if (':large' in fileType):
                            fileType = str(thing[-1].split('.')[-1]).replace(':large', '')
                        elif ('pbs.twimg.com' in url):
                            url = str(pic['url'])+':large'
                        #Twitter image end
                        try:
                            await download_file(url, str(name), str(thing[-1].split('.')[0]), fileType, dash)
                        except:
                            print('exception')
                            pass
                elif message.attachments:
                    #GIF download
                    for pic in message.attachments:
                        thing = str(pic['url']).split('/')
                        try:
                            await download_file(str(pic['url']), (name), str(thing[-1].split('.')[-2]), str(thing[-1].split('.')[-1]), dash)
                        except:
                            pass
                elif r_image.match(urls[0]):
                    for pic in urls:
                        thing = str(pic).split('/')
                        try:
                            await download_file(str(pic), (name), str(thing[-1].split('.')[-2]), str(thing[-1].split('.')[-1]), dash)
                        except:
                            pass
                else:
                    print('ERROR!! |'+str(pic['url'])+'|'+name+'|'+str(thing[-1].split('.')[-2])+'|'+str(thing[-1].split('.')[-1]))
            elif (message.channel.is_private) and (message.embeds or message.attachments) and (not imgurmatch):
                name = '@pms\\'+str(message.channel.user)
                if message.embeds:
                    for pic in message.embeds:
                        thing = str(pic['url']).split('/')
                        try:
                            await download_file(str(pic['url']), str(name), str(thing[-1].split('.')[-2]), str(thing[-1].split('.')[-1]), dash)
                        except:
                            pass
                elif message.attachments:
                    for pic in message.attachments:
                        thing = str(pic['url']).split('/')
                        try:
                            await download_file(str(pic['url']), str(name), str(thing[-1].split('.')[-2]), str(thing[-1].split('.')[-1]), dash)
                        except:
                            pass
                else:
                    print('ERROR!! |'+str(pic['url'])+'|'+name+'|'+str(thing[-1].split('.')[-2])+'|'+str(thing[-1].split('.')[-1]))
        except Exception as e:
            raise
            print(message.server.name+': '+message.author.name+': '+message.content)


def checkIgnore(message):
    channelsFile = open("channels_to_ignore.txt","r")
    serversFile = open("servers_to_ignore.txt","r")
    channelsToIgnore = channelsFile.read().splitlines()
    serversToIgnore = serversFile.read().splitlines()
    channelsToIgnore.append('bot')
    serversToIgnore.append('bot')
    for server in serversToIgnore:
        if server == message.server.name:
            ignoreServer = True
            break
        else:
            ignoreServer = False
    if not ignoreServer:
        for channel in channelsToIgnore:
            if channel == message.channel.name:
                ignoreMessage = True
                break
            else:
                ignoreMessage = False
    else:
        ignoreMessage = True
    return ignoreMessage


async def download_file(url, path, file_name, file_type, dash):
    if file_type == 'exe' or file_name == 'js':
        return
    if not os.path.exists('.'+dash+'pictures'+dash+path):
        os.makedirs('.'+dash+'pictures'+dash+path)
    headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0'
    }
    try:
        test_file = Path('.'+dash+'pictures'+dash+path+dash+str(file_name)+'.'+str(file_type))
        test_path = test_file.resolve()
        random_number = random.randint(1, 10000000000000)
        r = requests.get(url, headers=headers, stream=True)
        with open('.'+dash+'pictures'+dash+path+dash+str(file_name)+str(random_number)+'.'+str(file_type), 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    except FileNotFoundError:
        r = requests.get(url, headers=headers, stream=True)
        with open('.'+dash+'pictures'+dash+path+dash+str(file_name)+'.'+str(file_type), 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

client.run(login_info[0], login_info[1])