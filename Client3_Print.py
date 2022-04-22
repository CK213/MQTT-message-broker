#Author: Cheuk Hang Ku
#Date: 22/4/2022
#File:Client3_Print.py
#Description: Subscribe the message published by Client2_Average.py and print out one minute, 5 minute, and 30 minutes averages to a pretty table.

# Importing class
import paho.mqtt.client as mqtt
from prettytable import PrettyTable

t = PrettyTable(["Time", "Average number"])

broker = "mqtt.eclipseprojects.io"
port = 1883


# The callback for when the client receives a CONNACK response from the server.
def connect_mqtt() -> mqtt:
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Client 3 Connected to MQTT Broker!")
        else:
            print("Client 3 Failed to connect, return code %d\n", rc)

    # Create a new client instance
    client3 = mqtt.Client("", True, None, mqtt.MQTTv31)
    # make sure the connection is done
    client3.on_connect = on_connect
    # Connecting to a Broker
    # Format (Broker IP Address, TCP port, Websocket Port)
    # Broker used: HiveMQ
    client3.connect("test.mosquitto.org", 1883, 60, "")
    return client3


def subscribe(client: mqtt):
    # The callback for when a PUBLISH message is recieved from the server.
    # Add all number to list
    while True:
        def on_message(client, userdata, msg):
            if msg.topic == "staticsGG/1min":
                t.add_row(["1 min", msg.payload.decode()])
                print(t)
            if msg.topic == "statics/5min":
                t.add_row(["5 mins", msg.payload.decode()])
                print(t)
            if msg.topic == "statics/30min":
                t.add_row(["30 mins", msg.payload.decode()])
                print(t)

        client.subscribe("statics/#")
        client.on_message = on_message


def main():
    client = connect_mqtt()
    client.loop_start()
    subscribe(client)


if __name__ == '__main__':
    main()
