

/* * uncomment ps2
   change rx and tx pins

*/
#include <SoftwareSerial.h>
#include <Cytron_PS2Shield.h>
int Select = 1, Start = 1, Ps2_UP = 1, Ps2_LEFT = 1, Ps2_DOWN = 1, Ps2_RIGHT = 1, Ps2_LEFT1 = 1, Ps2_LEFT2 = 1, Ps2_RIGHT1 = 1, Ps2_RIGHT2 = 1, Ps2_TRIANGLE = 1, Ps2_CIRCLE = 1, Ps2_CROSS = 1, Ps2_SQUARE = 1;


Cytron_PS2Shield ps2(10,11);
char prev='a';
char current='a';

void setup()
{
  ps2.begin(9600);
  // This baudrate must same with the jumper setting at PS2 shield
  
  Serial.begin(9600);
  Serial.println("Initialized");

}
void loop()
{ 
  Select = ps2.readButton(PS2_SELECT);
  Start = ps2.readButton(PS2_START);
  Ps2_UP = ps2.readButton(PS2_UP);
  Ps2_DOWN = ps2.readButton(PS2_DOWN);
  Ps2_RIGHT = ps2.readButton(PS2_RIGHT);
  Ps2_LEFT = ps2.readButton(PS2_LEFT);
  Ps2_LEFT1 = ps2.readButton(PS2_LEFT_1);
  Ps2_LEFT2 = ps2.readButton(PS2_LEFT_2);
  Ps2_RIGHT1 = ps2.readButton(PS2_RIGHT_1);
  Ps2_RIGHT2 = ps2.readButton(PS2_RIGHT_2);
  Ps2_TRIANGLE = ps2.readButton(PS2_TRIANGLE);
  Ps2_CIRCLE = ps2.readButton(PS2_CIRCLE);
  Ps2_CROSS = ps2.readButton(PS2_CROSS);
  Ps2_SQUARE = ps2.readButton(PS2_SQUARE);

   if (Ps2_LEFT == 0) {
//    Serial.println("0");
       current='0';

  }
  else if(Ps2_RIGHT== 0){
//    Serial.println("1");
    current='1';
}
 else if (Ps2_UP == 0) {
//    Serial.println("2");
    current='2';
  } 
  else if (Ps2_DOWN == 0) {
//    Serial.println("3");
  current='3';
  }
  else if (Ps2_LEFT1 == 0){
//    Serial.println("4");
    current='4';
}
  else if (Ps2_LEFT2 == 0){
//    Serial.println("5");
      current='5';
}
  else if (Ps2_RIGHT1 == 0){
//    Serial.println("6");
      current='6';
} 
 else if (Ps2_RIGHT2 == 0){
//    Serial.println("7");
    current='7';
}
  else if (Ps2_CIRCLE == 0){
//    Serial.println("c");
    current='c';
}
  else if (Ps2_TRIANGLE == 0){
//    Serial.println("t");
    current='t';
}
  else if (Ps2_CROSS == 0){
//    Serial.println("x");
    current='x';
}
  else if (Ps2_SQUARE == 0){
//    Serial.println("s");
    current='s';

}
else{
//  Serial.println("a");
  current='a';
}
if(current!=prev)
  prev=current;
Serial.println(prev);

}
