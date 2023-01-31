from signal import signal, SIGINT
from os import path as ospath, remove as osremove, execl as osexecl, environ
from subprocess import run as srun, check_output
from psutil import disk_usage, cpu_percent, swap_memory, cpu_count, virtual_memory, net_io_counters, boot_time
from time import time
from sys import executable
from telegram.ext import CommandHandler
from telegram.error import Conflict

from bot import bot, dispatcher, updater, botStartTime, LOGGER, Interval, main_loop
from .helper.ext_utils.bot_utils import get_readable_time, get_readable_file_size
from .helper.telegram_helper.bot_commands import BotCommands
from .helper.telegram_helper.message_utils import sendMessage, editMessage, sendLogFile
from .helper.telegram_helper.filters import CustomFilters
from .helper.telegram_helper.button_build import ButtonMaker
from .modules import list, cancel_mirror, clone, delete, count, mirror_status


def stats(update, context):
    total, used, free, disk = disk_usage('/')
    swap = swap_memory()
    memory = virtual_memory()
    stats = f'<b>Bot Uptime:</b> {get_readable_time(time() - botStartTime)}\n'\
            f'<b>OS Uptime:</b> {get_readable_time(time() - boot_time())}\n\n'\
            f'<b>Total Disk Space:</b> {get_readable_file_size(total)}\n'\
            f'<b>Used:</b> {get_readable_file_size(used)} | <b>Free:</b> {get_readable_file_size(free)}\n\n'\
            f'<b>Upload:</b> {get_readable_file_size(net_io_counters().bytes_sent)}\n'\
            f'<b>Download:</b> {get_readable_file_size(net_io_counters().bytes_recv)}\n\n'\
            f'<b>CPU:</b> {cpu_percent(interval=0.5)}%\n'\
            f'<b>RAM:</b> {memory.percent}%\n'\
            f'<b>DISK:</b> {disk}%\n\n'\
            f'<b>Physical Cores:</b> {cpu_count(logical=False)}\n'\
            f'<b>Total Cores:</b> {cpu_count(logical=True)}\n\n'\
            f'<b>SWAP:</b> {get_readable_file_size(swap.total)} | <b>Used:</b> {swap.percent}%\n'\
            f'<b>Memory Total:</b> {get_readable_file_size(memory.total)}\n'\
            f'<b>Memory Free:</b> {get_readable_file_size(memory.available)}\n'\
            f'<b>Memory Used:</b> {get_readable_file_size(memory.used)}\n'
    sendMessage(stats, context.bot, update.message)

def start(update, context):
    buttons = ButtonMaker()
    buttons.buildbutton("Repo", "https://www.github.com/culturecloud/gdrive-clone-bot")
    buttons.buildbutton("Support", "https://t.me/pseudokawaii")
    reply_markup = buttons.build_menu(2)
    if CustomFilters.authorized_user(update) or CustomFilters.authorized_chat(update):
        start_string = f'''
This bot can help you clone, delete, list Google Drive files/folders (public/private with access). Service accounts, index link generation supported.\n\nType /{BotCommands.HelpCommand} to get a list of available commands
'''
        sendMessage(start_string, context.bot, update.message, reply_markup)
    else:
        sendMessage('Not an Authorized user, deploy your own clone bot', context.bot, update.message, reply_markup)

def restart(update, context):
    restart_message = sendMessage("Restarting...", context.bot, update.message)
    LOGGER.info("Stopping HTTP server ...")
    srun(["pkill", "-9", "-f", "gunicorn"])
    
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
            LOGGER.info(f'Successfully pulled latest commits from \'{UPSTREAM_BRANCH}\' branch of {UPSTREAM_REPO}')
        else:
            LOGGER.error('Something went wrong while updating, recheck UPSTREAM_REPO variable!')
            
    with open(".restartmsg", "w") as f:
        f.truncate(0)
        f.write(f"{restart_message.chat.id}\n{restart_message.message_id}\n")
    osexecl(executable, executable, "-m", "bot")

def ping(update, context):
    start_time = int(round(time() * 1000))
    reply = sendMessage("Starting Ping", context.bot, update.message)
    end_time = int(round(time() * 1000))
    editMessage(f'{end_time - start_time} ms', reply)

def log(update, context):
    sendLogFile(context.bot, update.message)

help_string = f'''
<b><u>Google Drive</u></b>
/{BotCommands.CloneCommand} [drive_url] - Copy file/folder to Google Drive.
/{BotCommands.CountCommand} [drive_url] - Count file/folder of Google Drive.
/{BotCommands.DeleteCommand} [drive_url] - Delete file/folder from Google Drive (Only Owner & Sudo).
/{BotCommands.ListCommand} [query] - Search in Google Drive(s).

<b><u>Task Control</u></b>
/{BotCommands.CancelMirror} - Cancel task by gid or reply.
/{BotCommands.CancelAllCommand} [query] - Cancel all [status] tasks.
/{BotCommands.StatusCommand} - Shows a status of all the downloads.

<b><u>Bot Control</u></b>
/{BotCommands.LogCommand} - Get a log file of the bot. Handy for getting crash reports (Owner Only).
/{BotCommands.PingCommand} - Check how long it takes to Ping the Bot (Owner Only).
/{BotCommands.RestartCommand} - Restart and update the bot (Owner Only).
/{BotCommands.StatsCommand} - Show stats of the machine where the bot is hosted in.

NOTE: <i>Try each command without any argument to see more detalis.</i>
'''

def bot_help(update, context):
    sendMessage(help_string, context.bot, update.message)
    
def duplicate_instance_handler(update, context):
    if isinstance(context.error, Conflict):
        LOGGER.warning("Duplicate instance detected! If this bot was deployed on Render, you can ignore this.")

def main():
    if ospath.isfile(".restartmsg"):
        with open(".restartmsg") as f:
            chat_id, msg_id = map(int, f)
        try:
            bot.edit_message_text("Restarted Successfully!", chat_id, msg_id)
        except:
            pass
        osremove(".restartmsg")
    start_handler = CommandHandler(BotCommands.StartCommand, start)
    restart_handler = CommandHandler(BotCommands.RestartCommand, restart,
                                        filters=CustomFilters.owner_filter)
    ping_handler = CommandHandler(BotCommands.PingCommand, ping,
                               filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    log_handler = CommandHandler(BotCommands.LogCommand, log, filters=CustomFilters.owner_filter)
    help_handler = CommandHandler(BotCommands.HelpCommand, bot_help,
                               filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)
    stats_handler = CommandHandler(BotCommands.StatsCommand, stats,
                               filters=CustomFilters.authorized_chat | CustomFilters.authorized_user)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(restart_handler)
    dispatcher.add_handler(ping_handler)
    dispatcher.add_handler(log_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(stats_handler)
    
    dispatcher.add_error_handler(duplicate_instance_handler)
    
    updater.start_polling()
    
    LOGGER.info("Bot Started!")

main()
main_loop.run_forever()
