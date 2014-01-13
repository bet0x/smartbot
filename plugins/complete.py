import io
import requests
import lxml.etree
import urllib.parse

class Plugin:
    def __call__(self, bot):
        bot.on_respond(r"complete (.+)$", self.on_respond)
        bot.on_help("complete", self.on_help)

    def on_respond(self, bot, msg, reply):
        url = "http://google.com/complete/search?q={0}&output=toolbar".format(urllib.parse.quote(msg["match"].group(1)))
        headers = { "User-Agent": "SmartBot" }

        page = requests.get(url, headers=headers)
        tree = lxml.etree.fromstring(page.text)

        suggestions = []
        for suggestion in tree.xpath("//suggestion"):
            suggestions.append(suggestion.get("data"))

        reply(", ".join(suggestions[:5]))

    def on_help(self, bot, msg, reply):
        reply("Syntax: complete <query>")
