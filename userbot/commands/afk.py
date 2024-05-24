import datetime

from pyrogram import Client, filters, types

from userbot.utils.misc import modules_help, prefix
from userbot.utils.db import db


# avoid using global variables
afk_info = db.get(
    "core.afk",
    "afk_info",
    {
        "start": 0,
        "is_afk": False,
        "reason": "",
    },
)

is_afk = filters.create(lambda _, __, ___: afk_info["is_afk"])


@Client.on_message(
    is_afk
    & (filters.private | filters.mentioned)
    & ~filters.channel
    & ~filters.me
    & ~filters.bot
)
async def afk_handler(_, message: types.Message):
    start = datetime.datetime.fromtimestamp(afk_info["start"])
    end = datetime.datetime.now().replace(microsecond=0)
    afk_time = end - start
    await message.reply(
        f"**I'm AFK {afk_time}\n" f"Reason:** __{afk_info['reason']}__"
    )


@Client.on_message(filters.command("afk", prefix) & filters.me)
async def afk(_, message):
    if len(message.text.split()) >= 2:
        reason = message.text.split(" ", maxsplit=1)[1]
    else:
        reason = "None"

    afk_info["start"] = int(datetime.datetime.now().timestamp())
    afk_info["is_afk"] = True
    afk_info["reason"] = reason

    await message.edit(f"**I'm going AFK.\n" f"Reason:** __{reason}__")

    db.set("core.afk", "afk_info", afk_info)


@Client.on_message(filters.command("unafk", prefix) & filters.me)
async def unafk(_, message):
    if afk_info["is_afk"]:
        start = datetime.datetime.fromtimestamp(afk_info["start"])
        end = datetime.datetime.now().replace(microsecond=0)
        afk_time = end - start
        await message.edit(f"**I'm not AFK anymore.\n" f"I was afk {afk_time}**")
        afk_info["is_afk"] = False
    else:
        await message.edit("**You weren't afk**")

    db.set("core.afk", "afk_info", afk_info)


modules_help["afk"] = {"afk [reason]": "Go to afk", "unafk": "Get out of AFK"}