#Author: Cheuk Hang Ku
#Date: 22/4/2022
#File:Client1.py
#Description: Publish a random number between 1 and 100 to Mosquito mqtt

# Importing class
import random
import time
import paho.mqtt.client as mqtt

broker = "mqtt.eclipseprojects.io"
port = 1883
topic = "Random"


def connect_mqtt():
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Client 1 Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    # Create a new client instance
    client1 = mqtt.Client("", True, None, mqtt.MQTTv31)
    # make sure the connection is done
    client1.on_connect = on_connect
    # Connecting to a Broker
    # Format (Broker IP Address, TCP port, Websocket Port)
    # Broker used: HiveMQ
    client1.connect("test.mosquitto.org", 1883, 60)
    return client1


def publish(client):
    # Random generator function
    randomNumber = random.randint(1, 100)
    while True:
        # Publish message
        result = client.publish("Random", randomNumber)
        status = result[0]
        if status == 0:
            print("client 1 sent message")
        else:
            print("Client 1 Failed to send message")
        # Sleep for random time between 1 and 30 seconds
        time.sleep(random.randint(1, 30))


def main():
    client = connect_mqtt()
    client.loop_start()
    publish(client)


if __name__ == '__main__':
    main()
