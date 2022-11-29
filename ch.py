from TwitterFrontendFlow.TwitterFrontendFlow import TwitterFrontendFlow, check_shadowban


import pprint
from importlib import reload




# screen_name = 'HardiePaz'

ban_list = []
#ログインフロー

with open('tw.txt', mode='r', encoding='utf-8') as f:
    screen_names = [x.strip() for x in f.readlines()]
    

# import pdb;pdb.set_trace()
for screen_name in screen_names:
    res = check_shadowban(screen_name=screen_name)
    print(screen_name)
    if res['suspend'] == True:
        banis = '{}:True'.format(screen_name)
    else:
        banis = '{}:False'.format(screen_name)
    ban_list.append(banis)

    
with open('end.txt', mode='w', encoding='utf-8') as f:
    f.write('\n'.join(ban_list))

import pdb;pdb.set_trace()
res = check_shadowban(screen_name='screen_name')





import pdb;pdb.set_trace()


user_id = flow.user_info(screen_name=screen_name).content["id_str"]



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
    res = flow.get_conversation(conversation_id = conversation_id)
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