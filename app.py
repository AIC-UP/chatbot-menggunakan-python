from flask import Flask, request
import requests
import os
from dotenv import load_dotenv
from retrival_bot import main

load_dotenv()


# get dari env
bot_token = os.getenv('bot_token')
ngrok_url = os.getenv('ngrok_url')


app = Flask(__name__)


def send_message(text, chat_id):
    url = "https://api.telegram.org/bot{}/sendMessage".format(bot_token)
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    requests.get(url, params=payload)

@app.route("/", methods=['POST', 'GET'])
def index():
    if (requests.method == 'POST'):
        message = request.get_json()
        chat_id = message['message']['chat']['id']
        text = message['message']['text']

        if text == '/start':
            send_message('Selamat datang di bot Penerimaan Mahasiswa Baru Universitas Pahlawan', chat_id)
        else:
            if 'text' in message['message']:
                message_text = message['message']['text']
            else:
                message_text = 'No text'

            print(message_text)
            response = main(message_text)

            send_message(response, chat_id)

    return 'App is Working'

@app.route('/setwebhook')
def set_webhook():
    url = ngrok_url
    print(url)
    s = requests.get('https://api.telegram.org/bot{}/setWebhook?url={}'.format(bot_token, url))

    if s:
        return 'Koneksi Terhubung'
    else:
        return 'Koneksi Gagal'

if __name__ == '__main__':
    app.run(debug="True")