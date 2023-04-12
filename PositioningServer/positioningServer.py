import paho.mqtt.client as paho
from datetime import datetime
from PositioningServer.fingerprintDatabase import *

class PositioningServer:
    def __init__(self, brokerIP, brokerPort, mode, level, scan_counter):
        self.brokerIP = brokerIP
        self.port = brokerPort
        self.mode = mode
        self.level = level

        self.attributes = ['beacon1', 'channel1', 'beacon2', 'channel2', 'beacon3', 'channel3', 'beacon4', 'channel4', 'beacon5','channel5',
    'beacon6', 'channel6', 'beacon7','channel7', 'beacon8', 'channel8', 'beacon9', 'channel9', 'beacon10', 'channel10', 'beacon11','channel11',
                           'beacon12', 'channel12', 'beacon13', 'channel13', 'beacon14','channel14', 'beacon15', 'channel15', 'beacon16', 'channel16', 'beacon17', 'channel17', 'beacon18',
                           'channel18', 'beacon19', 'channel19', 'beacon20', 'channel20', 'beacon21', 'channel21', 'beacon22', 'channel22']

        self.client = paho.Client("client")
        if mode =="offline":
            self.client.on_message = self.on_message_offline
            self.scan_counter = scan_counter
        elif mode == "online":
            self.client.on_message = self.on_message_online
        self.client.username_pw_set(username='Server', password='IPS')
        self.client.connect(self.brokerIP, port= self.port, keepalive=60)
        print("connected to the broker")
        self.client.subscribe([("fingerprint",0),("scanFinished",0)])
        self.client.loop_forever()

    @db_session
    def on_message_offline(self, client, userdata, message):
      try:
        if message.topic == "fingerprint":

            now = datetime.datetime.now()
            fingerprint_record = message.payload.decode('utf-8')
            fingerprint_record = fingerprint_record.split('*')
            advertising_device_mac, rssi = fingerprint_record[2], fingerprint_record[1]
            channel = fingerprint_record[0].split('-')[1]

            current_beacon = Beacon.get(mac_address = advertising_device_mac, level= self.level)
            if  current_beacon == None:
                registered_beacons_count = count(b for b in Beacon)
                current_beacon = Beacon(mac_address = advertising_device_mac, beacon_name ="beacon"+str(registered_beacons_count+1))

            Advertisement(advertised_device = current_beacon, rssi = rssi,advertised_channel = channel, date = now,location = "unknown", scan_number = self.scan_counter)
            print("stored from: "+current_beacon.beacon_name)

        elif message.topic == "scanFinished":
          if message.payload.decode('utf-8') == "T":
            print("Scan "+ str(self.scan_counter) + " finished.")

            unlabeled = select(f for f in Advertisement if f.location == "unknown")[:]
            if len(unlabeled) > 50:
                for i in unlabeled[0:len(unlabeled) - 50]:
                #    print(len(unlabeled))
                    i.location = "lost"
            unlabeled = select(f for f in Advertisement if f.location == "unknown")[:]
            if len(unlabeled)!=0:
                fingerprint = Fingerprint(scan_number = self.scan_counter, date = unlabeled[0].date, location= "unknown")
                for f in unlabeled:
                    setattr(fingerprint,getattr(f,'advertised_device').beacon_name,f.rssi)
                    setattr(fingerprint,self.attributes[self.attributes.index(getattr(f,'advertised_device').beacon_name)+1], f.advertised_channel)

                self.scan_counter +=1

          elif message.payload.decode('utf-8') == "L":
                location_label = input("Please enter the location label: ")
                unlabeled = select(f for f in Advertisement if f.location == "unknown")[:]
                for f in unlabeled:
                    f.location = location_label

                unlabeled = select(f for f in Fingerprint if f.location == "unknown")[:]
                if len(unlabeled) > 21:
                    for i in unlabeled[0:len(unlabeled) - 21]:
                        i.location = "lost"

                unlabeled = select(f for f in Fingerprint if f.location == "unknown")[:]
                for f in unlabeled:
                    f.location = location_label
      except:
          print("oh no")

    def on_message_online(self, client, userdata, message):
        pass





