import requests
import lxml.html
from .tv_program import found_information_tv_program as found_tv_program
from .model_message import ModelMessage


class TelegramBot():
    def __init__(self, TELEGRAM_TOKEN) -> None:
        self.url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
        self.offset = "0"
        self.run = True

    def listen(self):
        while self.run:
            res, status = self.get_updates()
            if status != 200 or not res["ok"]:
                print("Server error.")
                break

            for info_msg in res["result"]:
                try:
                    msg = ModelMessage(**info_msg)
                    self.offset = str(msg.update_id + 1)
                    result = found_tv_program(msg.message.text)
                except Exception:
                    result = "Incorrect input"

                text = lxml.html.fromstring(result)
                self.send_message(text.text_content(), msg.message.chat.id)

    def get_updates(self):
        res = requests.get(self.url + "/getUpdates?offset=" + self.offset)
        return res.json(), res.status_code

    def send_message(self, text, chat_id):
        URL = self.url + "/sendMessage"
        URL += f"?chat_id={chat_id}"
        URL += f"&text={text}"
        URL += "&parse_mode=html"
        res = requests.post(URL)
        return res.json(), res.status_code
