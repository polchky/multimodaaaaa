int sensor0;
int sensor1;
int sensor2;
int sensor3;
void setup()
{
  Serial.begin(9600);
}

void loop()
{
  if (Serial.available()){
    Serial.read();
    Serial.print('s');
    for (int i = 0; i < 4; i++){
      Serial.print(analogRead(i));
      Serial.print(':');
    }
    Serial.println('e');
  }
}
