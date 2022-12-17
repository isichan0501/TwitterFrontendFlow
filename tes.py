from TwitterFrontendFlow.TwitterFrontendFlow import TwitterFrontendFlow, check_shadowban


import pprint
from importlib import reload
import glob
import random
import os
import time



screen_name = 'thorndike_ed'
password='majika19940909'


filepath = f'./db/{screen_name}.json'

# cks = glob.glob('./db/*.json')

# filepath = random.choice(cks)
name='myname'

description="""prof"""

location='jp'
prof = dict()
prof = {
        'birthdate_year': '{}'.format(random.randint(1990,2000)),
        'birthdate_month': '{}'.format(random.randint(1,12)),
        'birthdate_day': '{}'.format(random.randint(1,28)),
        'birthdate_visibility': 'self',
        'birthdate_year_visibility': 'self',
        'displayNameMaxLength': 50,
        'birthdate_year_visibility': 'self',
        'name': name,
        'description': description,
        'location': location
        }




#ログインフロー

flow = TwitterFrontendFlow()

print(
"""login: ログイン
password_reset: パスワードリセット
load: cookieのロード""")

action = input()

if action == "login":
    flow.login_flow()
    flow.LoginJsInstrumentationSubtask()
    print(flow.get_subtask_ids())
    if "LoginEnterUserIdentifierSSO" in flow.get_subtask_ids():
        print("Telephone number / Email address / User name")
        flow.LoginEnterUserIdentifierSSO(input())
        print(flow.get_subtask_ids())
    if "LoginEnterAlternateIdentifierSubtask" in flow.get_subtask_ids():
        print(flow.content["subtasks"][0]["enter_text"]["primary_text"]["text"])
        flow.LoginEnterAlternateIdentifierSubtask(input())
        print(flow.get_subtask_ids())
    if "LoginEnterPassword" in flow.get_subtask_ids():
        print(flow.content["subtasks"][0]["enter_password"]["primary_text"]["text"])
        flow.LoginEnterPassword(input())
        print(flow.get_subtask_ids())
    if "AccountDuplicationCheck" in flow.get_subtask_ids():
        flow.AccountDuplicationCheck()
        print(flow.get_subtask_ids())
    if "LoginTwoFactorAuthChallenge" in flow.get_subtask_ids():
        print(flow.content["subtasks"][0]["enter_text"]["header"]["primary_text"]["text"])
        flow.LoginTwoFactorAuthChallenge(input())
        print(flow.get_subtask_ids())
    if "LoginAcid" in flow.get_subtask_ids():
        print(flow.content["subtasks"][0]["enter_text"]["header"]["secondary_text"]["text"])
        flow.LoginAcid(input())
        print(flow.get_subtask_ids())
    if "LoginSuccessSubtask" in flow.get_subtask_ids():
        print("===========Success===========")
        print(flow.get_subtask_ids())
    if "SuccessExit" not in flow.get_subtask_ids():
        print("Error")
        exit()

    flow.SaveCookies(filepath)


elif action == "password_reset":
    flow.password_reset_flow()
    flow.PwrJsInstrumentationSubtask()
    print(flow.get_subtask_ids())
    if "PasswordResetBegin"in flow.get_subtask_ids():
        print("電話番号/メールアドレス/ユーザー名")
        flow.PasswordResetBegin(input())
        print(flow.get_subtask_ids())
    if "PwrKnowledgeChallenge"in flow.get_subtask_ids():
        print(flow.content["subtasks"][0]["enter_text"]["secondary_text"]["text"])
        flow.PwrKnowledgeChallenge(input())
        print(flow.get_subtask_ids())
    if "PwrKnowledgeChallenge"in flow.get_subtask_ids():
        print(flow.content["subtasks"][0]["enter_text"]["secondary_text"]["text"])
        flow.PwrKnowledgeChallenge(input())
        print(flow.get_subtask_ids())
    if "PasswordResetChooseChallenge"in flow.get_subtask_ids():
        print("\n".join([choices["id"] + ": " + choices["text"]["text"] for choices in flow.content["subtasks"][0]["choice_selection"]["choices"]]))
        flow.PasswordResetChooseChallenge(input())
        print(flow.get_subtask_ids())
    if "PasswordResetConfirmChallenge"in flow.get_subtask_ids():
        print("コードを入力")
        flow.PasswordResetConfirmChallenge(input())
        print(flow.get_subtask_ids())
    if "PasswordResetNewPassword"in flow.get_subtask_ids():
        print("新しいパスワードを入力")
        flow.PasswordResetNewPassword(input())
        print(flow.get_subtask_ids())
    if "PasswordResetSurvey"in flow.get_subtask_ids():
        print("パスワードを変更した理由を教えてください")
        print("\n".join([choices["id"] + ": " + choices["text"]["text"] for choices in flow.content["subtasks"][0]["choice_selection"]["choices"]]))
        flow.PasswordResetSurvey(input())
        print(flow.get_subtask_ids())
    exit()

elif action == "load":
    print("ファイル名")
    flow.LoadCookies(filepath)

    
# flow.LoadCookies(filepath)




import pdb;pdb.set_trace()

# user_id = flow.user_info(screen_name="Flower_kyujin")
user_id = flow.user_info(screen_name=screen_name).content["id_str"]


#プロフ設定用---

res = flow.verify_password(password)

mydata = flow.account_data(password=password).content


res = flow.change_country()
flow.dm_filter()
print(flow.display_sensitive_media())
print(flow.gender())
print(flow.allow_dm())




import pdb;pdb.set_trace()
res = flow.update_profile(data=prof)
imgs = glob.glob('./img/*')
img_path = random.choice(imgs)
res_img = flow.update_profile_image(img_path).content


import pdb;pdb.set_trace()



#相互フォロー用

import pysnooper


@pysnooper.snoop()
def mutual_follow():
    res = flow.user_search("相互フォロー")
    user_ids = [u for u in res.content['globalObjects']['users'].keys()]
    for user_id in user_ids:
        resp = flow.friendships_create(user_id)
        time.sleep(1)



mutual_follow()
import pdb;pdb.set_trace()



users = res.content['globalObjects']['users']
users1 = [u for u in users.keys()]

fres = flow.friendships_create(users1[0])

res = flow.user_search("相互フォロー")
userss = res.content['globalObjects']['users']
users2 = [u for u in userss.keys()]

res = flow.followers_ids("yuri_yymm")


res = flow.change_country()
# flow.change_country_flow(country_code="jp")
# flow.change_country_subtask()
# flow.change_country_end()
# flow.dm_filter()

# print(flow.display_sensitive_media())
# print(flow.gender())
# print(flow.allow_dm())


res = flow.change_country()
flow.dm_filter()
print(flow.display_sensitive_media())
print(flow.gender())
print(flow.allow_dm())
res = flow.update_profile(data=prof)
imgs = glob.glob('./img/*')
img_path = random.choice(imgs)
res_img = flow.update_profile_image(img_path).content



import pdb;pdb.set_trace()





res = flow.update_profile(data=prof)
imgs = glob.glob('./img/*')
img_path = random.choice(imgs)
res_img = flow.update_profile_image(img_path).content



import pdb;pdb.set_trace()


imgs = glob.glob('./img/*')
img_path = random.choice(imgs)
res_img = flow.update_profile_image(img_path).content


import pdb;pdb.set_trace()



res = check_shadowban(screen_name='yoru2onna')

import pdb;pdb.set_trace()
#------DM用----------------


def create_conversation_id(user_id, you_id):
    if int(user_id) < int(you_id):
        return '{}-{}'.format(user_id, you_id)
    else:
        return '{}-{}'.format(you_id, user_id)
    

#送信歴なしなら相手のuserid, ありならNoneを返す
def get_unsent_userid(flow, user_id, conversation_id):
    #送信履歴があるかチェックする
    #まずはDM履歴一覧を取得
    res = flow.get_conversation(conversation_id=conversation_id)
    #会話履歴
    convs = res.content['conversation_timeline']['entries']
    #会話相手のuserid
    msg = convs[0]['message']['message_data']
    you_id = msg['recipient_id'] if user_id == msg['sender_id'] else msg['sender_id']
    #送信ユーザのIDのリスト
    sender_ids = [cn['message']['message_data']['sender_id'] for cn in convs]
    #あとで２通目のDMなど作る場合用
    send_count = sender_ids.count(user_id)
    print('send dm count {}'.format(send_count))
    if user_id not in sender_ids:
        print(f'you_id:{you_id}はまだ送信してないユーザー')
        return you_id
    else:
        print(f'you_id:{you_id}は送信済み')
        return None



#最新20人のDM履歴から送信履歴ないやつに送信.さらに過去履歴もやるためにmin_entry_idを返す
def send_dm_for_unsent(flow, user_id, send_msg, max_id=''):
    res = flow.get_dm(max_id=max_id)
    dms = res.content['user_inbox']


    #さらに過去のＤＭを取得する場合
    # min_entry_id=dms['min_entry_id']
    # res = flow.get_dm_more(max_id=min_entry_id)
    # dms = res.content['user_inbox']

    #会話一覧
    conversation_ids = list(dms['conversations'].keys())
    for conversation_id in conversation_ids:
        you_id = get_unsent_userid(flow, user_id, conversation_id)
        if you_id:
            flow.send_dm(send_msg, user_id=you_id)
            print(f'send dm to {you_id}')

    return dms['min_entry_id']



import pdb;pdb.set_trace()







print(
"""login: ログイン
password_reset: パスワードリセット
load: cookieのロード""")

action = input()

if action == "login":
    flow.login_flow()
    flow.LoginJsInstrumentationSubtask()
    print(flow.get_subtask_ids())
    if "LoginEnterUserIdentifierSSO" in flow.get_subtask_ids():
        print("Telephone number / Email address / User name")
        flow.LoginEnterUserIdentifierSSO(input())
        print(flow.get_subtask_ids())
    if "LoginEnterAlternateIdentifierSubtask" in flow.get_subtask_ids():
        print(flow.content["subtasks"][0]["enter_text"]["primary_text"]["text"])
        flow.LoginEnterAlternateIdentifierSubtask(input())
        print(flow.get_subtask_ids())
    if "LoginEnterPassword" in flow.get_subtask_ids():
        print(flow.content["subtasks"][0]["enter_password"]["primary_text"]["text"])
        flow.LoginEnterPassword(input())
        print(flow.get_subtask_ids())
    if "AccountDuplicationCheck" in flow.get_subtask_ids():
        flow.AccountDuplicationCheck()
        print(flow.get_subtask_ids())
    if "LoginTwoFactorAuthChallenge" in flow.get_subtask_ids():
        print(flow.content["subtasks"][0]["enter_text"]["header"]["primary_text"]["text"])
        flow.LoginTwoFactorAuthChallenge(input())
        print(flow.get_subtask_ids())
    if "LoginAcid" in flow.get_subtask_ids():
        print(flow.content["subtasks"][0]["enter_text"]["header"]["secondary_text"]["text"])
        flow.LoginAcid(input())
        print(flow.get_subtask_ids())
    if "LoginSuccessSubtask" in flow.get_subtask_ids():
        print("===========Success===========")
        print(flow.get_subtask_ids())
    if "SuccessExit" not in flow.get_subtask_ids():
        print("Error")
        exit()

elif action == "password_reset":
    flow.password_reset_flow()
    flow.PwrJsInstrumentationSubtask()
    print(flow.get_subtask_ids())
    if "PasswordResetBegin"in flow.get_subtask_ids():
        print("電話番号/メールアドレス/ユーザー名")
        flow.PasswordResetBegin(input())
        print(flow.get_subtask_ids())
    if "PwrKnowledgeChallenge"in flow.get_subtask_ids():
        print(flow.content["subtasks"][0]["enter_text"]["secondary_text"]["text"])
        flow.PwrKnowledgeChallenge(input())
        print(flow.get_subtask_ids())
    if "PwrKnowledgeChallenge"in flow.get_subtask_ids():
        print(flow.content["subtasks"][0]["enter_text"]["secondary_text"]["text"])
        flow.PwrKnowledgeChallenge(input())
        print(flow.get_subtask_ids())
    if "PasswordResetChooseChallenge"in flow.get_subtask_ids():
        print("\n".join([choices["id"] + ": " + choices["text"]["text"] for choices in flow.content["subtasks"][0]["choice_selection"]["choices"]]))
        flow.PasswordResetChooseChallenge(input())
        print(flow.get_subtask_ids())
    if "PasswordResetConfirmChallenge"in flow.get_subtask_ids():
        print("コードを入力")
        flow.PasswordResetConfirmChallenge(input())
        print(flow.get_subtask_ids())
    if "PasswordResetNewPassword"in flow.get_subtask_ids():
        print("新しいパスワードを入力")
        flow.PasswordResetNewPassword(input())
        print(flow.get_subtask_ids())
    if "PasswordResetSurvey"in flow.get_subtask_ids():
        print("パスワードを変更した理由を教えてください")
        print("\n".join([choices["id"] + ": " + choices["text"]["text"] for choices in flow.content["subtasks"][0]["choice_selection"]["choices"]]))
        flow.PasswordResetSurvey(input())
        print(flow.get_subtask_ids())
    exit()

elif action == "load":
    print("ファイル名")
    flow.LoadCookies(input())







while True:
    print(
"""tweet: ツイート
fav: いいね
unfav: いいね取り消し
rt: リツイート
unrt: リツイート取り消し
follow: フォロー
unfollow: フォロー取り消し
save: cookieの出力
end: 終了""")

    action = input()

    if action == "tweet":
        print("ツイート内容")
        flow.CreateTweet(input())
    elif action == "fav":
        print("ツイートid")
        flow.FavoriteTweet(input())
    elif action == "unfav":
        print("ツイートid")
        flow.UnfavoriteTweet(input())
    elif action == "rt":
        print("ツイートid")
        flow.CreateRetweet(input())
    elif action == "unrt":
        print("ツイートid")
        flow.DeleteRetweet(input())
    elif action == "follow":
        print("ユーザー内部id")
        flow.friendships_create(input())
    elif action == "unfollow":
        print("ユーザー内部id")
        flow.friendships_destroy(input())
    elif action == "save":
        print("ファイル名")
        flow.SaveCookies(input())
    elif action == "end":
        break