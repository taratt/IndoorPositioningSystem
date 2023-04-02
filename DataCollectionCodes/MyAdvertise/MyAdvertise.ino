#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

// See the following for generating UUIDs:
// https://www.uuidgenerator.net/

#define BEACON_NAME            "TaraTT IPS Node1"
#define SERVICE_UUID        "50c36274-c290-11ed-afa1-0242ac120002"

void changeChannel(int channelNumber){
  BLEDevice::stopAdvertising();
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  BLEAdvertisementData advertisingChannel = BLEAdvertisementData();
  switch(channelNumber) {
  case 37:
    pAdvertising->setAdvertisementChannelMap(ADV_CHNL_37);
    advertisingChannel.setName("37");
    Serial.println("on 37");
    break;

  case 38:
    pAdvertising->setAdvertisementChannelMap(ADV_CHNL_38);
    advertisingChannel.setName("38");
    Serial.println("on 38");

    break;
  case 39:
    pAdvertising->setAdvertisementChannelMap(ADV_CHNL_39);
    advertisingChannel.setName("39");
    Serial.println("on 39");
}

  pAdvertising->setAdvertisementData(advertisingChannel);
  BLEDevice::startAdvertising();

}


void setup() {
  Serial.begin(115200);
  Serial.println("Starting BLE!");

//creating the server
  BLEDevice::init(BEACON_NAME);
  BLEServer *pServer = BLEDevice::createServer();

//creating the service
  BLEService *pService = pServer->createService(SERVICE_UUID);
  pService->start();

//advertising the service
  BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
  pAdvertising->addServiceUUID(SERVICE_UUID);
  pAdvertising->setScanResponse(true);
  // pAdvertising->setMinInterval(0x100);
  // pAdvertising->setMaxInterval(0x100);
  pAdvertising->setMinPreferred(0x06);  // functions that help with iPhone connections issue
  pAdvertising->setMinPreferred(0x12);

//initializing the advertising channel to 37
  pAdvertising->setAdvertisementChannelMap(ADV_CHNL_37);

  BLEAdvertisementData advertisingChannel = BLEAdvertisementData();
  advertisingChannel.setManufacturerData("37");
  pAdvertising->setAdvertisementData(advertisingChannel);
  
  BLEDevice::startAdvertising();
}

void loop() {
  changeChannel(37);
  delay(1000);
  changeChannel(38);
  delay(1000);
  changeChannel(39);
  delay(1000);
}