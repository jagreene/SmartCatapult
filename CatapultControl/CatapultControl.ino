

#include <SPI.h>
#include <Servo.h>

Servo servoA;
Servo servoB;
Servo servoC;
Servo servoD;

unsigned int posA = 0;
unsigned int posB = 0;
unsigned int posC = 0;
unsigned int posD = 0;

unsigned int resetBPos = 45;
unsigned int resetCPos = 22;

unsigned int cockPos = 90;
unsigned int firePos = 120;

unsigned int bufferLength;


void command() {
  char buffer[64];
  int i, ch, val;
  long j, num;
  

  for (i = 0; i<63; i++) {
    for (ch = Serial.read(); ch==-1; ch = Serial.read()) {}
    if (ch==';')
      break;
    buffer[i] = (char)ch;
  }
  buffer[i] = '\0';
  bufferLength = i;
  if ((!strncmp(buffer, "posA?", 4)) || (!strncmp(buffer, "POSA?", 4))) {
    posA = 0;
    for (i = 5; i<bufferLength; i++){
      posA += (buffer[i]-48)*pow(10,bufferLength-i-1);
    }
    Serial.print("Setting Servo A to ");
    Serial.println(posA);
  }
  if ((!strncmp(buffer, "posB?", 4)) || (!strncmp(buffer, "POSB?", 4))) {
    Serial.print("Setting Servo B to ");
    posB = 0;
    for (i = 5; i<bufferLength; i++){
      posB += (buffer[i]-48)*pow(10,bufferLength-i-1);
    }
    Serial.println(posB);
  }
  if ((!strncmp(buffer, "posC?", 4)) || (!strncmp(buffer, "POSC?", 4))) {
    Serial.print("Setting Servo C to ");
    posC = 0;
    for (i = 5; i<bufferLength; i++){
      posC += (buffer[i]-48)*pow(10,bufferLength-i-1);
    }
    Serial.println(posC);
  }
  if ((!strncmp(buffer, "posD?", 4)) || (!strncmp(buffer, "POSD?", 4))) {
    Serial.print("Setting Servo D to ");
    posD = 0;
    for (i = 5; i<bufferLength; i++){
      posD += (buffer[i]-48)*pow(10,bufferLength-i-1);
    }
    Serial.println(posD);
  }
  if ((!strncmp(buffer, "test", 4)) || (!strncmp(buffer, "TEST", 4))) {
    Serial.print("Moving Servos to:");
    Serial.println(posA);
    Serial.println(posB);
    Serial.println(posC);
    Serial.println(posD);
    test_servos(posA, posB, posC, posD);
  }
  if ((!strncmp(buffer, "shoot", 4)) || (!strncmp(buffer, "SHOOT", 4))) {
    Serial.print("FIRE");
    shoot(posA, posD);
  }
}

void test_servos(int posA, int posB, int posC, int posD){
  Serial.println("Testing");
  servoA.write(posA);
  delay(20);
  servoB.write(posB);
  delay(20);
  servoC.write(posC);
  delay(20);
  servoC.write(posD);
  delay(20);
  
  
  posA = 0;
  posB = 0;
  posC = 0;
}

void shoot(int posA, int posD){
    Serial.println("Shooting");
    
    //make sure arm is lowered
    servoB.write(resetBPos);
    delay(100);
    //trap arm
    servoC.write(resetCPos);
    delay(20);
    //set angle to user inputed angle and tension arm
    servoA.write(posA);
    servoD.write(posD);
    servoB.write(cockPos);
    delay(200);
    //Pull the trigger
    servoC.write(firePos);
    delay(300);
    
    //Reset
    servoB.write(resetBPos);
}

void setup() {
  servoA.attach(2);
  servoB.attach(3);
  servoC.attach(4);
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);  
  Serial.begin(115200);
}

void loop() {
  if (Serial.available()>0) {
    command();
    digitalWrite(13, LOW);  
  }
}

