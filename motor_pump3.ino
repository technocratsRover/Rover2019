#include <Stepper.h>
//Pins for stepper
const int stepsPerRevolution = 200;  
char val;
//black-out4
//red-out3
//orange-out1
//green-out2

//in1-3
//in2-4
//in3-5
//in4-6
//enable short
//arduino common ground w/ source 
Stepper myStepper(stepsPerRevolution, 3, 4, 5, 6);
//pumps
int enA = 9;
int in1 = 10;
int in2 = 12;

int enB = 7;
int in3 = 11;
int in4 = 8;

int enC=A0; //eA
int in5=A1; //i1
int in6=A2;  //i2

int in7=A3;  //i3
int in8=A4;   //i4
int enD=13;   //eb


void pump() //activates pump
 {
   if(Serial.available())
  {
    val=Serial.read();
  }

  if(val=='1')
 { digitalWrite(in2, HIGH);
   }
   if(val=='2')
 { digitalWrite(in3, HIGH);
 }

  if(val=='3')
 { digitalWrite(in5, HIGH);
   }
    if(val=='4')
 { digitalWrite(in7, HIGH);
   }

  }  

  
  void stopp() // stops all pumps 
  {
 digitalWrite(in1, LOW);
 digitalWrite(in2, LOW);
 digitalWrite(in3, LOW);
 digitalWrite(in4, LOW);
 digitalWrite(in5, LOW);
 digitalWrite(in6, LOW);
 digitalWrite(in7, LOW);
 digitalWrite(in8, LOW);
  }
 void stepm()
 {
  if(Serial.available())
  {
    val=Serial.read();
  }
  
  if(val=='a')
  {
  myStepper.step(700/6); //one sixth rev
  val='0';
  }

  
   if(val=='c')
  {
  myStepper.step(-700/6);
  val='0';
  }
 }




 
void setup() {
 
  myStepper.setSpeed(30);
  pinMode(enA, OUTPUT);
  pinMode(enB, OUTPUT);
  pinMode(enC, OUTPUT);
  pinMode(enD, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(in3, OUTPUT);
  pinMode(in4, OUTPUT);
   pinMode(in5, OUTPUT);
  pinMode(in6, OUTPUT);
  pinMode(in7, OUTPUT);
  pinMode(in8, OUTPUT);
  digitalWrite(in2, LOW);
  analogWrite(enA, 200);
  digitalWrite(in1, LOW);
   digitalWrite(in3, LOW);
  analogWrite(enB, 200);
  digitalWrite(in4, LOW);
   analogWrite(enC, 200);
    digitalWrite(in5, LOW);
  digitalWrite(in6, LOW);
   analogWrite(enD, 200);
  digitalWrite(in8, LOW);
   digitalWrite(in7, LOW);
  Serial.begin(9600);
  val='0';
 
 
 

}
void loop() {
  
  if(Serial.available())
  {
    val=Serial.read();
  }

 if(val=='c'||val=='a') //stepper control
 {
  stepm();
 }
 
if(val=='1'||val=='2'||val=='3'||val=='4')
{
 pump(); //activate pump
}
if(val=='s')
 {
 stopp();
 }  

 }


 
 
