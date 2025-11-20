import asyncio
import os
import shutil
import socket
from datetime import datetime

import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from pyrogram import filters

import config
from SONALI_MUSIC import app
from SONALI_MUSIC.misc import HAPP, SUDOERS, XCB
from SONALI_MUSIC.utils.database import (
    get_active_chats,
    remove_active_chat,
    remove_active_video_chat,
)
from SONALI_MUSIC.utils.decorators.language import language
from SONALI_MUSIC.utils.pastebin import SonaBin

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


async def is_heroku():
    return "heroku" in socket.getfqdn()


# ---------------- LOGS ---------------- #
@app.on_message(
    filters.command(["getlog", "logs", "getlogs"], prefixes=["/", "!", "%", ",", ".", "@", "#"])
    & filters.user(SUDOERS)
)
@language
async def log_(client, message, _):
    try:
        await message.reply_document(document="log.txt")
    except:
        await message.reply_text(_["server_1"])


# ---------------- UPDATE / GITPULL ---------------- #
@app.on_message(
    filters.command(["update", "gitpull"], prefixes=["/", "!", "%", ",", ".", "@", "#"])
    & filters.user(SUDOERS)
)
@language
async def update_(client, message, _):

    if await is_heroku() and HAPP is None:
        return await message.reply_text(_["server_2"])

    response = await message.reply_text(_["server_3"])

    try:
        repo = Repo()
    except GitCommandError:
        return await response.edit(_["server_4"])
    except InvalidGitRepositoryError:
        return await response.edit(_["server_5"])

    os.system(f"git fetch origin {config.UPSTREAM_BRANCH} &> /dev/null")
    await asyncio.sleep(5)

    updates = ""
    repo_url = repo.remotes.origin.url.split(".git")[0]

    for commit in repo.iter_commits(f"HEAD..origin/{config.UPSTREAM_BRANCH}"):
        day = int(datetime.fromtimestamp(commit.committed_date).strftime('%d'))
        date = datetime.fromtimestamp(commit.committed_date).strftime('%b %Y')
        updates += f"• <a href='{repo_url}/commit/{commit.hexsha}'>{commit.summary}</a> — {day} {date}\n"

    if not updates:
        return await response.edit(_["server_6"])

    if len(updates) > 4000:
        link = await SonaBin(updates)
        await response.edit(f"Updates too long, check here:\n{link}")
    else:
        await response.edit(updates, disable_web_page_preview=True)

    os.system("git stash &> /dev/null && git pull")

    # notify chats
    try:
        active = await get_active_chats()
        for chat in active:
            try:
                await app.send_message(chat, _["server_8"].format(app.mention))
                await remove_active_chat(chat)
                await remove_active_video_chat(chat)
            except:
                pass
        await response.edit(f"{updates}\n\n{_['server_7']}")
    except:
        pass

    # Restart bot
    if await is_heroku():
        try:
            os.system(
                f"{XCB[5]} {XCB[7]} {XCB[9]}{XCB[4]}{XCB[0]*2}"
                f"{XCB[6]}{XCB[4]}{XCB[8]}{XCB[1]}{XCB[5]}"
                f"{XCB[2]}{XCB[6]}{XCB[2]}{XCB[3]}{XCB[0]}"
                f"{XCB[10]}{XCB[2]}{XCB[5]} {XCB[11]}{XCB[4]}{XCB[12]}"
            )
            return
        except Exception as err:
            await response.edit(f"{updates}\n\n{_['server_9']}")
            return await app.send_message(
                config.LOGGER_ID,
                _["server_10"].format(err),
            )
    else:
        os.system("pip3 install -r requirements.txt")
        os.kill(os.getpid(), 9)


# ---------------- RESTART ---------------- #
@app.on_message(
    filters.command(["restart"], prefixes=["/", "!", "%", ",", ".", "@", "#"])
    & filters.user(SUDOERS)
)
async def restart_(_, message):

    response = await message.reply_text("Restarting...")

    active = await get_active_chats()
    for chat in active:
        try:
            await app.send_message(
                chat,
                f"{app.mention} is restarting… Please wait 15-20 seconds."
            )
            await remove_active_chat(chat)
            await remove_active_video_chat(chat)
        except:
            pass

    for folder in ["downloads", "raw_files", "cache"]:
        try:
            shutil.rmtree(folder)
        except:
            pass

    await response.edit("Restart process started…")

    os.kill(os.getpid(), 9)
