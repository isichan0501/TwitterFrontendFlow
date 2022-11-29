import requests
import json
import pysnooper

#追加
# 加工した画像ファイルをbase64変換する-
from io import BytesIO
import base64
from PIL import Image, ImageDraw, ImageFont


def pil_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format="jpeg")
    img_str = base64.b64encode(buffer.getvalue()).decode("ascii")
    return img_str


class TwitterFrontendFlow:
    def __init__(self, proxies={}, language="en"):
        self.USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
        self.AUTHORIZATION = "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA"
        self.proxies = proxies
        self.session = requests.session()
        self.__twitter()
        self.x_guest_token = self.__get_guest_token()
        self.method_check_bypass = False
        self.flow_token = None
        self.language = language

    def __twitter(self):
        headers = {
            "User-Agent": self.USER_AGENT,
        }
        response = self.session.get(
            "https://twitter.com/", headers=headers, proxies=self.proxies
        )
        return self

    def __get_guest_token(self):
        headers = {
            "authorization": self.AUTHORIZATION,
            "User-Agent": self.USER_AGENT,
        }
        response = self.session.post(
            "https://api.twitter.com/1.1/guest/activate.json",
            headers=headers,
            proxies=self.proxies,
        ).json()
        return response["guest_token"]

    def __get_headers(self):
        return {
            "authorization": self.AUTHORIZATION,
            "User-Agent": self.USER_AGENT,
            "Content-type": "application/json",
            "x-guest-token": self.x_guest_token,
            "x-csrf-token": self.session.cookies.get("ct0"),
            "x-twitter-active-user": "yes",
            "x-twitter-client-language": self.language,
        }

    def __get_headers_legacy(self):
        return {
            "authorization": self.AUTHORIZATION,
            "User-Agent": self.USER_AGENT,
            "Content-type": "application/x-www-form-urlencoded",
            "x-csrf-token": self.session.cookies.get("ct0"),
            "x-twitter-active-user": "yes",
            "x-twitter-auth-type": "OAuth2Session",
        }

    def get_subtask_ids(self):
        return [subtasks["subtask_id"] for subtasks in self.content["subtasks"]]

    def __flow_token_check(self):
        if self.flow_token == None:
            raise Exception("not found token")

    def __error_check(self):
        if self.content.get("errors"):
            raise Exception(self.content["errors"][0]["message"])

    def __method_check(self, method_name):
        if self.method_check_bypass:
            return
        if method_name not in self.get_subtask_ids():
            raise Exception(
                "{0} is inappropriate method. choose from {1}. information: https://github.com/fa0311/TwitterFrontendFlow#inappropriate-method".format(
                    method_name, ", ".join(self.get_subtask_ids())
                )
            )

    def LoadCookies(self, file_path):
        with open(file_path, "r") as f:
            for cookie in json.load(f):
                self.session.cookies.set_cookie(
                    requests.cookies.create_cookie(**cookie)
                )
        return self

    def SaveCookies(self, file_path):
        cookies = []
        for cookie in self.session.cookies:
            cookie_dict = dict(
                version=cookie.version,
                name=cookie.name,
                value=cookie.value,
                port=cookie.port,
                domain=cookie.domain,
                path=cookie.path,
                secure=cookie.secure,
                expires=cookie.expires,
                discard=cookie.discard,
                comment=cookie.comment,
                comment_url=cookie.comment_url,
                rfc2109=cookie.rfc2109,
                rest=cookie._rest,
            )
            cookies.append(cookie_dict)

        with open(file_path, "w") as f:
            json.dump(cookies, f, indent=4)
        return self

    # ログイン

    def login_flow(self):
        data = {
            "input_flow_data": {
                "flow_context": {
                    "debug_overrides": {},
                    "start_location": {"location": "splash_screen"},
                }
            },
            "subtask_versions": {
                "contacts_live_sync_permission_prompt": 0,
                "email_verification": 1,
                "topics_selector": 1,
                "wait_spinner": 1,
                "cta": 4,
            },
        }
        params = {"flow_name": "login"}
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            params=params,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def LoginJsInstrumentationSubtask(self):
        self.__flow_token_check()
        self.__method_check("LoginJsInstrumentationSubtask")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "LoginJsInstrumentationSubtask",
                    "js_instrumentation": {
                        "response": json.dumps(
                            {
                                "rf": {
                                    "af07339bbc6d24ced887d705eb0c9fd29b4a7d7ddc21136c9f94d53a4bc774d2": 88,
                                    "a6ce87d6481c6ec4a823548be3343437888441d2a453061c54f8e2eb325856f7": 250,
                                    "a0062ad06384a8afd38a41cd83f31b0dbfdea0eff4b24c69f0dd9095b2fb56d6": 16,
                                    "a929e5913a5715d93491eaffaa139ba4977cbc826a5e2dbcdc81cae0f093db25": 186,
                                },
                                "s": "Q-H-53m1uXImK0F0ogrxRQtCWTH1KIlPbIy0MloowlMa4WNK5ZCcDoXyRs1q_cPbynK73w_wfHG_UVRKKBWRoh6UJtlPS5kMa1p8fEvTYi76hwdzBEzovieR8t86UpeSkSBFYcL8foYKSp6Nop5mQR_QHGyEeleclCPUvzS0HblBJqZZdtUo-6by4BgCyu3eQ4fY5nOF8fXC85mu6k34wo982LMK650NsoPL96DBuloqSZvSHU47wq2uA4xy24UnI2WOc6U9KTvxumtchSYNnXq1HV662B8U2-jWrzvIU4yUHV3JYUO6sbN6j8Ho9JaUNJpJSK7REwqCBQ3yG7iwMAAAAX2Vqcbs",
                            }
                        ),
                        "link": "next_link",
                    },
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def LoginEnterUserIdentifierSSO(self, user_id):
        self.__flow_token_check()
        self.__method_check("LoginEnterUserIdentifierSSO")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "LoginEnterUserIdentifierSSO",
                    "settings_list": {
                        "setting_responses": [
                            {
                                "key": "user_identifier",
                                "response_data": {"text_data": {"result": user_id}},
                            }
                        ],
                        "link": "next_link",
                    },
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def AccountDuplicationCheck(self):
        self.__flow_token_check()
        self.__method_check("AccountDuplicationCheck")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "AccountDuplicationCheck",
                    "check_logged_in_account": {
                        "link": "AccountDuplicationCheck_false"
                    },
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def LoginEnterAlternateIdentifierSubtask(self, text):
        self.__flow_token_check()
        self.__method_check("LoginEnterAlternateIdentifierSubtask")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "LoginEnterAlternateIdentifierSubtask",
                    "enter_text": {"text": text, "link": "next_link"},
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def LoginEnterPassword(self, password):
        self.__flow_token_check()
        self.__method_check("LoginEnterPassword")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "LoginEnterPassword",
                    "enter_password": {"password": password, "link": "next_link"},
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def LoginTwoFactorAuthChallenge(self, TwoFactorCode):
        self.__flow_token_check()
        self.__method_check("LoginTwoFactorAuthChallenge")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "LoginTwoFactorAuthChallenge",
                    "enter_text": {"text": TwoFactorCode, "link": "next_link"},
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def LoginAcid(self, acid):
        self.__flow_token_check()
        self.__method_check("LoginAcid")
        data = {
            "flow_token":self.flow_token,
            "subtask_inputs":[
                {
                    "subtask_id":"LoginAcid",
                    "enter_text":
                        {
                            "text": acid,
                            "link":"next_link"
                        }
                    }
                ]
            }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self


    # attの取得 無くても動くっぽい

    def get_att(self):
        data = {"flow_token": self.flow_token, "subtask_inputs": []}
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.content = response
        self.__error_check()
        return self

    # ct0の更新 無くても動くっぽい

    def Viewer(self):
        params = {
            "variables": json.dumps(
                {
                    "withCommunitiesMemberships": True,
                    "withCommunitiesCreation": True,
                    "withSuperFollowsUserFields": True,
                }
            )
        }
        response = self.session.get(
            "https://twitter.com/i/api/graphql/O_C5Q6xAVNOmeolcXjKqYw/Viewer",
            headers=self.__get_headers(),
            params=params,
        )

        self.content = response
        self.__error_check()
        return self

    def RedirectToPasswordReset(self):
        raise Exception(
            "RedirectToPasswordResetは現在サポートされていません。代わりにpassword_reset_flowを使用して下さい。"
        )

    # パスワードリセット

    def password_reset_flow(self):
        data = {
            "input_flow_data": {
                "flow_context": {
                    "debug_overrides": {},
                    "start_location": {"location": "manual_link"},
                }
            },
            "subtask_versions": {
                "contacts_live_sync_permission_prompt": 0,
                "email_verification": 1,
                "topics_selector": 1,
                "wait_spinner": 1,
                "cta": 4,
            },
        }
        params = {"flow_name": "password_reset"}
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            params=params,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def PwrJsInstrumentationSubtask(self):
        self.__flow_token_check()
        self.__method_check("PwrJsInstrumentationSubtask")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "PwrJsInstrumentationSubtask",
                    "js_instrumentation": {
                        "response": json.dumps(
                            {
                                "rf": {
                                    "af07339bbc6d24ced887d705eb0c9fd29b4a7d7ddc21136c9f94d53a4bc774d2": 88,
                                    "a6ce87d6481c6ec4a823548be3343437888441d2a453061c54f8e2eb325856f7": 250,
                                    "a0062ad06384a8afd38a41cd83f31b0dbfdea0eff4b24c69f0dd9095b2fb56d6": 16,
                                    "a929e5913a5715d93491eaffaa139ba4977cbc826a5e2dbcdc81cae0f093db25": 186,
                                },
                                "s": "Q-H-53m1uXImK0F0ogrxRQtCWTH1KIlPbIy0MloowlMa4WNK5ZCcDoXyRs1q_cPbynK73w_wfHG_UVRKKBWRoh6UJtlPS5kMa1p8fEvTYi76hwdzBEzovieR8t86UpeSkSBFYcL8foYKSp6Nop5mQR_QHGyEeleclCPUvzS0HblBJqZZdtUo-6by4BgCyu3eQ4fY5nOF8fXC85mu6k34wo982LMK650NsoPL96DBuloqSZvSHU47wq2uA4xy24UnI2WOc6U9KTvxumtchSYNnXq1HV662B8U2-jWrzvIU4yUHV3JYUO6sbN6j8Ho9JaUNJpJSK7REwqCBQ3yG7iwMAAAAX2Vqcbs",
                            }
                        ),
                        "link": "next_link",
                    },
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def PasswordResetBegin(self, user_id):
        self.__flow_token_check()
        self.__method_check("PasswordResetBegin")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "PasswordResetBegin",
                    "enter_text": {"text": user_id, "link": "next_link"},
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def PasswordResetChooseChallenge(self, choices="0"):
        self.__flow_token_check()
        self.__method_check("PasswordResetChooseChallenge")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "PasswordResetChooseChallenge",
                    "choice_selection": {
                        "link": "next_link",
                        "selected_choices": [choices],
                    },
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def PwrKnowledgeChallenge(self, text):
        self.__flow_token_check()
        self.__method_check("PwrKnowledgeChallenge")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "PwrKnowledgeChallenge",
                    "enter_text": {"text": text, "link": "next_link"},
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def PasswordResetConfirmChallenge(self, code):
        self.__flow_token_check()
        self.__method_check("PasswordResetConfirmChallenge")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "PasswordResetConfirmChallenge",
                    "enter_text": {"text": code, "link": "next_link"},
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def PasswordResetNewPassword(self, password):
        self.__flow_token_check()
        self.__method_check("PasswordResetNewPassword")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "PasswordResetNewPassword",
                    "enter_password": {"password": password, "link": "next_link"},
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    def PasswordResetSurvey(self, choices="0"):
        self.__flow_token_check()
        self.__method_check("PasswordResetSurvey")
        data = {
            "flow_token": self.flow_token,
            "subtask_inputs": [
                {
                    "subtask_id": "PasswordResetSurvey",
                    "choice_selection": {
                        "link": "next_link",
                        "selected_choices": [choices],
                    },
                }
            ],
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/onboarding/task.json",
            headers=self.__get_headers(),
            json=data,
            proxies=self.proxies,
        ).json()
        self.flow_token = response.get("flow_token")
        self.content = response
        self.__error_check()
        return self

    # ログイン後

    def CreateTweet(self, tweet_text):
        data = {
            "queryId": "XyvN0Wv13eeu_gVIHDi10g",
            "variables": json.dumps(
                {
                    "tweet_text": tweet_text,
                    "media": {"media_entities": [], "possibly_sensitive": False},
                    "withDownvotePerspective": False,
                    "withReactionsMetadata": False,
                    "withReactionsPerspective": False,
                    "withSuperFollowsTweetFields": True,
                    "withSuperFollowsUserFields": False,
                    "semantic_annotation_ids": [],
                    "dark_request": False,
                    "withBirdwatchPivots": False,
                }
            ),
        }
        response = self.session.post(
            "https://twitter.com/i/api/graphql/XyvN0Wv13eeu_gVIHDi10g/CreateTweet",
            headers=self.__get_headers(),
            json=data,
        ).json()
        self.content = response
        self.__error_check()
        return self

    def FavoriteTweet(self, tweet_id):
        data = {
            "queryId": "lI07N6Otwv1PhnEgXILM7A",
            "variables": json.dumps(
                {
                    "tweet_id": tweet_id,
                }
            ),
        }
        response = self.session.post(
            "https://twitter.com/i/api/graphql/lI07N6Otwv1PhnEgXILM7A/FavoriteTweet",
            headers=self.__get_headers(),
            json=data,
        ).json()
        self.content = response
        self.__error_check()
        return self

    def UnfavoriteTweet(self, tweet_id):
        data = {
            "queryId": "ZYKSe-w7KEslx3JhSIk5LA",
            "variables": json.dumps(
                {
                    "tweet_id": tweet_id,
                }
            ),
        }
        response = self.session.post(
            "https://twitter.com/i/api/graphql/ZYKSe-w7KEslx3JhSIk5LA/UnfavoriteTweet",
            headers=self.__get_headers(),
            json=data,
        ).json()
        self.content = response
        self.__error_check()
        return self

    def CreateRetweet(self, tweet_id):
        data = {
            "queryId": "ojPdsZsimiJrUGLR1sjUtA",
            "variables": json.dumps(
                {
                    "tweet_id": tweet_id,
                    "dark_request": False,
                }
            ),
        }
        response = self.session.post(
            "https://twitter.com/i/api/graphql/ojPdsZsimiJrUGLR1sjUtA/CreateRetweet",
            headers=self.__get_headers(),
            json=data,
        ).json()
        self.content = response
        self.__error_check()
        return self

    def DeleteRetweet(self, tweet_id):
        data = {
            "queryId": "iQtK4dl5hBmXewYZuEOKVw",
            "variables": json.dumps(
                {
                    "source_tweet_id": tweet_id,
                    "dark_request": False,
                }
            ),
        }
        response = self.session.post(
            "https://twitter.com/i/api/graphql/iQtK4dl5hBmXewYZuEOKVw/DeleteRetweet",
            headers=self.__get_headers(),
            json=data,
        ).json()
        self.content = response
        self.__error_check()
        return self


    # Legacy API v1.1

    def friendships_create(self, tweet_id):
        data = {
            "include_profile_interstitial_type": 1,
            "include_blocking": 1,
            "include_blocked_by": 1,
            "include_followed_by": 1,
            "include_want_retweets": 1,
            "include_mute_edge": 1,
            "include_can_dm": 1,
            "include_can_media_tag": 1,
            "include_ext_has_nft_avatar": 1,
            "skip_status": 1,
            "id": tweet_id,
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/friendships/create.json",
            headers=self.__get_headers_legacy(),
            data=data,
        ).json()
        self.content = response
        return self

    def friendships_destroy(self, tweet_id):
        data = {
            "include_profile_interstitial_type": 1,
            "include_blocking": 1,
            "include_blocked_by": 1,
            "include_followed_by": 1,
            "include_want_retweets": 1,
            "include_mute_edge": 1,
            "include_can_dm": 1,
            "include_can_media_tag": 1,
            "include_ext_has_nft_avatar": 1,
            "skip_status": 1,
            "id": tweet_id,
        }
        response = self.session.post(
            "https://twitter.com/i/api/1.1/friendships/destroy.json",
            headers=self.__get_headers_legacy(),
            data=data,
        ).json()
        self.content = response
        return self


    #追加--
    
    def get_dm_inbox(self):
            response = self.session.get('https://twitter.com/i/api/1.1/dm/inbox_initial_state.json', headers=self.__get_headers_legacy(), timeout=30).json()
            self.content = response
            return self

    def get_dm(self, max_id=''):

        if max_id == '':
            response = self.session.get('https://api.twitter.com/1.1/dm/user_inbox.json', headers=self.__get_headers_legacy(), timeout=30).json()

        else:
            data = {
                'max_conv_count': '50',
                'include_groups': 'true',
                'max_id': max_id,
                'cards_platform': 'Web-13',
                'include_entities': '0',
                'include_user_entities': '0',
                'include_cards': '0',
                'send_error_codes': '1',
                'tweet_mode': 'extended',
                'include_ext_alt_text': 'true',
                'include_reply_count': 'true',
            }
            
            response = self.session.get('https://api.twitter.com/1.1/dm/user_inbox.json', headers=self.__get_headers_legacy(), data=data, timeout=30).json()

        self.content = response
        return self

    
    def get_dm_more(self, max_id='999999999999999999999999'):
        
        data = {
            'max_conv_count': '50',
            'include_groups': 'true',
            'max_id': max_id,
            'cards_platform': 'Web-13',
            'include_entities': '0',
            'include_user_entities': '0',
            'include_cards': '0',
            'send_error_codes': '1',
            'tweet_mode': 'extended',
            'include_ext_alt_text': 'true',
            'include_reply_count': 'true',
        }
        
        response = self.session.get('https://api.twitter.com/1.1/dm/user_inbox.json', headers=self.__get_headers_legacy(), data=data, timeout=30).json()
        self.content = response
        return self

    
    def get_conversation(self, conversation_id=''):


        url = 'https://api.twitter.com/1.1/dm/conversation/{}.json'.format(conversation_id)
        # data = {
        #     'ext': 'altText',
        #     'count': '100',
        #     'max_id': max_id,
        #     'cards_platform': 'Web-13',
        #     'include_entities': '1',
        #     'include_user_entities': '1',
        #     'include_cards': '1',
        #     'send_error_codes': '1',
        #     'tweet_mode': 'extended',
        #     'include_ext_alt_text': 'true',
        #     'include_reply_count': 'true',
        # }
        
        response = self.session.get(url, headers=self.__get_headers_legacy(), timeout=30).json()
        self.content = response
        return self

    def send_dm(self, text, screen_name=None, user_id=None):
        if screen_name == None:
            if user_id == None:
                print("Neither 'screen_name' nor 'user_id' was entered.")
            else:
                data = {
                    'recipient_ids': user_id,
                    'text': text
                }

                response = self.session.post('https://twitter.com/i/api/1.1/dm/new.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()

        else:
            response = self.session.get('https://api.twitter.com/1.1/users/show.json?screen_name=' + screen_name, headers=self.__get_headers_legacy(),timeout=30).json()
            data = {
                'recipient_ids': response['id'],
                'text': text
            }

            response = self.session.post('https://twitter.com/i/api/1.1/dm/new.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()

        self.content = response
        return self
    

    #アカウント設定用

    def user_info(self, screen_name=None, user_id=None):
        if screen_name == None:
            if user_id == None:
                print("Neither 'screen_name' nor 'user_id' was entered.")
            else:
                response = self.session.get('https://api.twitter.com/1.1/users/show.json?user_id=' + user_id, headers=self.__get_headers_legacy(),timeout=30).json()
        else:
            response = self.session.get('https://api.twitter.com/1.1/users/show.json?screen_name=' + screen_name, headers=self.__get_headers_legacy(),timeout=30).json()

        self.content = response
        return self

    def verify_password(self, password):
        data = {
            'password': password
        }
        
        response = self.session.post('https://twitter.com/i/api/1.1/account/verify_password.json', headers=self.__get_headers_legacy(), data=data)

        return response.json() | response.cookies.get_dict()

    def account_data(self, verify=None, password=""):
        if verify == None:
            data = {
                'password': password
            }

            response = self.session.post('https://twitter.com/i/api/1.1/account/verify_password.json', headers=self.__get_headers_legacy(), data=data)
            if "errors" in response.json():
                print(response.json()["errors"][0]["message"])
            elif response.json()["status"] == "ok":
                # cookie = self.headers["cookie"] + '; _twitter_sess=' + response.cookies.get_dict()["_twitter_sess"]
                # self.headers["cookie"] = cookie

                response = self.session.get('https://twitter.com/i/api/1.1/account/personalization/p13n_data.json', headers=self.__get_headers_legacy(),timeout=30).json()

        elif not verify == None:
            # cookie = self.headers["cookie"] + '; _twitter_sess=' + verify
            # self.headers["cookie"] = cookie

            response = self.session.get('https://twitter.com/i/api/1.1/account/personalization/p13n_data.json', headers=self.__get_headers_legacy(),timeout=30).json()

        self.content = response
        return self

    
    def display_sensitive_media(self, display='true'):

        data = {
            'display_sensitive_media': display.lower()
        }

        response = self.session.post('https://twitter.com/i/api/1.1/account/settings.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()
        self.content = response
        return self

    def pin_tweet(self, id):
        data = {
            'id': id
        }

        response = self.session.post('https://twitter.com/i/api/1.1/account/pin_tweet.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()

        return response

    def unpin_tweet(self, id):
        data = {
            'id': id
        }

        response = self.session.post('https://twitter.com/i/api/1.1/account/unpin_tweet.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()

        self.content = response
        return self

    def change_id(self, id):
        data = {
            'screen_name': id
        }
        
        response = self.session.post('https://twitter.com/i/api/1.1/account/settings.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()

        self.content = response
        return self

    def private(self, protected):
        if not protected.lower() in ["true", "false"]:
            print("""Please enter "true" or "false".""")
        elif protected.lower() in ["true", "false"]:
            data = {
                'protected': protected
            }
            
            response = self.session.post('https://twitter.com/i/api/1.1/account/settings.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()

        self.content = response
        return self

    def gender(self, gender='female'):
        if gender.lower() in ["female", "male"]:
            data = '{"preferences":{"gender_preferences":{"use_gender_for_personalization":true,"gender_override":{"type":"' + gender.lower() + '","value":"' + gender.lower() + '"}}}}'

            response = self.session.post('https://twitter.com/i/api/1.1/account/settings.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()
        else:
            data = '{"preferences":{"gender_preferences":{"use_gender_for_personalization":true,"gender_override":{"type":"custom","value":"' + gender.lower() + '"}}}}'

        self.content = response
        return self


    def allow_dm(self, allow_dms_from='all'):
        #allow_dms_from = 'all' or 'following'

        data = {
            'include_mention_filter': 'true',
            'include_nsfw_user_flag': 'true',
            'include_nsfw_admin_flag': 'true',
            'include_ranked_timeline': 'true',
            'include_alt_text_compose': 'true',
            'allow_dms_from': allow_dms_from,
        }

        response = self.session.post('https://twitter.com/i/api/1.1/account/settings.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()
        self.content = response
        return self

    def update_profile(self, data):
        """
        Args:
            data (dict): 
            {
                'birthdate_year': '2000',
                'birthdate_month': '1',
                'birthdate_day': '1',
                'birthdate_visibility': 'self',
                'birthdate_year_visibility': 'self',
                'displayNameMaxLength': 50,
                'url': 'https://twitter.com/aaa',
                'name': 'bot',
                'description': 'yoyo!',
                'location': 'JP'
            }
        """
        response = self.session.post('https://twitter.com/i/api/1.1/account/update_profile.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()
        self.content = response
        return self
    
    def update_profile_image(self, img_path):
        src_img = Image.open(img_path)
        img_str = pil_to_base64(src_img)
        data = {
            'image': img_str
        }
        response = self.session.post('https://twitter.com/i/api/1.1/account/update_profile_image.json', headers=self.__get_headers_legacy(), data=data,timeout=30).json()
        self.content = response
        return self




def check_shadowban(screen_name):

    cookies = {
        '_ga_4E8SDFWKN5': 'GS1.1.1669633608.1.0.1669633608.0.0.0',
        '_ga': 'GA1.2.1479150603.1669633609',
        '_gid': 'GA1.2.1288539343.1669633609',
        '_gat_gtag_UA_202220676_1': '1',
        '__gads': 'ID=c589bfc8c8066f7b-22feefe0abd8009f:T=1669633608:RT=1669633608:S=ALNI_Map5heMU212-gSYSxM7lS4DO-oGmg',
        '__gpi': 'UID=00000b856b7b2b20:T=1669633608:RT=1669633608:S=ALNI_MYBpmGUeJ2vZ-__Foiy2SGgZgt0iA',
        'FCNEC': '%5B%5B%22AKsRol8IQ5YxG-cXUCxav6OZ2n6gpHSIq7m55sLr3T4g1p-KZj8cQO71VUDId1OG8L9b9wMXj8X0nQobgUnYkGr3hS-XOew3neAqc9iSm4nkZdYrbJ0cTLt2HvAbE-7yGWDQgBA3jTyoAcOAXS40HYLwUjFnyzKDIA%3D%3D%22%5D%2Cnull%2C%5B%5D%5D',
    }

    headers = {
        'authority': 'taishin-miyamoto.com',
        'accept': '*/*',
        'accept-language': 'ja',
        # Requests sorts cookies= alphabetically
        # 'cookie': '_ga_4E8SDFWKN5=GS1.1.1669633608.1.0.1669633608.0.0.0; _ga=GA1.2.1479150603.1669633609; _gid=GA1.2.1288539343.1669633609; _gat_gtag_UA_202220676_1=1; __gads=ID=c589bfc8c8066f7b-22feefe0abd8009f:T=1669633608:RT=1669633608:S=ALNI_Map5heMU212-gSYSxM7lS4DO-oGmg; __gpi=UID=00000b856b7b2b20:T=1669633608:RT=1669633608:S=ALNI_MYBpmGUeJ2vZ-__Foiy2SGgZgt0iA; FCNEC=%5B%5B%22AKsRol8IQ5YxG-cXUCxav6OZ2n6gpHSIq7m55sLr3T4g1p-KZj8cQO71VUDId1OG8L9b9wMXj8X0nQobgUnYkGr3hS-XOew3neAqc9iSm4nkZdYrbJ0cTLt2HvAbE-7yGWDQgBA3jTyoAcOAXS40HYLwUjFnyzKDIA%3D%3D%22%5D%2Cnull%2C%5B%5D%5D',
        'referer': 'https://taishin-miyamoto.com/ShadowBan/',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }

    params = {
        'screen_name': screen_name,
    }

    response = requests.get('https://taishin-miyamoto.com/ShadowBan/API/JSON', params=params, cookies=cookies, headers=headers, timeout=30).json()
    print(response)
    return response