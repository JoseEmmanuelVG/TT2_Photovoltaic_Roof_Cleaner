 // Ejemplo_Control_Motor_Paso_a_paso

int PUL=7; //Pin para la señal de pulso
int DIR=6; //define Direction pin
int EN=5; //define Enable Pin

void setup() {
  pinMode(PUL, OUTPUT);
  pinMode(DIR, OUTPUT);
  pinMode(EN, OUTPUT);
  digitalWrite(EN,HIGH);
}

void loop() {
  digitalWrite(DIR,LOW);
  for (int i=0; i<1600; i++) //Forward 1600 steps
  {
    digitalWrite(PUL,HIGH);
    delayMicroseconds(400);
    digitalWrite(PUL,LOW);
    delayMicroseconds(400);
  }
  
  delay(100);
  digitalWrite(DIR,HIGH);
  
  for (int i=0; i<1600; i++) //Backward 1600 steps
  {
    digitalWrite(PUL,HIGH);
    delayMicroseconds(400);
    digitalWrite(PUL,LOW);
    delayMicroseconds(400);
  }
}