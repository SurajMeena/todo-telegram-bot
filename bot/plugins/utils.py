import requests
from bs4 import BeautifulSoup
import numpy as np
import re, json, logging
from firebase_admin import db
# from youtubesearchpython import *
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

def InlineButtonList(msg_key, msg):
    return eval("InlineKeyboardButton(msg, callback_data=msg_key)")

def InlineButtonKey(task):
    return eval("InlineKeyboardButton(task, callback_data=task)")

async def InlineButtonEdit():
    return eval("InlineKeyboardButton('Edit list/Show lists', callback_data='edit')")

async def InlineButtonInline():
    return eval("InlineKeyboardButton('Use Inline', switch_inline_query_current_chat='')")

async def InlineButtonGroup(info):
    return eval("InlineKeyboardButton(info, url='https://t.me/messtotelebot')")

def Filter(string, substr):
    return [stri for stri in string if any(sub in stri for sub in substr)]

def grouporprivate(message):
    isgroup_msg = message.chat.type == "group" or message.chat.type == "supergroup"
    typelist = "personaltodo"
    if isgroup_msg:
        typelist = "grouptodo"
    return typelist

def check_is_duplicate_item(todotype,chat_id,hashtagtext,new_msg):
    todo_hashtag_ref = db.reference("/{}/{}/{}".format(todotype, chat_id, hashtagtext))
    if todo_hashtag_ref.get() is not None:
        for i in todo_hashtag_ref.get().items():
            value = i[1]
            if(value["msg"] == new_msg):
                return True
    return False

def remove_all_specific_element(arr,item):
    return [item_i for item_i in  arr if item_i!=item]

def push_db(todotype, message, hashtagtext, msg_text):
    is_duplicate_item = False
    msg_from = "misc"
    chat_id = message.chat.id
    # try and except for handling anonymous user
    try:
        msg_from = message.from_user.id
    except AttributeError:
        msg_from = "anonymous"
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
    return todo_ref, is_duplicate_item

def show_webpage_info(msg_text):
    matched = re.findall('https?://\S+', msg_text)
    for url in matched:
        try:
            # making requests instance
            reqs = requests.get(url)
            # using the BeaitifulSoup module
            soup = BeautifulSoup(reqs.text, 'html.parser')
            # displaying the title
            title = soup.find('title').text
            msg_text = msg_text.replace(url, f"[{title}]({url})")
        except Exception as e:
            logging.error(f"Unable to find title for {url}", exc_info=True)
    return msg_text

def addtodoitems(todotype, hashtagtext, message):
    is_duplicate_item = False
    if hashtagtext == "newtodo":
        msg_text_list = message.text.markdown.split(' ')[1:]
        msg_text_list = list(np.char.strip(msg_text_list, " "))
        msg_text_list = remove_all_specific_element(msg_text_list, "")     
        msg_text = " ".join(msg_text_list)
    else:
        msg_text_list = message.text.markdown.split(" ")
        msg_text_list = list(np.char.strip(msg_text_list, " "))
        msg_text_list = remove_all_specific_element(msg_text_list, "")     
        msg_text = " ".join(msg_text_list)
    
    # pattern = re.findall(r"((?:https?:\/\/)?(www\.)?youtube\.com\S+?v=\S+)", msg_text)
    # for link in pattern:
    #     try:
    #         print(link[0])
    #         video = Video.getInfo(link[0], mode=ResultMode.json)
    #         x = json.loads(video)
    #         msg_text = msg_text.replace(link[0], f"[{x['title']}]({link[0]})")
    #         logging.info("created a markup link from url in msg")
    #     except:
    #         logging.error(f"Couldn't create a markup link for {link}", exc_info=True)
    # from bot.bot_file import bot_cls
    # web_page_info = bot_cls.show_webpage_info(message)
    # if len(web_page_info) != 0:
    #     pattern = re.findall(web_page_info[0])
    #     for link in pattern:
    #         try:
    #             msg_text = msg_text.replace(web_page_info[0], f"[{web_page_info[2]}]({web_page_info[1]})")
    #             logging.info("created a markup link from url in msg")
    #         except:
    #             logging.error(f"Couldn't create a markup link for {link}", exc_info=True)
    # above one only possible for userbots
    msg_text = show_webpage_info(msg_text)
    todo_ref, is_duplicate_item = push_db(todotype, message, hashtagtext, msg_text)
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
    for j in get_lists.items():
        key = j[0]
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
        for key, value in entries.items():
            buttons.append([InlineButtonList((key + "___" + hashtag).encode(), value["msg"])])
    return buttons


def msg_list_from_db(todotype, chat_id, hashtag):
    entries = db.reference("/{}/{}/{}".format(todotype, chat_id, hashtag)).get()
    msg_list = []
    from_usr = []
    if entries is None:
        return msg_list, from_usr
    for i in entries.items():
        value = i[1]
        msg_list.append(value["msg"])
        if todotype == "grouptodo":
            from_usr.append(value["msg_from"])
    return msg_list, from_usr

def inline_results(title, task, thumb_link):
    return eval("InlineQueryResultArticle(title=title, input_message_content=InputTextMessageContent(task), thumb_url=thumb_link, description=task)")

def inline_results_1(title, task, thumb_link):
    return eval("InlineQueryResultArticle(title=title, input_message_content=InputTextMessageContent(title), thumb_url=thumb_link, description=task)")



