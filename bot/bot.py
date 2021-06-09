import asyncio
import logging
import numpy as np
from os import path
import firebase_admin
from pyrogram import Client
from firebase_admin import db
from configparser import ConfigParser
from pyrogram.errors import FloodWait, MessageNotModified, ButtonDataInvalid, MessageEditTimeExpired
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from .plugins.utils import msg_list_from_db, create_list_buttons, InlineButtonEdit

class bot(Client):
    def __init__(self, name):
        config_file = f"{name}.ini"
        config = ConfigParser()
        config.read(config_file)
        name = name.lower()
        plugins = {'root': path.join(__package__, 'plugins')}
        api_id = config.get('pyrogram', 'api_id')
        api_hash = config.get('pyrogram', 'api_hash')
        super().__init__(
            name,
            config_file=config_file,
            workers=16,
            plugins=plugins,
            workdir="./",
        )

    async def start(self):
        await super().start()
        print("bot started. Hi.")

    async def stop(self, *args):
        await super().stop()
        print("bot stopped. Bye.")


    def create_list(self, todotype, message):
        chat_id = message.chat.id
        list_btns = create_list_buttons(todotype, chat_id)
        buttons = [[]]
        if len(list_btns[0]) == 0:
            msg = super().send_message(
                chat_id,
                "This is your to do list",
                reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Get Started Guide",
                            callback_data="additem"
                        )
                    ]
                ])
            )
        else:
            msg = super().send_message(
                chat_id,
                "This is your to do list",
                reply_markup=InlineKeyboardMarkup(buttons+list_btns)
            )
        return msg

    async def get_data(self, data, from_usr):
        lst_data = ""
        j = 1
        if len(from_usr) != 0:
            for i, k in zip(data, from_usr):
                lst_data += str(j) + "." + " "
                if isinstance(k, int):
                    usr = await super().get_users(k)
                    lst_data += i + "|" + usr.mention(style="md") + "\n"
                else:
                    usr = k
                    lst_data += i + "|" + "@misc" + "\n"
                j += 1
        else:
            for i in data:
                lst_data += str(j) + "." + " "
                lst_data += i + "\n"
                j += 1
        return lst_data

    async def show_list_in_keyboard(self, todotype, chat_id, hashtagtext, message):
        msg_list, from_usr = msg_list_from_db(todotype, chat_id, hashtagtext)
        lst_data = await self.get_data(msg_list, from_usr)
        updated_reply_msg = "This is a hashtag {} list \n".format(hashtagtext) + lst_data
        inline_msg_id_node = db.reference("/{}/{}/{}".format(todotype, chat_id,"bot_msg_id")).get("bot_msg_id")[0]
        try:
            await super().edit_message_text(chat_id, inline_msg_id_node, updated_reply_msg)
            await super().edit_message_reply_markup(
                chat_id, inline_msg_id_node,
                InlineKeyboardMarkup([
                    [
                        await InlineButtonEdit(),
                    ]
                ]))
            logging.info("Successfully added a task using /new command")
        except MessageEditTimeExpired as e:
            await super().send_message("It's been too long since you have used the /start command. Please /start@todogroup_bot to create a new inline keyboard")
        except FloodWait as e:
            await asyncio.sleep(e.x)
        except MessageNotModified as e:
            logging.info(f"Got message not modified while adding {message.message_id} in {chat_id} using /new command")
        except Exception as e:
            logging.error(f"Facing issues in adding a msg using /new command while editing inline keyboard in chat id [{chat_id}], and in msg_id {message.message_id}", exc_info=True)


