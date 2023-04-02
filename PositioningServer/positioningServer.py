import paho.mqtt.client as paho


class PositioningServer:
    def __init__(self, brokerIP, brokerPort, mode):
        self.brokerIP = brokerIP
        self.port = brokerPort
        self.mode = mode

        self.client = paho.Client("client")
        if mode =="offline":
            self.client.on_message = self.on_message_offline
        elif mode == "online":
            self.client.on_message = self.on_message_online
        self.client.username_pw_set(username='Server', password='IPS')
        self.client.connect(self.brokerIP, port= self.port, keepalive=60)
        print("connected to the broker")
        self.client.subscribe("fingerprint")
        self.client.loop_forever()


    def on_message_offline(self, client, userdata, message):
        fingerprint_record = message.payload.decode('utf-8')
        print(fingerprint_record)
        fingerprint_record = fingerprint_record.split('*')

        # Fingerprints(advertised_device = fingerprint_record[0])









