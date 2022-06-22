

#include <WiFi.h>
#include <HTTPClient.h>
#include "DHT.h" // DHT library from Adafruit
//Adafruit Unified Sensor library.



//used for server connection
//-----------------------------------------
String temperature_value, humidity_value, gas_analog, gas_digital,device_status1;
const char* ssid     = "Realmenarzo";
const char* password = "alien@123";
char simple_json1[200];
char json[200];
//Your Domain name with URL path or IP address with path
const char* serverName = "http://192.168.121.158:8000/readings";

// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastTime = 0;
// Timer set to 10 minutes (600000)
//unsigned long timerDelay = 600000;
// Send data every  30 seconds (5000)
unsigned long timerDelay = 5000;
//----------------------------------------
//second esp32 connection

// Set static IP
IPAddress AP_LOCAL_IP(192, 168, 1, 160);
IPAddress AP_GATEWAY_IP(192, 168, 1, 4);
IPAddress AP_NETWORK_MASK(255, 255, 255, 0);


//----------------------------------------

//give Accesspoint SSID and passcode, your esp's hotspot name
const char *Apssid = "receiver_user";
const char *Appassword = "receiver_pass";
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>
AsyncWebServer server(80);

const char index_html[] PROGMEM = R"rawliteral(
<html>
  <body>
    connection Sucess
  </body>
</html>
)rawliteral";


//Used for sensor reading
//=========================================
int d32 = 5;
int Buzzer = 33;        // used for ESP32
int Gas_analog = 34;    // used for ESP32
int Gas_digital = 2;
#define pin_red 23
#define pin_green 22
float temp;
float humi;
int led=19;
DHT dht(d32, DHT11);
//=========================================
//ESP32 connection(second)
String processor(const String& var){
  return String();
}


//----------------------------------------------------------------
void server_Connection(const char* serverName,float humi,float temp,int gasanalog,int gasdigital) {
  if ((millis() - lastTime) > timerDelay) {
    //Check WiFi connection status
    if (WiFi.status() == WL_CONNECTED) {
      WiFiClient client;
      HTTPClient http;

      // Your Domain name with URL path or IP address with path
      http.begin(client, serverName);
      boolean device_status;
      // If you need an HTTP request with a content type: application/json, use the following:

      http.addHeader("Content-Type", "application/json");
      if(isnan(humi)|| isnan(temp) || gasanalog == 0){
        device_status=false;
        pinMode(led,HIGH);
      }
      else{
        device_status=true;
        pinMode(led,LOW);
      }
      Serial.println("device_status:");
      Serial.print(device_status);
      
      sprintf(simple_json1, "{\"device_id\":\"%d\",\"temp_reading\":\"%.2f\",\"hum_reading\":\"%.2f\",\"device_status\":\"%d\",\"smoke_reading\":\"%d\"}", 1, temp, humi,device_status,gasanalog);
      int httpResponseCode1 = http.POST(simple_json1);
      delay(1000);
      sprintf(json, "{\"device_id\":\"%d\",\"temp_reading1\":\"%s\",\"hum_reading1\":\"%s\",\"device_status\":\"%d\",\"gas_analog_reading1\":\"%s\"}", 2,temperature_value,humidity_value,boolean(device_status1),gas_analog);
      
      //sending post request
     
      int httpResponseCode2 = http.POST(json);
      Serial.print("temperature:");
      Serial.println(temp);
      Serial.print("humidity:");
      Serial.println(humi);
      Serial.print("gas:");
      Serial.println(gasanalog);
      Serial.print("temperature2:");
      Serial.println(temperature_value);
      Serial.print("humidity2:");
      Serial.println(humidity_value);
      Serial.print("gas2:");
      Serial.println(gas_analog);

      Serial.print("HTTP Response code1: ");
      Serial.println(httpResponseCode1);
      Serial.print("HTTP Response code2: ");
      Serial.println(httpResponseCode2);

      // Free resources
      http.end();
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }

}
void setup() {
  Serial.begin(115200);
   pinMode(Buzzer, OUTPUT);
  pinMode(pin_red, OUTPUT);
  pinMode(pin_green, OUTPUT);
  digitalWrite (Buzzer, LOW) ;
  pinMode(Gas_digital, INPUT);
  /* Start the DHT11 Sensor */
  dht.begin();
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
  
  Serial.println("Timer set to 5 seconds (timerDelay variable), it will take 5 seconds before publishing the first reading.");
  WiFi.mode(WIFI_AP_STA);
  WiFi.softAP(Apssid, Appassword);
  WiFi.setSleep(false);
  
  if (!WiFi.softAPConfig(AP_LOCAL_IP, AP_GATEWAY_IP, AP_NETWORK_MASK)) {
    Serial.println("AP Config Failed");
    return;
  }
  IPAddress myIP = WiFi.softAPIP();
  Serial.print("Access Point IP address: ");
  Serial.println(myIP);
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
     
      if (request->hasParam("tmp_value")) {
        temperature_value = request->getParam("tmp_value")->value();
        Serial.print("Received temperature value is : ");
        Serial.println(temperature_value);
        humidity_value = request->getParam("hum_value")->value();
        Serial.print("Received humidity value is : ");
        Serial.println(humidity_value);
        gas_analog = request->getParam("gasanalog_value")->value();
        Serial.print("Received gas analog value is : ");
        Serial.println(gas_analog);
        
        gas_digital= request->getParam("gasdigital_value")->value();
        Serial.print("Received gas digital value is : ");
        Serial.println(gas_digital);
        device_status1= request->getParam("status")->value();
        Serial.print("Received device status value is : ");
        Serial.println(device_status1);
      }
    request->send_P(200, "text/html", index_html, processor);
  });

  server.begin();


}
void loop() {
    int gassensorAnalog = analogRead(Gas_analog);
  int gassensorDigital = digitalRead(Gas_digital);


  humi = dht.readHumidity();
  temp = dht.readTemperature();
  if (isnan(humi) && isnan(temp) ) {


  }
  else {
    Serial.print("Temperature: ");
    Serial.print(temp);
    Serial.print("ºC ");
    Serial.print("Humidity: ");
    Serial.println(humi);
    delay(1000);
  }

  if (gassensorAnalog > 1000 && temp > 30) {
    Serial.println("Gas");
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
    Serial.println("No Gas");
    analogWrite(pin_green, 255);
    analogWrite(pin_red, 0);
    delay(1000);
    analogWrite(pin_green, 0);
    analogWrite(pin_red, 0);
    Serial.println(gassensorAnalog);

  }
  delay(100);
  server_Connection(serverName,humi,temp,gassensorAnalog,gassensorDigital);

}
