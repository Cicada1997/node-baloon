#include <WiFi.h>

const char *ssid = "Node_bloon_0";
const char *password = "theoAFS";

WiFiServer server(80);

void setup() {
  Serial.begin(115200);
  WiFi.softAP(ssid, password);
  server.begin();
}

void loop() {
  WiFiClient client = server.available();
  if (client) {
    String request = client.readStringUntil('\r');
    client.flush();

    client.println("HTTP/1.1 200 OK");
    client.println("Content-type:text/html");
    client.println();
    client.println("<h1>ESP32 Web Server</h1>");
    client.println("<p><a href='/LEDON'>Turn LED ON</a></p>");
    client.println("<p><a href='/LEDOFF'>Turn LED OFF</a></p>");
    client.println();
  }
}
