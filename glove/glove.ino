
int sensor0;
int sensor1;
int sensor2;
void setup()
{
  Serial.begin(9600);
}

void loop()
{
  sensor0 = analogRead(0);
  sensor1 = analogRead(1);
  sensor2 = analogRead(2);
  
  if Serial.available()
  {
    Serial.read()
    Serial.print('s');
    Serial.print(sensor0);
    Serial.print(':');
    Serial.print(sensor1);
    Serial.print(':');
    Serial.print(sensor2);
    Serial.println('e');
  }
}
