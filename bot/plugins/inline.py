from bot import bot
from firebase_admin import db
from .utils import Filter, inline_results, inline_results_1, msg_list_from_db

@bot.on_inline_query()
async def answer(client, inline_query):
    inline_options = []
    todotype = "personaltodo"
    # thumb_url = "https://data.alemi.dev/todo-small.png"
    thumb_url = "https://imgur.com/9nahZuY.png"
    # thumb_url = "https://imgur.com/YxvePl2.png"
    # try:
    from_usr = inline_query.from_user.id
    # except:
    #     inline_options.append(inline_results("Ooops", "You are probably an anonymous admin, you can't access inline", thumb_url))
    #     await inline_query.answer(
    #     inline_options,
    #     cache_time=1
    #     )
    #     return
    lst_name = inline_query.query
    todo_ref = db.reference("/{}/{}".format(todotype, from_usr)).get()
    if todo_ref is None:
        inline_options.append(inline_results("No tasks yet", "Please add lists in private chat first. Go to @todogroup_bot to do so", thumb_url))
    else:
        hashtag_lst = list(todo_ref.keys())
        hashtag_lst.remove('bot_msg_id')
        if len(hashtag_lst) == 0:
            inline_options.append(inline_results("No tasks yet", "Please add lists in private chat first. Go to @todogroup_bot to do so", thumb_url))
        substr = [lst_name]
        filterd_list = Filter(hashtag_lst,substr)
        if lst_name in hashtag_lst:
            msg_list, from_usr_lst = msg_list_from_db(todotype, from_usr, lst_name)
            for i, j in zip(msg_list, range(len(msg_list))):
                try:
                    inline_options.append(inline_results_1(str(j+1)+". "+i, lst_name, thumb_url))
                except Exception as e:
                    print(e)
        else:
            if(len(lst_name)==0):
                filterd_list = hashtag_lst
            for lst_name in filterd_list:
                msg_list, from_usr_lst = msg_list_from_db(todotype, from_usr, lst_name)
                listname_data =""
                for i in range(len(msg_list)):
                    listname_data += "{}. {} \n".format(i+1, msg_list[i])
                inline_options.append(inline_results(lst_name, listname_data, thumb_url))
    await inline_query.answer(
        inline_options,
        cache_time=1
    )