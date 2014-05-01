
int sensor0;
int sensor1;
int sensor3;
void setup()
{
  Serial.begin(9600);
}

void loop()
{
  sensor3 = analogRead(3);
  
  Serial.println("Sensor 3");
  Serial.print(sensor3);
}
