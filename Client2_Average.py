#Author: Cheuk Hang Ku
#Date: 22/4/2022
#File:Client2_Average.py
#Description: Subscribe the message published by Client1.py and calculate one minute, 5 minute, and 30 minutes averages. Then publish to Mosquitto Broker.

# Importing class
from statistics import mean
import paho.mqtt.client as mqtt
import time
from schedule import every, repeat, run_pending

oldtime = time.time()
total = list()
# result = []

broker = "mqtt.eclipseprojects.io"
port = 1883


# Find average
def average(total):
    avg = list(map(int, total))
    return mean(avg)


# The callback for when the client receives a CONNACK response from the server.
def connect_mqtt() -> mqtt:
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Client 2 Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    # Create a new client instance
    client2 = mqtt.Client("", True, None, mqtt.MQTTv31)
    # make sure the connection is done
    client2.on_connect = on_connect
    # Connecting to a Broker
    # Format (Broker IP Address, TCP port, Websocket Port)
    # Broker used: HiveMQ
    client2.connect("test.mosquitto.org", 1883, 60, "")
    return client2


def subscribe(client: mqtt):
    # The callback for when a PUBLISH message is recieved from the server.
    # Add all number to list
    def on_message(client, userdata, msg):
        total.extend(msg.payload.decode())

    client.subscribe("Random")
    client.on_message = on_message
    time.sleep(30)


def publish(client):
    # calculate average and publish message
    @repeat(every(1).minute)
    def one_min():
        avg = average(total)
        result = client.publish("statics/1min", avg)
        time.sleep(59)
        try:
            status = result[0]
            if status == 0:
                print("client 2 sent message")
            else:
                print("Client 2 Failed to send message")
        except:
            time.sleep(1)

    @repeat(every(5).minutes)
    def five_min():
        avg = average(total)
        result = client.publish("statics/5min", avg)
        time.sleep(59)
        try:
            status = result[0]
            if status == 0:
                print("client 2 sent message")
            else:
                print("Client 2 Failed to send message")
        except:
            time.sleep(1)

    @repeat(every(30).minutes)
    def thirty_min():
        avg = average(total)
        result = client.publish("statics/30min", avg)
        time.sleep(59)
        # Check if the message was sent
        try:
            status = result[0]
            if status == 0:
                print("client 2 sent message")
            else:
                print("Client 2 Failed to send message")
        except:
            time.sleep(1)

    while True:
        run_pending()
        time.sleep(1)


def main():
    client = connect_mqtt()
    client.loop_start()
    subscribe(client)
    publish(client)


if __name__ == '__main__':
    main()
