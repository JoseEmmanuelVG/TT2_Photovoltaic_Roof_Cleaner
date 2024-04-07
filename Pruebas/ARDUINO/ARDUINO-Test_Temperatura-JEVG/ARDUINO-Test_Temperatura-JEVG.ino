#include <DHT.h>

// Definir el pin de conexión del sensor DHT11
#define DHTPIN 2     // El pin donde se conecta el sensor

// Definir el tipo de sensor DHT
#define DHTTYPE DHT11   // DHT 11

// Inicializar el sensor DHT
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600); // Iniciar la comunicación serial
  dht.begin(); // Iniciar el sensor DHT
}

void loop() {
  // Esperar unos segundos entre mediciones
  delay(2000);

  // Leer la humedad relativa
  float h = dht.readHumidity();
  // Leer la temperatura en Celsius (también se pueden obtener los grados Fahrenheit con readTemperature(true))
  float t = dht.readTemperature();

  // Verificar si alguna lectura falló y salir temprano (para intentar de nuevo).
  if (isnan(h) || isnan(t)) {
    Serial.println("¡Fallo en la lectura del sensor DHT11!");
    return;
  }

  // Imprimir los valores en la terminal serial
  Serial.print("Humedad: ");
  Serial.print(h);
  Serial.print(" %\t");
  Serial.print("Temperatura: ");
  Serial.print(t);
  Serial.println(" *C ");
}
