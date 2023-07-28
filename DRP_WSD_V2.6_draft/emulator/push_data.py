import os
import random
import sys
import time
from paho.mqtt.client import Client

par_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)
if par_dir not in sys.path:
    sys.path.append(par_dir)

from utils.constant import MQTT_WEIGHT_WHEEL, MQTT_WEIGHT_BS, MQTT_POTENTIOMETER
from settings import MQTT_HOST, MQTT_PORT, DEVICES, INTERVAL

mqtt_client = Client()


def on_mqtt_connected(client, userdata, flags, rc):
    print('MQTT: Connected to the Broker, Host: {}, Port: {}, UserData: {}, Flags: {}, Result code: {}'.format(
        MQTT_HOST, MQTT_PORT, userdata, flags, rc))


mqtt_client.on_connect = on_mqtt_connected
mqtt_client.connect(MQTT_HOST, MQTT_PORT)
mqtt_client.loop_start()


while True:
    try:
        s_time = time.time()

        for dev in DEVICES:
            mqtt_client.publish(topic=MQTT_WEIGHT_WHEEL.format(device=dev), payload=str(random.randint(-100, 2000)))
            mqtt_client.publish(topic=MQTT_WEIGHT_BS.format(device=dev), payload=str(random.randint(-100, 750)))
            mqtt_client.publish(topic=MQTT_POTENTIOMETER.format(device=dev), payload=str(random.randint(0, 200)))
            time.sleep(1)

        elapsed = time.time() - s_time
        time.sleep(max(INTERVAL - elapsed, 0))
    except KeyboardInterrupt:
        break
