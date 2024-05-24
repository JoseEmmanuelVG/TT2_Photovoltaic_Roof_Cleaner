// Definir los pines de conexión
const int pinPWM = 9;   // Puerto de control de velocidad (PWM)
const int pinDireccion = 7; // Control de avance y retroceso

void setup() {
  // Configurar los pines como salidas
  pinMode(pinPWM, OUTPUT);
  pinMode(pinDireccion, OUTPUT);

  // Establecer la dirección inicial del motor
  digitalWrite(pinDireccion, LOW); // Baja para avance (CW), Alta para retroceso (CCW)
}

void loop() {
  // Establecer la velocidad del motor
  // Puedes cambiar el valor '128' con cualquier valor entre 0 (motor parado) y 255 (velocidad máxima)
  analogWrite(pinPWM, 128);

  // Cambiar la dirección después de un tiempo
  delay(5000); // El motor gira en una dirección por 5 segundos
  digitalWrite(pinDireccion, HIGH); // Cambiar la dirección de rotación
  delay(5000); // El motor gira en la dirección opuesta por 5 segundos
  digitalWrite(pinDireccion, LOW); // Volver a la dirección original
}