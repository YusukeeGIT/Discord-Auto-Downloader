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

def readChannelsToIgnore():
    global channelsToIgnore
    ignoreChannelsFile = open("channels_to_ignore.txt","r")
    channelsToIgnore = ignoreChannelsFile.read().splitlines()
    ignoreChannelsFile.close()
    channelsToIgnore.append('bot')

def readServersToWatch():
    global serversToWatch
    watchServersFile = open("servers_to_watch.txt","r")
    serversToWatch = watchServersFile.read().splitlines()
    watchServersFile.close()
    if not serversToWatch:
        serversToWatch.append('all')    

def readSettings():
    global dash
    global ignoreTwitter
    global ignoreImgur
    global ignoreInstagram
    global ignorePuush
    settingsFile = open('settings.txt','r')
    settings = settingsFile.read().splitlines()
    settingsFile.close()
    for line in settings:
        settings = line.split('=')
        if 'ignoreTwitter' in settings[0]:
            ignoreTwitter = int(settings[1])
        if 'ignoreInstagram' in settings[0]:
            ignoreInstagram = int(settings[1])
        if 'ignoreImgur' in settings[0]:
            ignoreImgur = int(settings[1])
        if 'ignorePuush' in settings[0]:
            ignorePuush = int(settings[1])
    if "Windows" in platform.system():
        dash = '\\'
    elif "Linux" in platform.system():
        dash = '/'

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

try:
    readChannelsToIgnore()
except Exception as e:
    ignoreChannelsFile = open("channels_to_ignore.txt","w+")
    ignoreChannelsFile.close()
    readChannelsToIgnore()

try:
    readServersToWatch()
except:
    watchServersFile = open("servers_to_watch.txt","w+")
    watchServersFile.close() 
    readServersToWatch() 

try:
    readSettings()
except:
    settingsFile = open('settings.txt','w+')
    settingsFile.writelines('ignoreTwitter=0\n')
    settingsFile.writelines('ignoreInstagram=0\n')
    settingsFile.writelines('ignoreImgur=0\n')
    settingsFile.writelines('ignorePuush=0\n')
    settingsFile.close()
    readSettings()

@client.async_event
async def on_ready():
    subprocess.call('cls',shell=True)
    print('------')
    print('Auto Downloader (By Moe Sea Cow and Yusukee)\nCurrently logged in as ['+client.user.name+' (ID: "'+client.user.id+'")]')
    print('Number of Servers Connected: '+str(len(list(client.servers)))+'\nNumbers of DMs: '+str(len(list(client.private_channels))))
    print('------')
    await client.change_presence(afk=True)


@client.async_event
async def on_message(message):    
    if (not message.author.bot) and (not checkIgnoreChannel(message)):
        currentTime = strftime("%H:%M:%S", localtime())
        imgurmatch = re.match("(https?)\:\/\/(?:i\.)?(www\.)?(?:m\.)?imgur\.com\/(gallery\/|a\/|r\/[a-z]+)?(?:\/)?([a-zA-Z0-9]+)(#[0-9]+)?(?:\.gifv)?", message.content)
        twittermatch = re.match("(https?)\:\/\/(www\.)?(?:m\.)?(twitter.com\/)([a-zA-Z0-9\_\.]+)(\/status\/)+([a-zA-Z0-9]+)", message.content)
        instagrammatch = re.match("(https?)\:\/\/(www\.)?(m\.)?(instagram\.com\/p\/)+([a-zA-Z0-9]+)+(\/)+", message.content)
        puushmatch = re.match("(https?)\:\/\/(?:i\.)?(www\.)?(puu\.sh\/)([a-zA-Z0-9]+\/)([a-zA-Z0-9]+)((\.jpg)?(\.png)?(\.gif)?)+", message.content)
        try:
            if imgurmatch and (not ignoreImgur):
                imgurlink = re.findall("(https?)\:\/\/(?:i\.)?(www\.)?(?:m\.)?imgur\.com\/(gallery\/|a\/|r\/[a-z]+)?(?:\/)?([a-zA-Z0-9]+)(#[0-9]+)?(?:\.gifv)?", message.content)
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
            elif twittermatch and (not ignoreTwitter):
                path = str(message.server.name)+dash+str(message.channel.name) 
                linkRegex = '(https?)\:\/\/(www\.)?(?:m\.)?(twitter.com\/)([a-zA-Z0-9\_\.]+)(\/status\/)+([a-zA-Z0-9]+)'
                imageRegex = '(https?)\:\/\/(www\.)?(m\.)?(pbs.twimg.com\/media\/)+([a-zA-Z0-9\-\_\.]{15})((\.jpg)?(\.png)?)+(\:large)?'
                twitterlink = re.search(linkRegex, message.content) 
                url = twitterlink.group(0)
                thing = url.split('/')
                fileName = str(thing[-1].split('.')[0])
                try:
                    await download_file(url, path, fileName, 'tmp', dash)
                except:
                    print('ERROR | Twitter image download')
                    raise
                try:
                    await downloadImageFromTmp(message, url, path, str(thing[-1].split('.')[0]), dash, imageRegex)
                except:
                    print('ERROR | Twitter image download')
                    raise
            elif instagrammatch and (not ignoreInstagram):
                path = str(message.server.name)+dash+str(message.channel.name)
                linkRegex = '(https?)\:\/\/(www\.)?(m\.)?(instagram\.com\/p\/)+([a-zA-Z0-9]+)+(\/)+'
                imageRegex = '(https?)\:\/\/(www\.)?(m\.)?(instagram\.)+([a-z]{4}[0-9]+\-+[0-9]+\.fna\.fbcdn\.net)+(\/[a-z0-9A-Z]+\.[a-z0-9A-Z]+\-[a-z0-9A-Z]+\/[a-z0-9A-Z]+\/[a-z0-9A-Z]+\_[a-z0-9A-Z]+\_[a-z0-9A-Z]+\_[a-z0-9A-Z]+)+((.jpg)?(.png)?)+'
                instagramlink = re.search(linkRegex, message.content)
                url = instagramlink.group(0)
                fileName = 'instagram'
                try:
                    await download_file(url, path, fileName, 'tmp', dash)
                except:
                    print('ERROR | Instagram image download')
                    raise
                try:
                    await downloadImageFromTmp(message, url, path, fileName, dash, imageRegex)
                except:
                    print('ERROR | Instagram image download')
                    raise
            elif puushmatch and (not ignorePuush):
                path = str(message.server.name)+dash+str(message.channel.name)
                imageRegex = '(https?)\:\/\/(?:i\.)?(www\.)?(puu\.sh\/)([a-zA-Z0-9]+\/)([a-zA-Z0-9]+)((\.jpg)?(\.png)?(\.gif)?)+'
                pic = re.search(imageRegex, message.content)
                url = pic.group(0)
                thing = url.split('/')
                fileType = str(thing[-1].split('.')[-1])
                fileName = str(thing[-1].split('.')[0])
                print('['+str(currentTime)+']: Download puu.sh image from: '+message.server.name+': '+message.channel.name) 
                try:
                    await download_file(url, path, fileName, fileType, dash)
                except:
                    print('exception')
                    raise 
            elif (not message.channel.is_private) and ((message.embeds) or (message.attachments)) and (not imgurmatch):
                name = str(message.server.name)+dash+str(message.channel.name)
                if (not 'instagram' in message.content) and (not 'twitter' in message.content):
                    print('['+str(currentTime)+']: Download image from: '+message.server.name+': '+message.channel.name)
                    if message.embeds:
                        for pic in message.embeds:
                            url = str(pic['url'])
                            thing = url.split('/')
                            fileType = str(thing[-1].split('.')[-1])
                            if (':large' in fileType) and ('pbs.twimg.com' in url):
                                fileType = str(thing[-1].split('.')[-1]).replace(':large', '')
                            elif (':orig' in fileType) and ('pbs.twimg.com' in url):
                                fileType = str(thing[-1].split('.')[-1]).replace(':orig', '')
                            elif 'pbs.twimg.com' in url:
                                url = url+':large'
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
        except:
            raise
            print('ERROR!!!! | '+message.server.name+': '+message.author.name+': '+message.content)

async def downloadImageFromTmp(message, url, path, fileName, dash, imageRegex):
    currentTime = strftime("%H:%M:%S", localtime())
    file = open('pictures'+dash+path+dash+fileName+'.tmp', "r", encoding="utf8")
    fileLines = file.read().splitlines()
    for line in fileLines:
        pic = re.search(imageRegex, line)
        if pic:
            url = pic.group(0)
            break;
        else:
            url = False
    file.close()
    if url:      
        thing = url.split('/')
        fileType = str(thing[-1].split('.')[-1])
        if 'pbs.twimg.com' in url:
            print('['+str(currentTime)+']: Download Twitter image from: '+message.server.name+': '+message.channel.name) 
            if (':large' in fileType) and ('pbs.twimg.com' in url):
                fileType = str(thing[-1].split('.')[-1]).replace(':large', '')
            elif (':orig' in fileType) and ('pbs.twimg.com' in url):
                fileType = str(thing[-1].split('.')[-1]).replace(':orig', '')
            elif 'pbs.twimg.com' in url:
                url = url+':large'
        else:
            print('['+str(currentTime)+']: Download Instagram image from: '+message.server.name+': '+message.channel.name) 
        try:
            await download_file(url, path, fileName, fileType, dash)
        except:
            print('exception')
            raise   
    os.remove('pictures'+dash+path+dash+fileName+'.tmp')

def checkIgnoreChannel(message):
    for server in serversToWatch:
        if (server == message.server.name) or ('all' == server):
            watchServer = True
            break
        else:
            watchServer = False
    if watchServer:
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
        time = strftime("%Y%m%d%H%M%S", localtime())
        r = requests.get(url, headers=headers, stream=True)
        with open('.'+dash+'pictures'+dash+path+dash+str(file_name)+'_'+str(time)+'.'+str(file_type), 'wb') as f:
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
