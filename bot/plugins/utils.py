from bot import bot
from firebase_admin import db
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import re
import numpy as np

def InlineButtonList(msg_key, msg):
    return eval("InlineKeyboardButton(msg, callback_data=msg_key)")

def InlineButtonKey(task):
    return eval("InlineKeyboardButton(task, callback_data=task)")

async def InlineButtonEdit():
    return eval("InlineKeyboardButton('Edit list/Show lists', callback_data='edit')")

def Filter(string, substr):
    return [str for str in string if any(sub in str for sub in substr)]



def get_data(data):
    lst_data = ""
    j = 1
    for i in data:
        lst_data += str(j) + "." + " "
        lst_data += i + "\n"
        j += 1
    return lst_data


def grouporprivate(message):
    isgroup_msg = message.chat.type == "group" or message.chat.type == "supergroup"
    typelist = "personaltodo"
    if isgroup_msg:
        typelist = "grouptodo"
    return typelist

def check_is_duplicate_item(todotype,chat_id,hashtagtext,new_msg):
    todo_hashtag_ref = db.reference("/{}/{}/{}".format(todotype,chat_id,hashtagtext))
    if todo_hashtag_ref.get() is not None:
        for key,value in todo_hashtag_ref.get().items():
            if(value["msg"] == new_msg):
                return True
    return False

def remove_all_specific_element(arr,item):
    return [item_i for item_i in  arr if item_i!=item]

def push_db(todotype, message, hashtagtext, msg_text):
    is_duplicate_item=False
    chat_id = message.chat.id
    msg_from = message.from_user.id
    todo_hashtag_ref = db.reference("/{}/{}/{}".format(todotype, chat_id, hashtagtext))
    has_this_hashtag = todo_hashtag_ref.get(hashtagtext)[0] is not None
    todo_ref = db.reference("/{}/{}".format(todotype,chat_id))
    msg_id = message.message_id
    msg_meta_details = {
        "msg_id" : msg_id,
        "msg_from" : msg_from,
        "msg" : msg_text,
    }
    if has_this_hashtag:
        if check_is_duplicate_item(todotype, chat_id, hashtagtext, msg_text):
            is_duplicate_item = True
        else:
            todo_hashtag_ref.push(msg_meta_details)
    else:
        todo_hashtag_ref.push(msg_meta_details)
    return todo_ref,is_duplicate_item

def addtodoitems(todotype, hashtagtext, message):
    msg_from = message.from_user.id
    is_duplicate_item = False
    if hashtagtext == "newtodo":
        msg_text_list = message.text.split(' ')[1:]
        msg_text_list = list(np.char.strip(msg_text_list, " "))
        msg_text_list = remove_all_specific_element(msg_text_list, "")     
        msg_text = " ".join(msg_text_list)
    else:
        msg_text_list = message.text.split(" ")
        msg_text_list = list(np.char.strip(msg_text_list, " "))
        msg_text_list = remove_all_specific_element(msg_text_list, "")     
        msg_text = " ".join(msg_text_list)
    chat_id = message.chat.id
    todo_ref,is_duplicate_item = push_db(todotype, message, hashtagtext, msg_text)
    pastmessages = todo_ref.get(hashtagtext)[0][hashtagtext]
    pastmessages_keys = list(pastmessages.keys())
    return pastmessages_keys, is_duplicate_item


def create_list_buttons(todotype, chat_id):
    list_btns = []
    get_lists = db.reference("/{}/{}".format(todotype, chat_id)).get()
    if(get_lists is None):
        return [[]]
    i = 1
    temp_lst = []
    for key, value in get_lists.items():
        if key != "bot_msg_id":
            if i%3 != 0:
                temp_lst.append(InlineButtonKey(key))
            elif i%3 == 0:
                temp_lst.append(InlineButtonKey(key))
                list_btns.append(temp_lst)
                temp_lst = []
            i += 1
    if len(temp_lst) != 0:
        list_btns.append(temp_lst)
    if len(list_btns) == 0:
        return [[]]
    return list_btns
            
def create_buttons(todotype, chat_id, hashtag):
    buttons = []
    entries = db.reference("/{}/{}/{}".format(todotype, chat_id, hashtag)).get()
    if entries != None:
        for key,value in entries.items():
            buttons.append([InlineButtonList((key + "___" + hashtag).encode(), value["msg"])])
    return buttons



def msg_list_from_db(todotype, chat_id, hashtag):
    entries = db.reference("/{}/{}/{}".format(todotype, chat_id, hashtag)).get()
    msg_list =[]
    if entries is None:
        return msg_list
    for key, value in entries.items():
        msg_list.append(value["msg"])
    return msg_list

def inline_results(title, task, thumb_link):
    return eval("InlineQueryResultArticle(title=title, input_message_content=InputTextMessageContent(task), thumb_url=thumb_link, description=task)")
def inline_results_1(title, task, thumb_link):
    return eval("InlineQueryResultArticle(title=title, input_message_content=InputTextMessageContent(title), thumb_url=thumb_link, description=task)")


