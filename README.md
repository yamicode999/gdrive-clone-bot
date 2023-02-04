# WHAT THE FUCK IS THIS!?

This project is a direct modification of [mirror-leech-telegram-bot](https://github.com/anasty17/mirror-leech-telegram-bot) by @anasty17, keeping only the cloning related features for people who only need a good cloning bot. The bot is very lightweight and can be hosted on most free tier PaaS plans.
<p align="center"><img src="https://i.ibb.co/MnqNByY/Screenshot-20230128-090728-Nekogram.png" /></p>

## Features
- [x] Clone public Google Drive links.
- [x] Clone private Google Drive links (with access).
- [x] Search in drives recursively, see results in Telegraph Instant View.
- [x] Count files/folders in a folder by link.
- [x] Delete files/folders by link.
- [x] Built-in updater, portable configuration. Configure bot settings & stay up-to-date with the source, without redeploying!

## How the fuck do you setup this shit?
0. Fork this repo.
1. Google Credentials! Create a `token.pickle` file and/or `accounts.zip` (for SA support). Follow [this guide](https://github.com/weebzone/WZML/wiki/Deployment#getting-google-oauth-api-credential-file-and-tokenpickle) to obtain them.
2. Upload the credential files to a secure location where you can obtain a direct link to them. Such as your root drive's personal index.
3. Create a gist named `something.env`. Fill in the following variables and add them to the gist:
    ```
    # Required Variables
    # Should be self-explanatory
    
    TELEGRAM_API = ""
    TELEGRAM_HASH = ""
    OWNER_ID = ""
    BOT_TOKEN = ""
    
    # Bot Private Files
    # ONLY DIRECT LINKS ARE SUPPORTED
    
    ACCOUNTS_ZIP = "" # direct link to accounts.zip file
    DRIVES_TXT = "" # direct link to drives.txt file
    TOKEN_PICKLE = "" # direct link to token.pickle file
    
    # Optional (but required) Variables
    # Read the attached comments carefullly before filling them
    
    AUTHORIZED_CHATS = "" # user/group ids
    AUTO_DELETE_MESSAGE_DURATION = "30" # no need to change
    CMD_SUFFIX = "" # should be alphanumeric
    GDRIVE_ID = "" # ID of the destination drive or 'root'
    INDEX_URL = "https://something.someone.workers.dev/0:" # you know what to set
    IS_TEAM_DRIVE = "True" # or False
    SERVER_PORT = "" # don't set anything if you're deploying on Render
    STATUS_LIMIT = "4" # no need to change
    STATUS_UPDATE_INTERVAL = "10" # no need to change
    STOP_DUPLICATE = "True" # or False
    UPSTREAM_BRANCH = "main" # don't change this
    UPSTREAM_REPO = "https://github.com/culturecloud/gdrive-clone-bot" # don't change this to keep the bot up-to-date
    USE_SERVICE_ACCOUNTS = "True" # or False
    VIEW_LINK = "False" # or True
    ```
5. Copy the gist's raw URL. It should look something like this:
    `https://gist.github.com/user/2d59b1ec7a6903532/raw/012b5e033488f77ff5c/config.env`
6. Remove the revision ID after `/raw`, along with a slash. The URL should now look like this:
    `https://gist.github.com/user/2b6a322ec7a903532/raw/config.env`
7. Set the URL as the value of the `CONFIG_ENV` variable where you want to deploy the bot. This is the only variable you need to set.
8. Deploy the bot.

## Exrtra Notes
- You can edit the configuration on gist.github.com and restart the bot using the `/restart` command. The bot will use the new configuration upon restart, so there is no need to redeploy it.
- If you want to update the bot to use latest code, keep upstream variables and just `/restart` it!

## Multi TD/Folders Search
To use `/list` command with multiple TD/folders, simply make a file named `drives.txt` file in working directory and fill it, in the following format:
```
DriveName folderID/tdID IndexLink(if available)
DriveName folderID/tdID IndexLink(if available)
```
Example:
```
RootDrive root https://example.workers.dev/0:
TeamDrive1 0AO1JDB1t3i5jUk9PVA https://example.workers.dev/1:
TeamDrive2 0A10hdb1t67hjYrTyVA https://example.workers.dev/2:
```
It goes without saying but you need to have access to these drives in order to search in them. Another thing to note that if you're using this bot with SA only and your SA group doesn't have access to these drives/folders, you can't search in them.

After you're done, upload the `drives.txt` file along with `token.pickle` and/or `accounts.zip` and set the direct link to this file as `DRIVES_TXT` variable.

## Planned Features
- [ ] Setup Google credentials (token.pickle) using the bot interface.
- [ ] Choosing destination drive using the bot interface.
- [ ] Auto resume support, bot will automatically resume cloning from where it stopped. (If it stops accidentally)
- [ ] TD to TD auto/scheduled sync.
