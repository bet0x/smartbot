import re
import urllib

import isodate
import requests

import smartbot
from smartbot import utils
from smartbot.exceptions import *
from smartbot.formatting import *


class Plugin(smartbot.Plugin):
    """Get information about posted Instagram photos."""
    names = ["instagram"]

    def __init__(self, client_id):
        self.client_id = client_id

    def _get_reply(self, media):
        caption = media["caption"]["text"]
        userName = media["user"]["full_name"]
        likes = media["likes"]["count"]

        return "{} by {} | {}".format(
            self.bot.format(caption, Style.underline),
            self.bot.format(userName, Style.underline),
            self.bot.format(likes, Colour.fg_green),
        )

    def _get_media_info(self, shortcode):
        url = "https://api.instagram.com/v1/media/shortcode/{}".format(shortcode)
        params = {
            "client_id": self.client_id,
        }

        s = utils.web.requests_session()
        res = s.get(url, params=params).json()
        try:
            return res["data"]
        except KeyError:
            return None

    def on_command(self, msg, stdin, stdout, reply):
        for shortcode in msg["args"][1:]:
            media = self._get_media_info(shortcode)
            if media:
                print(self._get_reply(media), file=stdout)

    def on_help(self):
        return "{} {} …".format(
            super().on_help(),
            self.bot.format("id", Style.underline)
        )
