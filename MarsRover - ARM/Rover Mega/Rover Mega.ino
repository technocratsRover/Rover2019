
/* * uncomment ps2
   change rx and tx pins

*/
#include <SoftwareSerial.h>

String prev="a";
String current="a";

String inp = "";
// BASE
int pwm0 = 4;
int dir0 = 5;
// 1ST
int pwm1 = 6;
int dir1 = 7;
// 2ND
int pwm2 = 8;
int dir2 = 9;
//3RD
int pwm3 = A0;
int dir3 = 10;
//4TH
int pwm4 = A3;
int dir4 = 11;
//GRIPPER
int pwm5 = A4;
int dir5 = 12;


void moveMotor(String inp){
    if (inp == "0") {
//    Serial.println("PS2_LEFT");
    digitalWrite(pwm0, HIGH);
    digitalWrite(dir0, HIGH);
    
//    digitalWrite(13,HIGH);
    
  }
  else if(inp== "1"){
//    Serial.println("PS2_RIGHT");
    digitalWrite(pwm0,HIGH);
    digitalWrite(dir0,LOW);
}
 else if (inp == "2") {
//    Serial.println("PS2_UP");
    digitalWrite(pwm1, HIGH);
    digitalWrite(dir1, HIGH);
  } 
  else if (inp == "3") {
//    Serial.println("PS2_DOWN");
    digitalWrite(pwm1, HIGH);
    digitalWrite(dir1, LOW);
//    delay(200);
  }
 
  else if (inp=="4"){
//    Serial.println("PS2_LEFT1");
  digitalWrite(pwm2, HIGH);
  digitalWrite(dir2, HIGH);
}
  else if (inp=="5"){
//    Serial.println("PS2_LEFT2");
  digitalWrite(pwm2, HIGH);
  digitalWrite(dir2, LOW);
}
  else if (inp=="6"){
//    Serial.println("PS2_RIGHT1");
  digitalWrite(pwm3, HIGH);
  digitalWrite(dir3, HIGH);
}
 else if (inp=="7"){
//    Serial.println("PS2_RIGHT2");
  digitalWrite(pwm3, HIGH);
  digitalWrite(dir3, LOW);
}
  else if (inp=="c"){
//    Serial.println("CIRCLE");
  digitalWrite(pwm4, HIGH);
  digitalWrite(dir4, HIGH);
}
  else if (inp=="t"){
//    Serial.println("PS2_TRIANGLE");
  digitalWrite(pwm5, HIGH);
  digitalWrite(dir5, HIGH);
}
  else if (inp=="x"){
//    Serial.println("PS2_CROSS");
  digitalWrite(pwm5, HIGH);
  digitalWrite(dir5, LOW);
}
  else if (inp=="s"){
//    Serial.println("PS2_SQUARE");
  digitalWrite(pwm4, HIGH);
  digitalWrite(dir4, LOW); 
}
    else if(inp=="a"){
    digitalWrite(pwm0, LOW);
//    digitalWrite(dir0, LOW);
    digitalWrite(pwm1, LOW);
//    digitalWrite(dir1, LOW);
    digitalWrite(pwm2, LOW);
//    digitalWrite(dir2, LOW);'
    digitalWrite(pwm3, LOW);
//    digitalWrite(dir3, LOW);
    digitalWrite(pwm4, LOW);
//    digitalWrite(dir4, LOW);
    digitalWrite(pwm5, LOW);
//    digitalWrite(dir5, LOW);
  }
 
}

void setup()
{

  
  Serial.begin(9600);
  Serial.setTimeout(25);
  Serial.println("Initialized");
  pinMode(pwm0, OUTPUT);
  pinMode(dir0, OUTPUT);
  pinMode(pwm1, OUTPUT);
  pinMode(dir1, OUTPUT);
  pinMode(pwm2, OUTPUT);
  pinMode(dir2, OUTPUT);
  pinMode(pwm3, OUTPUT);
  pinMode(dir3, OUTPUT);
  pinMode(pwm4, OUTPUT);
  pinMode(dir4, OUTPUT);
  pinMode(pwm5, OUTPUT);
  pinMode(dir5, OUTPUT);
}


void loop()
{
  digitalWrite(13,HIGH);
//  Serial.println(Serial.available());
  while(Serial.available()>0){
  current = Serial.readString();

  if(current!=prev)
    prev=current;
  moveMotor(prev);
  }
//Serial.flush();
  digitalWrite(13,LOW);
}
