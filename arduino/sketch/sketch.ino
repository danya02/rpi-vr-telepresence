#include <Servo.h>

#define SERIAL_BAUD_RATE 19200

#define BASE_PIN 3
#define ARM_MAJOR_PIN 5
#define ARM_MINOR_PIN 6
#define KLAW_PIN 9

// Message is two bytes: first is key, second is value.
// Key specifies servo to control, value is what to write to servo (expecting 0..180)

Servo base;    // key is B (ASCII 0x42)
Servo arm_maj; // key is A (ASCII 0x41)
Servo arm_min; // key is a (ASCII 0x61)
Servo klaw;    // key is K (ASCII 0x4b)

void setup() {
  Serial.begin(SERIAL_BAUD_RATE);
  base.attach(BASE_PIN);
  arm_maj.attach(ARM_MAJOR_PIN);
  arm_min.attach(ARM_MINOR_PIN);
  klaw.attach(KLAW_PIN);
}

void loop() {
  // put your main code here, to run repeatedly:
  int a = -1;
  while(a == -1){a = Serial.read();}
  int b = -1;
  while(b == -1){b = Serial.read();}
  set((char)a, b);
}

void set(char segment, int value){
  Servo s;
  switch(segment){
    case 'B':s=base;break;
    case 'A':s=arm_maj;break;
    case 'a':s=arm_min;break;
    case 'K':s=klaw;break;
    default:return;
  }
  Serial.print(segment);
  Serial.print("->");
  Serial.println(value);
  s.write(value);
}
