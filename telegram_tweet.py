#!/usr/bin/env python
# -*- coding: utf-8 -*-
# made with python 3
# pylint: disable=C1001
import tweepy


class TweetFromTelegram():

    def __init__(self):
        consumer_key = ""
        consumer_secret = ""
        access_token = ""
        access_token_secret = ""
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth, wait_on_rate_limit=True)

    def new_tweet(self, tweet, has_media=False):
        """Create a new tweet"""
        link = None
        try:
            if not has_media:
                self.api.update_status(str(tweet))
            else:
                self.api.update_with_media('downloaded_img.png', str(tweet))
            link = TweetFromTelegram.get_last_status_link(self.api)
        except UnicodeEncodeError:
            link = "error"
        return link

    @staticmethod
    def get_last_status_link(api):
        """Get the link from the last tweet from user timeline"""
        link = "https://twitter.com/pytwe_bot/status/"
        tweets = api.user_timeline()
        link += str(tweets[0].id)
        return link
