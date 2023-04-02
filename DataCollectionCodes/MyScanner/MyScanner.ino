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
  // Serial.println(WiFi.localIP());
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
      String fingerprintRecord = ""; 
      if (advertisedDevice->haveName())
        fingerprintRecord = String(advertisedDevice->getName().c_str() + '*' );
      fingerprintRecord = String(fingerprintRecord + '*');
      fingerprintRecord = String (fingerprintRecord + advertisedDevice->getRSSI());
      client.publish("fingerprint",fingerprintRecord.c_str());
      Serial.printf("Advertised Device: %s \n", advertisedDevice->toString().c_str());
      Serial.printf(" RSSI: %d \n", advertisedDevice->getRSSI());
    }
};

void setup() {
  Serial.begin(115200);
  initWiFi();
  initMQTT();
  

  Serial.println(F("Scanning..."));
  BLEDevice::init("");
  pBLEScan = BLEDevice::getScan(); //create new scan
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
 // pBLEScan->setActiveScan(true); //active scan uses more power, but get results faster
  pBLEScan->setInterval(100);
  pBLEScan->setWindow(99);  // less or equal setInterval value
}

void loop() {
  BLEScanResults foundDevices = pBLEScan->start(5, false);
  Serial.print(F("Devices found: "));
  Serial.println(F("Scan done!"));
  pBLEScan->clearResults();   // delete results fromBLEScan buffer to release memory
  delay(2000);
}