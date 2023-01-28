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
1. Google Credentials! Create a `token.pickle` file and/or `accounts.zip` (for SA support). Follow [this guide](https://github.com/weebzone/WZML/wiki/Deployment#getting-google-oauth-api-credential-file-and-tokenpickle) to obtain them.
2. Upload the credential files to a secure location where you can obtain a direct link to them. Such as your root drive's personal index.
3. Create a gist named `something.env`. Fill in the following variables and add them to the gist:
    ```
    # Required Variables
    TELEGRAM_API = ""
    TELEGRAM_HASH = ""
    OWNER_ID = ""
    BOT_TOKEN = ""
    
    # Optional (but required) Variables
    ACCOUNTS_ZIP = "" # direct link to accounts.zip file
    AUTHORIZED_CHATS = ""
    AUTO_DELETE_MESSAGE_DURATION = "30"
    CMD_SUFFIX = ""
    GDRIVE_ID = ""
    INDEX_URL = "https://something.someone.workers.dev/0:" # you know what to set
    IS_TEAM_DRIVE = "True"
    SERVER_PORT = "" # don't set anything if you're deploying on Render
    STATUS_LIMIT = "4" # no need to change
    STATUS_UPDATE_INTERVAL = "10" # no need to change
    STOP_DUPLICATE = "True" # or False
    TOKEN_PICKLE = "" # direct link to token.pickle file
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

## Planned Features
- [ ] Setup Google credentials (token.pickle) using the bot interface.
- [ ] Choosing destination drive using the bot interface.
- [ ] Auto resume support, bot will automatically resume cloning from where it stopped. (If it stops accidentally)
- [ ] TD to TD auto/scheduled sync.
