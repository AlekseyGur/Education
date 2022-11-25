from scrapy.http import HtmlResponse
from instaparser.items import InstaparserItem
from copy import deepcopy
from urllib.parse import urlencode
import json
import re
import scrapy

class InstaSpider(scrapy.Spider):
    # атрибуты класса
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['https://instagram.com/']
    insta_login = 'логин_для_входа'
    insta_pwd = '#PWD_INSTAGRAM_BROWSER'
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    users_to_parse = ['логин_пользователя_1', 'логин_пользователя_2']  # пользователь для парса

    posts_hash = 'хеш страницы с лентой новостей'
    user_followers_hash = 'хеш страницы с фоловерами'
    user_subscriptions_hash = 'хеш страницы с подписками'

    def get_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def get_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
    
    def parse(self, response: HtmlResponse):
        csrf_token = self.get_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.get_userpage,
            formdata={
                'username': self.insta_login,
                'enc_password': self.insta_pwd
            },
            headers={
                'X-CSRFToken': csrf_token
            }
        )

    def get_userpage(self, response: HtmlResponse):
        b = json.loads(response.text)
        if b['authenticated']:
            for username in self.users_to_parse:
                yield response.follow(
                    f'/{username}',
                    callback=self.parse_user_data,
                    cb_kwargs={'username': username}
                )

    def parse_user_info(self, response: HtmlResponse, username, user_id, variables, followed_by):
        j_data = json.loads(response.text)

        page_info = j_data.get('data').get('user').get('edge_followed_by' if followed_by else 'edge_follow')

        if page_info is None:
            return

        page_info = page_info.get('page_info') if page_info is not None else None

        if page_info.get('has_next_page'):
            variables['after'] = page_info['end_cursor']

            user_followers_url = f'{self.graphql_url}query_hash={self.user_followers_hash}&{urlencode(variables)}'

            yield response.follow(
                user_followers_url,
                callback=self.parse_user_info,
                cb_kwargs={
                    'username': username,
                    'user_id': user_id,
                    'variables': variables
                }
            )

        users = j_data.get('data').get('user').get('edge_followed_by' if followed_by else 'edge_follow').get('edges')
        for user in users:  # Перебираем подписчиков, собираем данные
            item = InstaparserItem(
                user_id=user.get('node').get('id'),
                user_name=user.get('node').get('username'),
                full_name=user.get('node').get('full_name'),
                photo=user.get('node').get('profile_pic_url'),
                is_followed_by=user_id if followed_by else None,
                follows=None if followed_by else user_id
            )

            yield item  # В пайплайн

    def parse_user_data(self, response: HtmlResponse, username):
        variables = {
            "id": self.get_user_id(response.text, username),
            "include_reel": True,
            "fetch_mutual": False,
            "first": 20
        }

        user_followers_url = f'{self.graphql_url}query_hash={self.user_followers_hash}&{urlencode(variables)}'
        yield response.follow(
            user_followers_url,
            callback=self.parse_user_info,
            cb_kwargs={
                'username': username,
                'user_id': user_id,
                'variables': variables,
                'followed_by': True
            }
        )

        user_subscriptions_url = f'{self.graphql_url}query_hash={self.user_subscriptions_hash}&{urlencode(variables)}'
        yield response.follow(
            user_subscriptions_url,
            callback=self.parse_user_info,
            cb_kwargs={
                'username': username,
                'user_id': user_id,
                'variables': variables,
                'followed_by': False
            }
        )
