import os
import app
import paho.mqtt.client as paho
import requests
import time

MQTT_USER = os.environ.get("MQTT_USER")
MQTT_PASS = os.environ.get("MQTT_PASS")

SLACK_API = 'https://slack.com/api/chat.postMessage'

MENSION_TARGET = '<@U0275UW8LNM>'

temp_max_threshold = 25.0
notify_interval = 60.0


def on_connect(mqttc, obj, flags,rc):
    mqttc.subscribe('WTout/temp' ,0)
    mqttc.subscribe('WTout/jpg', 0)
    mqttc.subscribe('WTout/jpg/done', 0)
    print("rc: "+str(rc))


def run():
    mqttc = paho.Client()
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_subscribe = on_subscribe
    mqttc.username_pw_set(MQTT_USER,MQTT_PASS)
    mqttc.connect('ambystoma.f5.si', 1883, 60)
    mqttc.loop_forever()

file_opened = False
file_buffer = bytearray()
filename = 0
start = time.time()
isNotifyRecently = False

def on_message(mqttc, obj, msg):
    print(msg.topic+" "+str(msg.qos))
    global start
    global isNotifyRecently

    if msg.topic == "WTout/temp" :
        temp = (msg.payload).decode()
        print((msg.payload).decode())

        if time.time() - start > notify_interval  :
            isNotifyRecently = False

        if float(temp) > temp_max_threshold and isNotifyRecently == False:
            overheat_text = app.MENSION_TARGET + ' 水温が高すぎます！現在' + str(temp) + '℃です！'
            isNotifyRecently = True
            start = time.time()
            data = {
                    'token': app.BOT_TOKEN,
                    'channel': app.SLACK_CHANNEL,
                    'text': overheat_text,
                    'username': MENSION_TARGET
                }
            response = requests.post(SLACK_API, data=data)
            print(response.text)

    global file_buffer
    global filename
    if msg.topic == "WTout/jpg":
        file_buffer += msg.payload
        
    elif msg.topic== "WTout/jpg/done":
            with open(str(filename) + ".jpg", "wb") as outfile:
                outfile.write(file_buffer)
            outfile.close()
            file_buffer = bytearray()
    

def on_publish(mqttc, obj, mid):
    print("mid: "+str(mid))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_log(mqttc, obj, level, string):
    print(string)



# if __name__ == '__main__':
# 
#     mqttc = paho.Client()
#     mqttc.on_message = on_message
#     mqttc.on_connect = on_connect
#     mqttc.on_subscribe = on_subscribe
# 
#     mqttc.username_pw_set('conomag','K6812990bps')
#     mqttc.connect('localhost', 1883, 60)
# 
# 
#     mqttc.loop_forever()

