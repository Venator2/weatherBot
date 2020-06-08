import json
from time import sleep
from pprint import pprint
import requests
import temperature


class WeatherBot():

    def __init__(self):
        self.token = '1129204534:AAETU7HGxWM2kxdj1trCUqInsnzGlTlKyA4'
        self.url = 'https://api.telegram.org/bot{}/'.format(self.token)

    def get_updates(self, offset=None):
        while True:
            try:
                URL = self.url + 'getUpdates'
                if offset:
                    URL += '?offset={}'.format(offset)

                r = requests.get(URL)
                while (r.status_code != 200 or len(r.json()['result']) == 0):
                    sleep(1)
                    r = requests.get(URL)
                print(r.url)
                return r.json()

            except:
                pass

    def get_last(self, data):

        results = data['result']
        count = len(results)
        last = count - 1
        last_update = results[last]
        return last_update

    def get_last_id_text(self, updates):
        last_update = self.get_last(updates)
        self.chat_id = last_update['message']['chat']['id']
        update_id = last_update['update_id']
        try:
            text = last_update['message']['text']
        except:
            text = ''
        return self.chat_id, text, update_id

    def ask_location(self, chat_id):
        print('Ask Location')
        text = 'Send Location'
        keyboard = [[{"text": "Location", "request_location": True}]]
        reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
        self.send_message(chat_id, text, json.dumps(reply_markup))

    def get_location(self, update_id):
        print('Get Location')
        updates = self.get_updates(update_id+1)
        location = self.get_last(updates)['message']['location']
        chat_id, text, update_id = self.get_last_id_text(updates)
        lat = str(location['latitude'])
        lon = str(location['longitude'])
        return lat, lon, update_id

    def send_message(self, chat_id, text, reply_markup=None):
        URL = self.url + \
            "sendMessage?text={}&chat_id={}&parse_mode=Markdown".format(
                text, chat_id)
        if reply_markup:
            URL += '&reply_markup={}'.format(reply_markup)
        r = requests.get(URL)
        while r.status_code != 200:
            r = requests.get(URL)
        print(r.status_code)

    def reply_markup_maker(self, data):
        keyboard = []
        for i in range(0, len(data), 2):
            key = []
            key.append(data[i].title())
            try:
                key.append(data[i+1].title())
            except:
                pass
            keyboard.append(key)

        reply_markup = {"keyboard": keyboard, "one_time_keyboard": True}
        return json.dumps(reply_markup)

    def weather(self, chat_id, update_id):
        self.ask_location(chat_id)
        lat, lon, update_id = self.get_location(update_id)
        message = temperature.w.temp(lat, lon)
        self.send_message(chat_id, message)

    def welcome_note(self, chat_id, commands):
        text = "Bot Welcomes You"
        self.send_message(chat_id, text)
        text = 'Select'
        reply_markup = self.reply_markup_maker(commands)
        self.send_message(chat_id, text, reply_markup)

    def start(self, chat_id):
        message = 'Wanna Start'
        reply_markup = self.reply_markup_maker(['Start'])
        self.send_message(chat_id, message, reply_markup)

        chat_id, text, update_id = self.get_last_id_text(self.get_updates())
        while(text.lower() != 'start'):
            chat_id, text, update_id = self.get_last_id_text(
                self.get_updates(update_id+1))
            sleep(0.5)

        return chat_id, text, update_id

    def end(self, chat_id, text, update_id):
        message = 'Do you wanna end?'
        reply_markup = self.reply_markup_maker(['Yes', 'No'])
        self.send_message(chat_id, message, reply_markup)

        new_text = text
        while(text == new_text):
            chat_id, new_text, update_id = self.get_last_id_text(
                self.get_updates(update_id+1))
            sleep(1)

        if new_text == 'Yes':
            return 'y'
        else:
            return 'n'

    def menu(self, chat_id, text, update_id):

        commands = ['weather']
        self.welcome_note(chat_id, commands)

        while(text.lower() == 'start'):
            chat_id, text, update_id = self.get_last_id_text(
                self.get_updates(update_id+1))
            sleep(0.5)
        print(text)
        while text.lower() not in commands:
            chat_id, text, update_id = self.get_last_id_text(
                self.get_updates(update_id+1))
            sleep(0.5)

        if text.lower() == 'weather':
            self.weather(chat_id, update_id)

    def main(self):
        text = ''
        chat_id, text, update_id = self.get_last_id_text(self.get_updates())
        chat_id, text, update_id = self.start(chat_id)
        print('Started')

        while text.lower() != 'y':
            sleep(1)
            text = 'start'
            self.menu(chat_id, text, update_id)
            text = 'y'

            chat_id, text, update_id = self.get_last_id_text(
                self.get_updates())
            text = self.end(chat_id, text, update_id)


b = WeatherBot()
if __name__ == '__main__':
    b.main()
