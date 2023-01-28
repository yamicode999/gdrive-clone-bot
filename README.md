# WHAT THE FUCK IS THIS!?

This project is a direct modification of [mirror-leech-telegram-bot](https://github.com/anasty17/mirror-leech-telegram-bot) by @anasty17, keeping only the cloning related features for people who only need a good cloning bot. The bot is very lightweight and can be hosted on most free tier PaaS plans.

## How the fuck do you setup this shit?
1. Google Credentials! Create a `token.pickle` file and/or `accounts.zip` (for SA support). Follow [this guide](https://github.com/weebzone/WZML/wiki/Deployment#getting-google-oauth-api-credential-file-and-tokenpickle) to obtain them.
2. Upload the credential files to a secure location where you can obtain a direct link to them. Such as your root drive's personal index.
3. Create a gist named `something.env`. Fill in the following variables and add them to the gist:
    ```
    BOT_TOKEN = ""
    OWNER_ID = ""
    TELEGRAM_API = ""
    TELEGRAM_HASH = ""
    TOKEN_PICKLE = "" # direct link to token.pickle file
    ACCOUNTS_ZIP = "" # direct link to accounts.zip file
    UPSTREAM_REPO = "https://github.com/culturecloud/gdrive-clone-bot" # don't change this to keep the bot up-to-date
    UPSTREAM_REPO = "master" # don't change this
    GDRIVE_ID = ""
    IS_TEAM_DRIVE = "True"
    STOP_DUPLICATE = "True" # or False
    INDEX_URL = "https://something.someone.workers.dev/0:" # you know what to set
    VIEW_LINK = "False" # or True
    STATUS_LIMIT = "4" # no need to change
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
- [ ] Setup Google credentials (token.pickle) using the bot itself.
- [ ] Store Google credentials using MongoDB, making the bot completely plug and play!
- [ ] TD to TD auto/scheduled sync.
