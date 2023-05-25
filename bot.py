#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
    NotSafeForWork - This bot will send a porn pic when asked.
    Copyright (C) 2023  NinjaLeft

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""


import telebot
from colorama import Fore
from io import BytesIO
import re
from random import choice
from os import listdir, path, rename, system, stat
import sys

debug = False
badArgs = ["bot.py", "./bot.py", "python"]
args = [arg for arg in sys.argv if arg not in badArgs]
API_TOKEN = "TokenFromBotFather"
try:
    if not re.fullmatch(r"^[0-9]{10}:[a-zA-Z0-9]{35}", API_TOKEN):
        API_TOKEN = input(" Bot Token: ")
    if not re.fullmatch(r"^[0-9]{10}:[a-zA-Z0-9]{35}", API_TOKEN):
        print(f"{Fore.RED} [×] Bad Token:{Fore.RESET} {API_TOKEN}")
        sys.exit(1)
except KeyboardInterrupt:
    sys.exit(0)
except:
    raise

bot = telebot.TeleBot(API_TOKEN)
cats = [
    "Artistic",
    "Athletic",
    "BDSM",
    "Cameltoe",
    "HQ",
    "Lesbian",
    "Small-Ass",
    "Small-Tits",
    "Tattoo",
    "Traps",
    "Traps Hentai",
    "Upskirt",
]

MessageCaption = ""
ProtectImage = False


def printList(iterable: list | tuple):
    text = ""
    for item in iterable:
        text += f"    {item}\n"
    return text


@bot.message_handler(commands=["start", "help"])
def start(message: telebot.types.Message):
    bot.send_message(
        message.chat.id,
        f"""Hello, User.
  You can start using the bot with these commands:
    /pic - Random Photo
    /cat [Category] - Get a pic from [Category]
    Example:
        /cat Lesbian
        /cat Tattoo

  All Categories:
{printList(cats)}""",
    )


@bot.message_handler(commands=["pic"])
def randomPic(message: telebot.types.Message):
    chatID = message.chat.id
    cat = choice(cats)
    cPath = f"./Cats/{cat}"
    contents = [file for file in listdir(cPath) if path.isfile(path.join(cPath, file))]
    contents.sort()
    ImageFileName = choice(contents)
    ImagePath = path.join(cPath, ImageFileName)
    with open(ImagePath, "rb") as file:
        ImageFile = file.read()
    if debug:
        MessageCaption = f"{cat}/{ImageFileName}"
    else:
        MessageCaption = f"Choosing image from {cat} ..."
    bot.reply_to(message, MessageCaption)
    bot.send_photo(
        chatID,
        BytesIO(ImageFile),
        protect_content=ProtectImage,
        reply_to_message_id=message.id,
        caption="Enjoy!",
    )


@bot.message_handler(regexp="/cat [a-zA-Z]{2,9}( Hentai)?")
def picFromCat(message: telebot.types.Message):
    chatID = message.chat.id
    messageText = message.text
    results = re.match(r"(/cat [a-zA-Z]{2,9}( Hentai)?)", messageText).group()
    results = results.replace("/cat ", "")
    if results in cats:
        iPath = f"./Cats/{results}"
        contents = [
            file for file in listdir(iPath) if path.isfile(path.join(iPath, file))
        ]
        contents.sort()
        ImageFileName = choice(contents)
        ImagePath = path.join(iPath, ImageFileName)
        with open(ImagePath, "rb") as file:
            ImageFile = file.read()
        if debug:
            MessageCaption = f"{results}/{ImageFileName}"
        else:
            MessageCaption = f"Choosing image from {results} ..."
        bot.reply_to(message, MessageCaption)
        bot.send_photo(
            chatID,
            BytesIO(ImageFile),
            protect_content=ProtectImage,
            reply_to_message_id=message.id,
            caption="Enjoy!",
        )
    else:
        bot.reply_to(
            message, "Category not found. You can get the list of them using /help ."
        )


@bot.message_handler(commands=["cat"])
def errorCat(message: telebot.types.Message):
    bot.reply_to(message, "No category specified. Use /help to see list of categories.")


if __name__ == "__main__":
    try:
        print(
            f"""
    NotSafeForWork  Copyright (C) 2023  NinjaLeft
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to
    redistribute it under certain conditions.
{Fore.GREEN}
\t _______    ______________________      __
\t \      \  /   _____/\_   _____/  \    /  \\
\t /   |   \ \_____  \  |    __) \   \/\/   /
\t/    |    \/        \ |     \   \        /
\t\____|__  /_______  / \___  /    \__/\  /
\t        \/        \/      \/          \/
{Fore.RESET}
"""
        )
        if "--help" in args:
            print(
                """
    --help\t\t - Show this message and exit.
    --debug\t\t - Script and bot show additional information.
    --protect=true/false\t\t - If True, removes the ability of saving/forwarding images; Taking screenshots works on pc.
        """
            )
            sys.exit(0)

        for a in args:
            if a.startswith("--protect"):
                a = a.split("=")[-1].lower()
                if "true" in a:
                    ProtectImage = True

        if "--debug" in args:
            debug = True
            print(f"sys.argv: {sys.argv}")
            print(f"Clean: {args}")
            print(f"Protect Content: {ProtectImage}")

        bot.polling(skip_pending=True, restart_on_change=True, path_to_watch=".")

    except KeyboardInterrupt:
        print(
            """
\t__________             ._.
\t\______   \___.__. ____| |
\t |    |  _<   |  |/ __ \ |
\t |    |   \\\___  \  ___/\|
\t |______  // ____|\___  >_
\t        \/ \/         \/\/
"""
        )
        bot.stop_polling()
        sys.exit(0)

    except SystemExit:
        raise

    except:
        print(Fore.RED, "*" * 10)
        print(f"Something bad happened:{Fore.RESET}")
        raise
