import logging,os

import threading
import mqtt

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


APP_TOKEN = os.environ.get("SLACK_APP_TOKEN)")
BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN)")

SLACK_CHANNEL = '#general'


app = App(token=BOT_TOKEN)

@app.message("hello")
def message_hello(message,say):
    say(f"Hey there <@{message['user']}>!")

@app.message("画像くれ")
def post_image(message,say):
    say(f"いいよ <@{message['user']}>!")
    upload_text_file = app.client.files_upload(
    channels="#general",
    title="image",
    file="./0.jpg",
)


def mqtt_run():
    mqtt.run()


mqtt_thread = threading.Thread(target=mqtt_run)

if __name__ == "__main__":

    mqtt_thread.start()
    SocketModeHandler(app,os.environ["SLACK_APP_TOKEN"]).start()