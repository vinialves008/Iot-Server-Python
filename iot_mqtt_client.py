import paho.mqtt.client as mqtt
import time
import random
import json


mqtt_broker = "local.modesto.com.br"
mqtt_broker_port = 1883
mqtt_keep_alive = 60

cmd_status_controle = False

mqtt_topic_pub = "iot/senai/101/modesto/cmd"
mqtt_topic_sub = "iot/senai/101/modesto/data"

def on_connect(client, userdata, flags, rc):
    print("Conectado! - Status: " + str(rc))
    client.subscribe(mqtt_topic_sub)

def on_message(client, userdata, msg):
    global cmd_status_controle
    msg_recv = str(msg.payload, 'utf-8')
    print("MSG: [" + msg.topic + "] - " + msg_recv)
    msg_json = json.loads(msg_recv)
    #print(msg_json['TEMP'])
    if msg_json["TEMP"] > 27.0:
        cmd_status_controle = True
    else:
        cmd_status_controle = False
    

if __name__ == '__main__':
    print("Iniciando aplicação Cliente MQTT...")
    client = mqtt.Client(client_id="iot_python_vinialves08", clean_session=True)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_broker, mqtt_broker_port, mqtt_keep_alive)
    time.sleep(5)

    client.loop_start()

    while True:
        time.sleep(5)
        if cmd_status_controle:
            client.publish(mqtt_topic_pub, "ON")
        else:
            client.publish(mqtt_topic_pub, "OFF")
