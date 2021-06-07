import logging
from bot import bot
from pyrogram import filters
from firebase_admin import db


@bot.on_message(filters.command(["start", "start@todogroup_bot"], prefixes=["/", "/"]), group=1)
async def start_command(client, message):
    chat_id = message.chat.id
    is_group_msg =message.chat.type == "group" or message.chat.type=="supergroup"
    todotype ="personaltodo"
    if is_group_msg:
        todotype ="grouptodo"
    todo_ref = db.reference("/{}/{}".format(todotype, chat_id))
    msg = await bot.create_list(todotype, message)
    todo_ref.update({"bot_msg_id": msg.message_id})
    logging.info(f"Bot msg_id updated to {msg.message_id} in {chat_id}")
    logging.info(f"User displayed a list in {todotype} in {chat_id}")