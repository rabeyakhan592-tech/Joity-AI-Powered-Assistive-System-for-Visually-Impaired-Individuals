#include <LiquidCrystal.h>
#include <SoftwareSerial.h>
#include <TinyGPS++.h>

// ---------------- LCD ----------------
LiquidCrystal lcd(2, 3, 4, 5, 6, 7);

// ---------------- GSM ----------------
SoftwareSerial GSM(11, 10);
char phone_no[] = "+88017********"; // Replace with recipient number

// ---------------- GPS ----------------
SoftwareSerial gpsSerial(8, 9);
TinyGPSPlus gps;

bool fixSent = false;  // Has the first fix SMS been sent?
bool hadSats = false;  // Were satellites found before?

// ---------------- Setup ----------------
void setup() {
  lcd.begin(16, 2);
  lcd.print("Initializing...");
  delay(2000);

  Serial.begin(9600);

  // GSM init
  GSM.begin(9600);
  delay(1000);
  initModule("AT", "OK", 1000);
  initModule("AT+CMGF=1", "OK", 1000);
  initModule("AT+CNMI=1,2,0,0,0", "OK", 1000);

  // GPS init
  gpsSerial.begin(9600);

  lcd.clear();
  lcd.print("GPS: Searching");
}

// ---------------- Loop ----------------
void loop() {
  // ---- GPS Handling ----
  while (gpsSerial.available()) {
    char c = gpsSerial.read();
    gps.encode(c);
  }

  // Show satellite status
  if (gps.satellites.value() > 0 && !hadSats) {
    lcd.clear();
    lcd.print("Satellites Found!");
    hadSats = true;
    delay(2000);
  }

  // If GPS fix available
  if (gps.location.isValid() && !fixSent) {
    double lat = gps.location.lat();
    double lng = gps.location.lng();

    lcd.clear();
    lcd.print("Location Found!");
    delay(2000);

    // Send SMS with location
    String msg = "GPS Location: Lat=" + String(lat, 6) + ", Lng=" + String(lng, 6);
    sendSMS(phone_no, msg.c_str());
    fixSent = true;

    delay(2000);
    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print("Lat:");
    lcd.print(lat, 4);
    lcd.setCursor(0, 1);
    lcd.print("Lng:");
    lcd.print(lng, 4);
  }
}

// ---------------- Functions ----------------
void sendSMS(char *number, const char *text) {
  lcd.clear();
  lcd.print("Sending SMS...");
  lcd.setCursor(0, 1);
  lcd.print(number);

  GSM.print("AT+CMGS=\"");
  GSM.print(number);
  GSM.println("\"");
  delay(1000);

  GSM.print(text);
  delay(1000);

  GSM.write(26);   // CTRL+Z
  delay(5000);

  String response = "";
  while (GSM.available()) {
    char c = GSM.read();
    response += c;
    Serial.write(c);
  }

  lcd.clear();
  if (response.indexOf("OK") != -1) {
    lcd.print("SMS Sent!");
  } else {
    lcd.print("SMS Fail!");
  }
  delay(2000);
}

void initModule(String cmd, char *res, int t) {
  for (int i = 0; i < 5; i++) {
    GSM.println(cmd);
    delay(500);

    if (GSM.find(res)) {
      delay(t);
      return;
    }
    delay(t);
  }
  lcd.clear();
  lcd.print("GSM Fail!");
}
