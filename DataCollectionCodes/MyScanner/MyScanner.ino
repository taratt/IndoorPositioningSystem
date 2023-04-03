// #include <BLEDevice.h>
// #include <BLEUtils.h>
// #include <BLEScan.h>
// #include <BLEAdvertisedDevice.h>

// #include <Arduino.h>

#include <NimBLEDevice.h>
#include <NimBLEAdvertisedDevice.h>
#include "NimBLEBeacon.h"

#include <PubSubClient.h>
#include <WiFi.h>


WiFiClient espClient;
PubSubClient client(espClient);

BLEScan* pBLEScan;
// NimBLEScan* pBLEScan;

void initWiFi() {
  const char* ssid = "Shanita2019";
  const char* password =  "tobeornottobe2020";
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi ..");
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print('.');
    delay(500);
  }
  Serial.println(WiFi.localIP());
}

void initMQTT() {
  const char* mqtt_broker = "192.168.1.144";
  const int mqtt_port = 1883;

  client.setServer(mqtt_broker, mqtt_port);
  client.setCallback(MQTTcallback);

  while (!client.connected()) 
  {
    Serial.println("Connecting to MQTT...");
    if (client.connect("ESP32","node","ESPNode"))
    {
      Serial.println("connected");
    }
    else
    {
      Serial.print("failed with state ");
      Serial.println(client.state());
      delay(1000);
    }
  }
}

void MQTTcallback(char* topic, byte* message, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.print(topic);
  Serial.print(". Message: ");
  String messageTemp;
  
  for (int i = 0; i < length; i++) {
    Serial.print((char)message[i]);
    messageTemp += (char)message[i];
  }
  Serial.println();
   if (String(topic) == "location"){
     ;
   }
}

class MyAdvertisedDeviceCallbacks: public BLEAdvertisedDeviceCallbacks {
    void onResult(BLEAdvertisedDevice *advertisedDevice) {
// class MyAdvertisedDeviceCallbacks: public NimBLEAdvertisedDeviceCallbacks {
//     void onResult(NimBLEAdvertisedDevice* advertisedDevice) {
      if (String((char *) advertisedDevice->getPayload()).substring(0,2) == "TT"){
        String fingerprintRecord = (char *)advertisedDevice->getPayload(); 
        fingerprintRecord = String(fingerprintRecord + '*');
        fingerprintRecord = String(fingerprintRecord +String(advertisedDevice->getRSSI()));
        fingerprintRecord = String(fingerprintRecord +'*');
        fingerprintRecord = String(fingerprintRecord + advertisedDevice->getAddress().toString().c_str());
        Serial.println(fingerprintRecord);
        
        client.publish("fingerprint",fingerprintRecord.c_str());
        // client.publish("fingerprint",(char *)advertisedDevice->getPayload());
       Serial.printf(" RSSI: %d \n", advertisedDevice->getRSSI());
       Serial.printf(" Payload: %s \n", advertisedDevice->getPayload());
       Serial.println(advertisedDevice->toString().c_str());

       }
    }
};

void setup() {
  Serial.begin(115200);
  initWiFi();
  initMQTT();
  
  BLEDevice::init("");  
  Serial.println(F("Scanning..."));
  pBLEScan = BLEDevice::getScan(); //create new scan
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  // pBLEScan->setActiveScan(true); //active scan uses more power, but get results faster
  pBLEScan->setInterval(100);
  pBLEScan->setWindow(99);  // less or equal setInterval value
  pBLEScan->setMaxResults(0);
}

void loop() {

  BLEScanResults foundDevices = pBLEScan->start(3, false);
  Serial.print(F("Devices found: "));
  Serial.println(F("Scan done!"));
  pBLEScan->clearResults();   // delete results fromBLEScan buffer to release memory
  delay(200);
}
