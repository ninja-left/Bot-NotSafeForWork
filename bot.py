#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
    PhBox_Bot - This bot will send a porn pic when asked.
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
from os import listdir, path, rename
import sys

debug = False
args = [arg for arg in sys.argv if arg not in ["bot.py", "./bot.py", "python"]]
API_TOKEN = "6136389534:AAH-HdT_L2Z82SeWjXqym3VHkoxWNKmVXsw"
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
bannedCats = [
    "Clothing",
    "Company",
    "Cum",
    "Pornstar",
    "Position",
]  # These categories have subdirs instead of files.
MessageCaption = ""


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
    All commands:
    /pic - Random Photo
    /cat [Category Name] - Get a pic from [Category Name]

    Categories Names:
{printList(cats)}

Have a nice day!
""",
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
    ImageFile = open(ImagePath, "rb").read()
    if debug:
        MessageCaption = f"{cat}/{ImageFileName}"
    else:
        MessageCaption = f"Choosing image from {cat} ..."
    bot.reply_to(message, MessageCaption)
    bot.send_photo(
        chatID,
        BytesIO(ImageFile),
        protect_content=True,
        reply_to_message_id=message.id,
        caption="Enjoy!",
    )


@bot.message_handler(regexp="/cat [a-zA-Z]{2,9}( Hentai)?")
def picFromCat(message: telebot.types.Message):
    chatID = message.chat.id
    messageText = message.text
    results = re.match(r"(/cat [a-zA-Z]{2,9}( Hentai)?)", messageText).group()
    results = results.replace("/cat ", "")
    if results in cats or results in bannedCats:
        if results not in bannedCats:
            iPath = f"./Cats/{results}"
            contents = [
                file for file in listdir(iPath) if path.isfile(path.join(iPath, file))
            ]
            contents.sort()
            ImageFileName = choice(contents)
            ImagePath = path.join(iPath, ImageFileName)
            ImageFile = open(ImagePath, "rb").read()
            if debug:
                MessageCaption = f"{results}/{ImageFileName}"
            else:
                MessageCaption = f"Choosing image from {results} ..."
            bot.reply_to(message, MessageCaption)
            bot.send_photo(
                chatID,
                BytesIO(ImageFile),
                protect_content=True,
                reply_to_message_id=message.id,
                caption="Enjoy!",
            )
        else:
            bot.reply_to(
                message,
                "This category is not implemented yet; End-User (You) cannot access it.",
            )
    else:
        bot.reply_to(
            message, "Category not found. You can get the list of them using /help ."
        )


@bot.message_handler(commands=["cat"])
def errorCat(message: telebot.types.Message):
    bot.reply_to(message, "No category specified. Use /help to see list of categories.")


if __name__ == "__main__":
    # Running the script with --debug will add the Category/FileName to the photo caption.
    try:
        print(
            f"""
    PhBox  Copyright (C) 2023  NinjaLeft
    This program comes with ABSOLUTELY NO WARRANTY.
    This is free software, and you are welcome to
    redistribute it under certain conditions.
{Fore.GREEN}\t______ _    ______
\t| ___ \ |   | ___ \ 
\t| |_/ / |__ | |_/ / _____  __
\t|  __/| '_ \| ___ \/ _ \ \/ /
\t| |   | | | | |_/ / (_) >  <
\t\_|   |_| |_\____/ \___/_/\_\ 
{Fore.RESET}
"""
        )
        if "--debug" in args:
            debug = True
            print(f"sys.argv: {sys.argv}")
            print(f"Clean: {args}")
        bot.polling()
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
    except:
        print(Fore.RED, "*" * 10)
        print(f"Something bad happened:{Fore.RESET}")
        raise
