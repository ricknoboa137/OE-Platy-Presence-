#include <ESP8266WiFi.h>
#include "Adafruit_MQTT.h"
#include "Adafruit_MQTT_Client.h"
#include <Servo.h>

Servo servo1;
Servo servo2;
const unsigned int MAX_MESSAGE_LENGTH = 12;
unsigned long startMillis;  //some global variables available anywhere in the program
unsigned long currentMillis;


/************************* WiFi Access Point *********************************/

#define WLAN_SSID       "IROB"
#define WLAN_PASS       "Ha62Me52"

/************************* Adafruit.io Setup *********************************/

#define AIO_SERVER      "10.8.8.181"
#define AIO_SERVERPORT  1883                   // use 8883 for SSL
#define AIO_USERNAME    ""
#define AIO_KEY         ""
/************ Global State (you don't need to change this!) ******************/

// Create an ESP8266 WiFiClient class to connect to the MQTT server.
WiFiClient client;
// or... use WiFiClientSecure for SSL
//WiFiClientSecure client;

// Setup the MQTT client class by passing in the WiFi client and MQTT server and login details.
Adafruit_MQTT_Client mqtt(&client, AIO_SERVER, AIO_SERVERPORT, AIO_USERNAME, AIO_KEY);

/****************************** Feeds ***************************************/

// Setup a feed called 'photocell' for publishing.
// Notice MQTT paths for AIO follow the form: <username>/feeds/<feedname>
Adafruit_MQTT_Publish photocell = Adafruit_MQTT_Publish(&mqtt, AIO_USERNAME "photocell");

// Setup a feed called 'onoff' for subscribing to changes.
Adafruit_MQTT_Subscribe test1 = Adafruit_MQTT_Subscribe(&mqtt, AIO_USERNAME "test1");

/*************************** Sketch Code ************************************/

// Bug workaround for Arduino 1.6.6, it seems to need a function declaration
// for some reason (only affects ESP8266, likely an arduino-builder bug).
void MQTT_connect();

void setup() {
  Serial.begin(115200);
  pinMode(LED_BUILTIN, OUTPUT); 
  servo1.attach(4); //D2 Horizontal
  servo2.attach(5); //D1 Vertical
  delay(10);
  Serial.println("Servos attached");
  Serial.println(F("Adafruit MQTT demo"));

  // Connect to WiFi access point.
  Serial.println(); Serial.println();
  Serial.print("Connecting to ");
  Serial.println(WLAN_SSID);

  WiFi.begin(WLAN_SSID, WLAN_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();

  Serial.println("WiFi connected");
  Serial.println("IP address: "); Serial.println(WiFi.localIP());

  // Setup MQTT subscription for onoff feed.
  mqtt.subscribe(&test1);
  delay(2000);
  startMillis = millis();  //initial start time
}

uint32_t x=0;
float oculusValues [5]={0,0,0,0,0};
long rotHor, rotVer, joyHor,joyVer, buttonA;


void loop() {
  digitalWrite(LED_BUILTIN, LOW);  // Turn the LED on (Note that LOW is the voltage level
  // but actually the LED is on; this is because
  // it is active low on the ESP-01)
  delay(100);                      // Wait for a second
  digitalWrite(LED_BUILTIN, HIGH);  // Turn the LED off by making the voltage HIGH
  delay(200);  
  //Read numbers from console (Serial Monitor) and write it as servo angle
  while (Serial.available() > 0)
 {
   //Create a place to hold the incoming message
   static char message[MAX_MESSAGE_LENGTH];
   static unsigned int message_pos = 0;
   //Read the next available byte in the serial receive buffer
   char inByte = Serial.read();
   //Message coming in (check not terminating character) and guard for over message size
   if ( inByte != '\n' && (message_pos < MAX_MESSAGE_LENGTH - 1) )
   {
     //Add the incoming byte to our message
     message[message_pos] = inByte;
     message_pos++;
   }
   //Full message received...
   else
   {
     //Add null character to string
     message[message_pos] = '\0';
     //Print the message (or do other things)
     Serial.println(message);
     int number = atoi(message);
     servo1.write(number);
     //Reset for the next message
     message_pos = 0;
   }
 }
  // Ensure the connection to the MQTT server is alive (this will make the first
  // connection and automatically reconnect when disconnected).  See the MQTT_connect
  // function definition further below.
  MQTT_connect();

  // this is our 'wait for incoming subscription packets' busy subloop
  // try to spend your time here

  Adafruit_MQTT_Subscribe *subscription;
  while ((subscription = mqtt.readSubscription(5000))) {
    if (subscription == &test1) {
      //Serial.print(F("Got: "));
      //Serial.println((char *)test1.lastread);
      char* token;
      x=0;
      token = strtok((char *)test1.lastread,",");
      while(token)
      {
        oculusValues[x] = atof(token);
        //Serial.println(oculusValues[x]);
        x++;
        token = strtok(NULL,",");
        
      }
      

      rotVer=oculusValues[0]*100;
      rotHor=oculusValues[1]*100;
      joyHor=oculusValues[2]*100;
      joyVer=oculusValues[3]*100;
      buttonA=oculusValues[4]*100;
      //Serial.print(map(rotVer,-40,25,0,70));
      Serial.print(rotVer);
      Serial.print(",");
      Serial.print(rotHor);
      Serial.print(",");
      Serial.print(joyVer);
      Serial.print(",");
      Serial.print(joyHor);
      Serial.print(",");
      Serial.println(buttonA);
      x=0;
      currentMillis=millis();
      if (currentMillis-startMillis >= 500)
       {
          UpdateServos();
          startMillis=millis();
       }
        
    }
  }

  // Now we can publish stuff!
  Serial.print(F("\nSending photocell val "));
  Serial.print(x);
  Serial.print("...");
  if (! photocell.publish(x++)) {
    Serial.println(F("Failed"));
  } else {
    Serial.println(F("OK!"));
  }
 
}
///////////////////////////////////////////////////////////////////////

// Function to connect and reconnect as necessary to the MQTT server.
// Should be called in the loop function and it will take care if connecting.
void MQTT_connect() {
  int8_t ret;

  // Stop if already connected.
  if (mqtt.connected()) {
    return;
  }

  Serial.print("Connecting to MQTT... ");

  uint8_t retries = 3;
  while ((ret = mqtt.connect()) != 0) { // connect will return 0 for connected
       Serial.println(mqtt.connectErrorString(ret));
       Serial.println("Retrying MQTT connection in 5 seconds...");
       mqtt.disconnect();
       delay(5000);  // wait 5 seconds
       retries--;
       if (retries == 0) {
         // basically die and wait for WDT to reset me
         while (1);
       }
  }
  Serial.println("MQTT Connected!");
}
///////////////////////////////////////////////////////////////////////////////////////
void UpdateServos()
{
  servo1.write(map(rotHor,-60,60,180,0));
  servo2.write(map(rotVer,-40,25,70,0));
  //delay(250);
}