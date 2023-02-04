from logging import FileHandler, StreamHandler, INFO, basicConfig, error as log_error, info as log_info
from os import path as ospath, environ
from subprocess import run as srun
from dotenv import load_dotenv

if ospath.exists('log.txt'):
    with open('log.txt', 'r+') as f:
        f.truncate(0)

basicConfig(format='[%(levelname)s] [%(name)s] [%(lineno)d] %(message)s',
            handlers=[FileHandler('log.txt'), StreamHandler()],
            level=INFO)
                    
CONFIG_ENV = environ.get('CONFIG_ENV', None)
if CONFIG_ENV:
    log_info("CONFIG_ENV variable found! Downloading config file ...")
    download_file = srun(["curl", "-sL", f"{CONFIG_ENV}", "-o", "config.env"])
    if download_file.returncode == 0:
        load_dotenv('config.env', override=True)
        log_info("Config file has been downloaded and loaded in current environment")
    else:
        log_error("Something went wrong while downloading config file! please recheck the CONFIG_ENV variable")
        exit(1)
else:
    log_error("CONFIG_ENV variable not found! exiting ...")
    exit(1)

TOKEN_PICKLE = environ.get('TOKEN_PICKLE', None)
if TOKEN_PICKLE:
    log_info("TOKEN_PICKLE variable found! Downloading token.pickle file ...")
    download_file = srun(["curl", "-sL", f"{TOKEN_PICKLE}", "-o", "token.pickle"])
    if download_file.returncode == 0:
        log_info("Pickle file downloaded as 'token.pickle'")
    else:
        log_error("Something went wrong while downloading token.pickle file! please recheck the TOKEN_PICKLE variable")

ACCOUNTS_ZIP = environ.get('ACCOUNTS_ZIP', None)
if ACCOUNTS_ZIP:
    log_info("ACCOUNTS_ZIP variable found! Downloading accounts.zip file ...")
    download_file = srun(["curl", "-sL", f"{ACCOUNTS_ZIP}", "-o", "accounts.zip"])
    if download_file.returncode == 0:
        log_info("Service Accounts zip file downloaded as 'accounts.zip'")
    else:
        log_error("Something went wrong while downloading Service Accounts zip file! please recheck the ACCOUNTS_ZIP variable")

if TOKEN_PICKLE is None and ACCOUNTS_ZIP is None:
    log_warning("Neither TOKEN_PICKLE nor ACCOUNTS_ZIP variable has been provided! If you don't provide either token.pickle or accounts.zip you won't be able to use this bot.")

DRIVES_TXT = environ.get('DRIVES_TXT', None)
if DRIVES_TXT:
    log_info("DRIVES_TXT variable found! Downloading drives.txt file ...")
    download_file = srun(["curl", "-sL", f"{DRIVES_TXT}", "-o", "drives.txt"])
    if download_file.returncode == 0:
        log_info("Drives list downloaded as 'drives.txt'")
    else:
        log_error("Something went wrong while downloading drives list file! please recheck the DRIVES_TXT variable")

BOT_TOKEN = environ.get('BOT_TOKEN', '')
if len(BOT_TOKEN) == 0:
    log_error("BOT_TOKEN variable is missing! Exiting now")
    exit(1)

bot_id = int(BOT_TOKEN.split(':', 1)[0])

UPSTREAM_REPO = environ.get('UPSTREAM_REPO', '')
if len(UPSTREAM_REPO) == 0:
    UPSTREAM_REPO = None
    
UPSTREAM_BRANCH = environ.get('UPSTREAM_BRANCH', '')
if len(UPSTREAM_BRANCH) == 0:
    UPSTREAM_BRANCH = 'main'
    
if UPSTREAM_REPO:
    if ospath.exists('.git'):
        srun(["rm", "-rf", ".git"])
    
    fetch_updates = srun([f"git init -q \
                        && git config --global user.email pseudokawaii@gmail.com \
                        && git config --global user.name pseudokawaii \
                        && git add . \
                        && git commit -sm update -q \
                        && git remote add origin {UPSTREAM_REPO} \
                        && git fetch origin -q \
                        && git reset --hard origin/{UPSTREAM_BRANCH} -q"], shell=True)
    
    if fetch_updates.returncode == 0:
        log_info(f'Successfully pulled latest commits from \'{UPSTREAM_BRANCH}\' branch of {UPSTREAM_REPO}')
    else:
        log_error('Something went wrong while updating, recheck UPSTREAM_REPO variable!')