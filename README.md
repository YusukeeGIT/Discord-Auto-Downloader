#### This is a modified version of [PvtSeaCow's Discord-AutoDownloader](https://github.com/PvtSeaCow/Discord-AutoDownloader)

# IMPORTANT
- Requires Python 3.5 64bit, NOTHING ELSE, ANY OTHER VERSION WILL NOT WORK  
- Requires Discord.py Made By: [Rapptz](https://github.com/Rapptz)
 - Get from here: [Rapptz/discord.py](https://github.com/Rapptz/discord.py)
- ALSO REQUIRES REQUESTS  
 - type in command prompt `pip install requests`
- ALSO REQUIRES IMGURPYTHON [Imgur/imgurpython](https://github.com/Imgur/imgurpython)
 - type in command prompt `pip install imgurpython`

#### Credentials
1. Edit 'credentials.txt' (Login is in plain text, careful)

# About
This is a discord bot that automatically downloads any picture from any of the servers/guilds you are in.  
#### WARNING:  
Running this bot acts as another login and will keep you online as long as this bot is on. There is no way to change this because Discord doesn't allow users to be offline and online at the same time (At the moment).  
~~Because you are now online with this bot on, ALL notifications will not show up on mobile (Might Change in the future).~~ (Might work now, I need to do more testing)

# Settings
- Run the script first to generate all settings / ignore files.
- This bot can extract pictures from imgur, twitter, instagram posts
- In settings.txt you can set to ignore these posts. (1 to ignore | 0 to watch)

### Ignore servers / channels:
- Ignores bots in all server / channel by default.
#### Servers:
- Add server name to servers_to_ignore.txt file
- New line for every server name.

#### Channels:
- Add channel name to channels_to_ignore.txt file
- New line for every channel name.

# File Stucture
1. This bot will download to the following folders:  
 - `(ROOT)/pictures/(Server Name)/(Channel Name)`  
- This bot will download pictures from dms too:  
 - `(ROOT)/pictures/@pms/[User]`  
- Imgur images will download to: 
 - `(ROOT)/pictures/(Server Name)/(Channel Name)/@imgur/(Album/Image ID)`
 
() = Will always be made  
[] = Will be made when the channel doesn't have lood/lewd/nsfw in the name or the server is not `Pillow Lounge`  
(ROOT) = The folder the script is in.  
This bot may not download every picture (working on it.) 

## TODO
	Clean code because it is a mess now.
	Check if download error occure.

## Credits

Original version: [PvtSeaCow](https://github.com/PvtSeaCow/Discord-AutoDownloader) 

##### Disclaimer
I am __NOT__ responsible for the files you download. You may download files that are not picture files and the file may be a virus. I am __NOT__ responsible if you happen to download a virus. Although I blocked downloading of exe's, some may slip by and will download.