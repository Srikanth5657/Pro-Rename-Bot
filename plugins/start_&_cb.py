from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from plugins.check_user_status import handle_user_status
import traceback
import os
from helper.database import db
from config import Config, Txt
import humanize
from time import sleep


@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):

    if message.from_user.id in Config.BANNED_USERS:
        await message.reply_text("Sorry, You are banned.")
        return

    user = message.from_user
    await db.add_user(client, message)
    button = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            '⛅ Uᴩᴅᴀᴛᴇꜱ', url='https://t.me/CinemasMawa'),
        InlineKeyboardButton(
            '🌨️ Sᴜᴩᴩᴏʀᴛ', url='https://t.me/CinemasMawa')
    ], [
        InlineKeyboardButton('☃️ Aʙᴏᴜᴛ', callback_data='about'),
        InlineKeyboardButton('❗ Hᴇʟᴩ', callback_data='help')
    ]])
    if Config.START_PIC:
        await message.reply_photo(Config.START_PIC, caption=Txt.START_TXT.format(user.mention), reply_markup=button)
    else:
        await message.reply_text(text=Txt.START_TXT.format(user.mention), reply_markup=button, disable_web_page_preview=True)


@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def rename_start(client, message):
    file = getattr(message, message.media.value)
    filename = file.file_name
    filesize = humanize.naturalsize(file.file_size)

    try:
        text = f"""**__What do you want me to do with this file.?__**\n\n**File Name** :- `{filename}`\n\n**File Size** :- `{filesize}`"""
        buttons = [[InlineKeyboardButton("📝 𝚂𝚃𝙰𝚁𝚃 𝚁𝙴𝙽𝙰𝙼𝙴 📝", callback_data="rename")],
                   [InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="close")]]
        await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
    except FloodWait as e:
        await sleep(e.value)
        text = f"""**__What do you want me to do with this file.?__**\n\n**File Name** :- `{filename}`\n\n**File Size** :- `{filesize}`"""
        buttons = [[InlineKeyboardButton("📝 𝚂𝚃𝙰𝚁𝚃 𝚁𝙴𝙽𝙰𝙼𝙴 📝", callback_data="rename")],
                   [InlineKeyboardButton("✖️ 𝙲𝙰𝙽𝙲𝙴𝙻 ✖️", callback_data="close")]]
        await message.reply_text(text=text, reply_to_message_id=message.id, reply_markup=InlineKeyboardMarkup(buttons))
    except:
        pass



@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    if data == "start":
        await query.message.edit_text(
            text=Txt.START_TXT.format(query.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    '⛅ Uᴩᴅᴀᴛᴇꜱ', url='https://t.me/CinemasMawa'),
                InlineKeyboardButton(
                    '🌨️ Sᴜᴩᴩᴏʀᴛ', url='https://t.me/CinemasMawa')
            ], [
                InlineKeyboardButton('☃️ Aʙᴏᴜᴛ', callback_data='about'),
                InlineKeyboardButton('❗ Hᴇʟᴩ', callback_data='help')
            ]])
        )
    elif data == "help":
        await query.message.edit_text(
            text=Txt.HELP_TXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔒 Cʟᴏꜱᴇ", callback_data="close"),
                InlineKeyboardButton("◀️ Bᴀᴄᴋ", callback_data="start")
            ]])
        )
    elif data == "about":
        await query.message.edit_text(
            text=Txt.ABOUT_TXT.format(client.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("🔒 Cʟᴏꜱᴇ", callback_data="close"),
                InlineKeyboardButton("◀️ Bᴀᴄᴋ", callback_data="start")
            ]])
        )
    elif data.startswith("ban_user_"):

        user_id = data.split("_", 2)[-1]
        if Config.UPDATES_CHANNEL is None:
            await query.answer("Sorry Sir, You didn't Set any Updates Channel!", show_alert=True)
            return
        if not int(query.from_user.id) == Config.BOT_OWNER:
            await query.answer("You are not allowed to do that!", show_alert=True)
            return
        try:
            await client.kick_chat_member(chat_id=int(Config.UPDATES_CHANNEL), user_id=int(user_id))
            await query.answer("User Banned from Updates Channel!", show_alert=True)
        except Exception as e:
            await query.answer(f"Can't Ban Him!\n\nError: {e}", show_alert=True)

    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()
