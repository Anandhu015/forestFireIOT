#include "DHT.h"
#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid     = "receiver_user";
const char* password = "receiver_pass";

const char* hostName = "192.168.1.160";
String post_request;
const char* resource_path = "/";

//--------------------------------------
int d32 = 5;
int Buzzer = 33;        // used for ESP32
int Gas_analog = 34;    // used for ESP32
int Gas_digital = 2;
#define pin_red 23
#define pin_green 22
float temp;
float humi;

DHT dht(d32, DHT11);// used for ESP32
//-------------------------------------

void turn_ON_WIFI() {
  WiFi.begin();
  Serial.println("WIFI ON");
  WiFi.begin(ssid, password);
  WiFi.setSleep(false);
  delay(2000);
}
//-------------------------------------
void sendDataTocentralNode(  String post_request, String resource_path, float humi, float temp, int gassensorAnalog, int gassensorDigital, boolean device_status1) {
   Serial.print("device_status:");
  Serial.println(device_status1);
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;
    String serverPath = post_request + resource_path + "?tmp_value=" + String(temp) + "&hum_value=" + String(humi) + "&gasanalog_value=" + String(gassensorAnalog) + "&gasdigital_value=" + String(gassensorDigital) + "&status=" + String(device_status1);
    http.begin(serverPath.c_str());
    int httpResponseCode = http.GET();
    if (httpResponseCode > 0) {
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
      String payload = http.getString();
      Serial.println(payload);
    }
    else {
      Serial.print("Error code: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  }

  delay(5000);
}
//---------------------------------------------------

void setup() {
  Serial.begin(115200);
  pinMode(Buzzer, OUTPUT);
  pinMode(pin_red, OUTPUT);
  pinMode(pin_green, OUTPUT);
  digitalWrite (Buzzer, LOW) ;
  pinMode(Gas_digital, INPUT);
  /* Start the DHT11 Sensor */
  dht.begin();

  post_request = String("http://");
  post_request += hostName;
  turn_ON_WIFI();
}

void loop() {

  int gassensorAnalog = analogRead(Gas_analog);
  int gassensorDigital = digitalRead(Gas_digital);


  humi = dht.readHumidity();
  temp = dht.readTemperature();

  if (gassensorAnalog > 350 && temp > 25) {
   

    Serial.println(gassensorAnalog);
    analogWrite(pin_red, 255);
    analogWrite(pin_green, 0);
    digitalWrite (Buzzer, HIGH) ; //send tone
    delay(1000);
    analogWrite(pin_red, 0);
    analogWrite(pin_green, 0);
    digitalWrite (Buzzer, LOW) ;
    delay(1000);//no tone
    

  }
  else {
  
    analogWrite(pin_green, 255);
    analogWrite(pin_red, 0);
    delay(1000);
    analogWrite(pin_green, 0);
    analogWrite(pin_red, 0);
   

  }
  delay(100);
  Serial.print("Gas value from sub-node:");
  Serial.println(gassensorAnalog);
  boolean device_status1;
  if (isnan(humi) || isnan(temp) || gassensorAnalog == 0) {
    device_status1 = false;

  }
  else {
    device_status1 = true;

  }
  
  sendDataTocentralNode(post_request, resource_path, humi, temp, gassensorAnalog, gassensorDigital, device_status1);

}