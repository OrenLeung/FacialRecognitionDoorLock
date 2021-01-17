#include <Servo.h>
Servo myservo;
String inByte;
const int button_pin = 2;
int pos;
int Locked = 0;

void setup()
{

  myservo.attach(9);
  myservo.write(90);
  Serial.begin(9600);
  pinMode(button_pin, INPUT);
}

void Lock(Servo myservo){
  myservo.write(155);
}

void Unlock(Servo myservo){
  myservo.write(90);
}

void loop()
{
  if (Serial.available())
  {
    inByte = Serial.readString();
    pos = inByte.toInt();
    Serial.print(inByte);
    if (strstr(const_cast<char *>(inByte.c_str()), "L") != NULL)
    {
      Locked = 1;
      Serial.print(inByte);
      Serial.print("Locking\n");
    }
    else if (strstr(const_cast<char *>(inByte.c_str()), "U") != NULL)
    {
      Locked = 0;
      Serial.print("Unlocking\n");
    }
  }

  if(digitalRead(button_pin)){
     Unlock(myservo);
  }else{
    if(Locked){
      Lock(myservo);
    }else{
      Unlock(myservo);
    }
  }

}
