const int luz_led[3] = {3, 4, 5};

void setup() {
  Serial.begin(9600);
  for (int i = 0; i < 3; i++) {
    pinMode(luz_led[i], OUTPUT);
  }
}

void loop() {
  if (Serial.available() > 0) {
    String msg = Serial.readStringUntil('\n');
    msg.trim();//limpieza d espacios
    if (msg.length() == 5) {
      for (int i = 0; i < 3; i++) {
        if (msg[i] == '1') {
          digitalWrite(luz_led[i], HIGH);
        } else {
          digitalWrite(luz_led[i], LOW);
        }
      }
    }
  }
}