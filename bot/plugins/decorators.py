import numpy as np
from bot import bot
import re
import sys
import time
import asyncio
import logging
from pyrogram import filters
from firebase_admin import db
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from .utils import grouporprivate, msg_list_from_db, create_list_buttons, create_buttons, InlineButtonEdit, addtodoitems, remove_all_specific_element, check_is_duplicate_item, push_db
from pyrogram.errors import ButtonDataInvalid, FloodWait, MessageNotModified


@bot.on_message(group=2)
async def my_handler(client, message):
    """Handler for messages containing hashtags

    Finds whether a msg contains a hashtag or not. If yes, then processes it and saves it at appropriate place in database.
    """
    if(message.via_bot is not None):
        return
    chat_id = message.chat.id
    todotype = grouporprivate(message)
    msg_text = message.text
    if(msg_text is None):
        return
    r = re.compile(r"(?:^|\s)([#])(\w+)")
    hashtags = r.findall(msg_text)
    if(len(hashtags) == 0):
        return
    tracked_list_ref = db.reference(
        "/{}/{}/{}".format(todotype, chat_id, "trackedlist"))
    tracked_lists_not_empty = tracked_list_ref.get("trackedlist")[
        0] is not None
    try:
        if tracked_lists_not_empty:
            for i in hashtags:
                hashtagtext = i[1]
                tracked_list = msg_list_from_db(
                    todotype, chat_id, "trackedlist")[0]
                ignore_lst = msg_list_from_db(
                    todotype, chat_id, "ignore_lst")[0]
                if hashtagtext in ignore_lst:
                    return
                if hashtagtext in tracked_list:
                    is_duplicate_item = addtodoitems(
                        todotype, hashtagtext, message)[1]
                    if(is_duplicate_item):
                        return
                    await bot.show_list_in_keyboard(todotype, chat_id, hashtagtext, message)
                else:
                    try:
                        await bot.send_message(chat_id, "Currently not tracking `{}` hashtag, Please use `/tracklists {}` if you want to track this hashtag list. You can also use `/ignore hashtag_names` to avoid this message next time".format(hashtagtext, hashtagtext), parse_mode="md")
                    except FloodWait as e:
                        await asyncio.sleep(e.x)
        else:
            db_ref = db.reference("/{}/{}".format(todotype, chat_id)).get()
            if(db_ref is not None):
                await bot.send_message(chat_id, "Currently not tracking any hashtag, Please use `/tracklists hashtag_names`, hashtag_names should be separated by commas", parse_mode="md")
            else:
                await bot.send_message(chat_id, "Please start todobot using /start@todogroup_bot")
    except Exception as e:
        logging.error(
            f"trouble in adding a msg containing hashtag into list [{chat_id}]", exc_info=True)


@bot.on_message(filters.command(["start", "start@todogroup_bot"], prefixes=["/", "/"]), group=1)
async def start_command(client, message):
    """
    Write something here
    """
    chat_id = message.chat.id
    is_group_msg = message.chat.type == "group" or message.chat.type == "supergroup"
    todotype = "personaltodo"
    if is_group_msg:
        todotype = "grouptodo"
    todo_ref = db.reference("/{}/{}".format(todotype, chat_id))
    msg = await bot.create_list(todotype, message)
    todo_ref.update({"bot_msg_id": msg.message_id})
    logging.info(f"Bot msg_id updated to {msg.message_id} in {chat_id}")
    logging.info(f"User displayed a list in {todotype} in {chat_id}")


@bot.on_message(filters.command(["new", "new@todogroup_bot"]), group=1)
async def new_command(client, message):
    txt = " ".join(message.text.split(" ")[1:])
    todotype = grouporprivate(message)
    chat_id = message.chat.id
    inline_msg_id = db.reference(
        "/{}/{}/{}".format(todotype, chat_id, "bot_msg_id")).get("bot_msg_id")[0]
    if(inline_msg_id is None):
        await bot.send_message(chat_id, "Please start todobot alteast once by using /start@todogroup_bot")
        return
    txt = txt.strip()
    if len(txt) != 0:
        inline_msg_id_node = db.reference(
            "/{}/{}/{}".format(todotype, chat_id, "bot_msg_id")).get("bot_msg_id")[0]
        if(inline_msg_id_node is None):
            await bot.send_message(chat_id, "Please use /start@todogroup_bot command atleast once for using this bot")
        else:
            is_duplicate_item = addtodoitems(todotype, "newtodo", message)[1]
            if(is_duplicate_item):
                return
            await bot.show_list_in_keyboard(todotype, chat_id, "newtodo", message)


@bot.on_message(filters.command(["tracklists", "tracklists@todogroup_bot"]), group=1)
async def tracklist_handler(client, message):
    txt = " ".join(message.text.split(" ")[1:])
    chat_id = message.chat.id
    todotype = grouporprivate(message)
    inline_msg_id = db.reference(
        "/{}/{}/{}".format(todotype, chat_id, "bot_msg_id")).get("bot_msg_id")[0]
    if(inline_msg_id is None):
        await bot.send_message(chat_id, "Please start todobot alteast once by using /start@todogroup_bot")
        return
    if(len(txt) == 0):
        return
    hashtags_lst = txt.split(",")
    hashtags_lst = list(np.char.strip(hashtags_lst))
    hashtags_lst = remove_all_specific_element(hashtags_lst, " ")
    for listname in hashtags_lst:
        if len(listname) > 36:
            hashtags_lst.remove(listname)
            await bot.send_message(chat_id, "Fuck Off! What are you writing ? Ramayana")
        else:
            hash_str = "#" + listname
            matched = re.match(r"^#\w+$", hash_str)
            if not bool(matched):
                return
            else:
                push_db(todotype, message, "trackedlist", listname)
                await bot.show_list_in_keyboard(todotype, chat_id, "trackedlist", message)


@bot.on_message(filters.command(["ignore", "ignore@todogroup_bot"]), group=1)
async def ignore_handler(client, message):
    todotype = grouporprivate(message)
    chat_id = message.chat.id
    txt = " ".join(message.text.split(" ")[1:])
    inline_msg_id = db.reference(
        "/{}/{}/{}".format(todotype, chat_id, "bot_msg_id")).get("bot_msg_id")[0]
    if(inline_msg_id is None):
        await bot.send_message(chat_id, "Please start todobot alteast once by using /start@todogroup_bot")
        return
    if(len(txt) == 0):
        return
    hashtags_lst = txt.split(",")
    hashtags_lst = list(np.char.strip(hashtags_lst))
    hashtags_lst = remove_all_specific_element(hashtags_lst, " ")
    tracked_hashtags = msg_list_from_db(todotype, chat_id, "trackedlist")[0]
    for i in hashtags_lst:
        if i in tracked_hashtags:
            await bot.send_message(chat_id, f"Uh-oh there is a clash, `{i}` is already in tracked lists")
        else:
            push_db(todotype, message, "ignore_lst", i)
    await bot.show_list_in_keyboard(todotype, chat_id, "ignore_lst", message)


@bot.on_message(filters.command(["showtrackedlists", "showtrackedlists@todogroup_bot"]), group=1)
async def tracked(client, message):
    chat_id = message.chat.id
    todotype = grouporprivate(message)
    inline_msg_id = db.reference(
        "/{}/{}/{}".format(todotype, chat_id, "bot_msg_id")).get("bot_msg_id")[0]
    if(inline_msg_id is None):
        await bot.send_message(chat_id, "Please start todobot alteast once by using /start@todogroup_bot")
        return
    todo_ref = db.reference("/{}/{}".format(todotype, chat_id)).get()
    if(todo_ref is None):
        await bot.send_message(chat_id, "Currently no hashtag is tracked, Use /start followed by `/tracklists hashtag1,hashtag2` for tracking hashtags", parse_mode="md")
        return
    tracked_hashtags = msg_list_from_db(todotype, chat_id, "trackedlist")[0]
    if(len(tracked_hashtags) == 0):
        await bot.send_message(chat_id, "Currently no hashtag is tracked, use `/tracklists hashtag1,hashtag2` for tracking hashtags", parse_mode="md")
    else:
        i = 1
        tracked_lists = "You are tracking following lists - \n"
        tracked_lists += ">>> "

        for hashtag in tracked_hashtags:
            if tracked_hashtags[-1] == hashtag:
                tracked_lists += hashtag
            else:
                tracked_lists += hashtag + ","
            i += 1
        await bot.send_message(chat_id, tracked_lists, parse_mode="md")


@bot.on_message(filters.command(["help", "help@todogroup_bot"]), group=1)
async def help_handler(client, message):
    await bot.send_message(message.chat.id, "/start@todogroup_bot - Shows all available lists and starts the bot for first time. Watch [this](https://t.me/help_todogroup_bot/5)\n/tracklists@todogroup_bot - Enter a hashtag name, enter multiple hashtag names separated by comma to track messages associated with a certain hashtag to be added in a list. Watch [this](https://t.me/help_todogroup_bot/5) \n/new@todogroup_bot - Creates a new task in a separate list named 'newtodo' independent of hashtags. Watch [this](https://t.me/help_todogroup_bot/5) \n/showtrackedlists@todogroup_bot - Shows all the lists which are being tracked for new additions \n/ignore@todogroup_bot Ignore messages with certain hashtags to be ignored by bot. Input format is same as /tracklists. \n/delete@todogroup_bot - Deletes a single list or all lists in one go. Please type list names separated by commas to delete multiple lists or type 'Delete All' to delete all lists except trackedlist \n/help@todogroup_bot - let's you know more on how to use this bot.\n\nHelp [channel](https://t.me/help_todogroup_bot) and Help [group](https://t.me/help_todogroup_chat) for usage, help, suggestions, etc.", parse_mode="md", disable_web_page_preview=True)


@bot.on_message(filters.command(["delete", "delete@todogroup_bot"]), group=1)
async def delete_handler(client, message):
    msg_text = " ".join(message.text.split(" ")[1:])
    chat_id = message.chat.id
    todotype = grouporprivate(message)
    inline_msg_id = db.reference(
        "/{}/{}/{}".format(todotype, chat_id, "bot_msg_id")).get("bot_msg_id")[0]
    if(inline_msg_id is None):
        await bot.send_message(chat_id, "Please start todobot alteast once by using /start@todogroup_bot")
        return
    if len(msg_text) == 0:
        return
    delete_items = msg_text.split(",")
    delete_items = remove_all_specific_element(delete_items, " ")

    if type(delete_items) is list:
        for item in delete_items:
            if item == "Delete All":
                for i in db.reference("/{}/{}".format(todotype, chat_id)).get().items():
                    key = i[0]
                    if key != "bot_msg_id" and key != "trackedlist" and key != "ignore_lst":
                        todo_lsts = db.reference(
                            "/{}/{}/{}".format(todotype, chat_id, key))
                        todo_lsts.set({})
            else:
                todo_ref = db.reference(
                    "/{}/{}/{}".format(todotype, chat_id, item))
                todo_ref.set({})
    else:
        todo_ref = db.reference(
            "/{}/{}/{}".format(todotype, chat_id, delete_items))
        todo_ref.set({})
    await start_command(client, message)


no_msg_in_cbq = filters.create(
    lambda flt, client, query: query.message is None)


@bot.on_callback_query(no_msg_in_cbq)
async def pass_handler(client, callback_query):
    await callback_query.answer("It's been 48 hours since you have last used /start. Please use /start@todogroup_bot for changes to reflect in Keyboard", show_alert=True)


@bot.on_callback_query()
async def callback_handler(client, callback_query):
    callbackdata = callback_query.data
    todotype = grouporprivate(callback_query.message)
    chat_id = callback_query.message.chat.id
    msg_id = callback_query.message.message_id
    bot_msg_id = db.reference(
        "/{}/{}/{}".format(todotype, chat_id, "bot_msg_id")).get()
    get_lists = db.reference("/{}/{}".format(todotype, chat_id)).get().items()
    keys = []
    for key, value in get_lists:
        if key != "bot_msg_id":
            keys.append(key)
    if msg_id == bot_msg_id:
        if callbackdata in keys:
            msg_list, from_usr = msg_list_from_db(
                todotype, chat_id, callbackdata)
            lst_data = await bot.get_data(msg_list, from_usr)
            try:
                await bot.edit_message_text(chat_id, msg_id, "This is a hashtag **{}** list \n————————————————————\n".format(callbackdata) + lst_data, parse_mode="md")
                await bot.edit_message_reply_markup(
                    chat_id, msg_id,
                    InlineKeyboardMarkup([
                        [
                            await InlineButtonEdit()
                        ]
                    ]))
                logging.info(
                    f"Successfully shown the {callbackdata} list to user")

            except Exception as e:
                logging.error(
                    f"Facing issues in editing inline keyboard while showing {callbackdata} list in chat_id {chat_id}", exc_info=True)
        elif callbackdata == "edit":
            find_it = re.search(
                r"This is a hashtag [\w]+ list", callback_query.message.text)
            hashtag = find_it.group(0).split(" ")[4]
            buttons = create_buttons(todotype, chat_id, hashtag)
            list_btns = create_list_buttons(todotype, chat_id)
            try:
                await bot.edit_message_text(chat_id, msg_id, "Click a task to delete or Click on a list name to open it")
                await bot.edit_message_reply_markup(
                    chat_id, msg_id,
                    InlineKeyboardMarkup(buttons+list_btns))
                logging.info(
                    "Successfully shown user with edit list interface")
            except ButtonDataInvalid as e:
                logging.info(
                    f"The button callback data contains invalid data or exceeds 64 bytes {value} in {hashtag}")
                sze = sys.getsizeof(key + "___" + hashtag)
                logging.info(
                    f"{sze} is the number of bytes for {key + '___' + hashtag}")
            except Exception as e:
                logging.error(
                    f"Facing issues in showing inline keyboard while clicking edit list button msg_id, chat_id {msg_id} {chat_id}]", exc_info=True)
        elif callbackdata == "additem":
            await help_handler(client, callback_query.message)
        else:
            key, hashtag = callbackdata.split('___')
            todo_ref = db.reference(
                "/{}/{}/{}".format(todotype, chat_id, hashtag))
            if(todo_ref.get() is not None):
                msg_keys = todo_ref.get().keys()
                if key in msg_keys:
                    todo_ref.child(key).set({})
            buttons = create_buttons(todotype, chat_id, hashtag)
            list_btns = create_list_buttons(todotype, chat_id)
            try:
                if(len((buttons+list_btns)[0]) == 0):
                    await bot.edit_message_text(chat_id, msg_id, "You don't have anything to delete. Please /start to use the bot")
                else:
                    await bot.edit_message_reply_markup(
                        chat_id, msg_id,
                        InlineKeyboardMarkup(buttons+list_btns)
                    )
                    logging.info(f"Successfully deleted msg with keyclick")
            except ButtonDataInvalid as e:
                logging.info(
                    f"The button callback data contains invalid data or exceeds 64 bytes {value} in {hashtag}")
                sze = sys.getsizeof(key + "___" + hashtag)
                logging.info(
                    f"{sze} is the number of bytes for {key + '___' + hashtag}")
            except FloodWait as e:
                await callback_query.answer(f"Uh-oh...Slow down, Please wait {e.x} seconds to get refreshed view", show_alert=True)
                time.sleep(e.x)
            except MessageNotModified as e:
                logging.info(
                    f"Got message not modified while deleting. {msg_id} and {chat_id}")
            except Exception as e:
                logging.critical(
                    f"Facing issues in deletion of tasks in a list in {msg_id} in {chat_id}", exc_info=True)

    else:
        try:
            await callback_query.answer("You have issued a more recent list using start command, Please maintain list there or use /start to display the list", show_alert=True)
        except Exception as e:
            logging.info(
                'there was some error in using callback_query.answer while using old inline keyboard')
