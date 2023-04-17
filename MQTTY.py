import random 
import time
import paho.mqtt.client as mqtt_client

broker_address = "localhost"
broker_port = 1883
topic = "/python/mqtt"

# broker generate #1
def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker")
        else: print(f"Failed to connect, Returned code: {rc}")
    
    def on_disconnect(client, userdata, flags, rc = 0):
        print(f"disconnected result code {str(rc)}")
    
    def on_log(client, userdata, level, buf):
        print(f"log: {buf}")

    #client generate #2
    client_id = f"mqtt_client_{random.randint(0, 1000)}"
    client = mqtt_client.Client(client_id)

    #callback function set #3
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_log = on_log

    #broker connect #4
    client.connect(host = broker_address, port = broker_port)
    return client

def publish(client: mqtt_client):
    msg_count = 0
    while True:
        time.sleep(1)
        msg = f"message:{msg_count}"
        result = client.publish(topic, msg)
        #result: {0, 1}
        
        status = result[0]
        if status == 0:
            print(f"Send '{msg}' to topic '{topic}'")
        else: 
            print(f"Failed to send message to topic {topic} ")
        msg_count += 1

def run():
    client = connect_mqtt()
    client.loop_start()
    print(f"connect to broker {broker_address} : {broker_port}")
    publish(client)
    
if __name__ == '__main__':
    run()
    Client(client_id = "", clean_session = True, userdata = None, protocol = MQTTv311, transport = "tcp")
