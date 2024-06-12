#include <DHT.h>
#include <NewPing.h>

// Pines y constantes
#define DHTPIN 10
#define DHTTYPE DHT11
#define TRIGGER_PIN_1 2
#define ECHO_PIN_1 3
#define TRIGGER_PIN_2 4
#define ECHO_PIN_2 5
#define TRIGGER_PIN_3 6
#define ECHO_PIN_3 7
#define TRIGGER_PIN_4 8
#define ECHO_PIN_4 9
#define MAX_DISTANCE 200
#define LED_PIN 13

// Inicialización de sensores
DHT dht(DHTPIN, DHTTYPE);
NewPing sonar1(TRIGGER_PIN_1, ECHO_PIN_1, MAX_DISTANCE);
NewPing sonar2(TRIGGER_PIN_2, ECHO_PIN_2, MAX_DISTANCE);
NewPing sonar3(TRIGGER_PIN_3, ECHO_PIN_3, MAX_DISTANCE);
NewPing sonar4(TRIGGER_PIN_4, ECHO_PIN_4, MAX_DISTANCE);

void setup() {
    Serial.begin(9600);
    dht.begin();
    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, HIGH); // Encender LED al inicio
    delay(1000);
    digitalWrite(LED_PIN, LOW);
}

void loop() {
    // Lectura de sensores ultrasónicos
    int distance1 = sonar1.ping_cm();
    int distance2 = sonar2.ping_cm();
    int distance3 = sonar3.ping_cm();
    int distance4 = sonar4.ping_cm();
    
    // Enviar distancias por serial (separadas por comas)
    Serial.print(distance1); 
    Serial.print(",");
    Serial.print(distance2);
    Serial.print(",");
    Serial.print(distance3);
    Serial.print(",");
    Serial.println(distance4);

    // Lectura de temperatura y humedad
    delay(2000); // Esperar 2 segundos entre lecturas del DHT11
    float humidity = dht.readHumidity();
    float temperature = dht.readTemperature();

    if (!isnan(humidity) && !isnan(temperature)) {
        Serial.print("Humedad: ");
        Serial.print(humidity);
        Serial.print(" %\t");
        Serial.print("Temperatura: ");
        Serial.print(temperature);
        Serial.println(" *C ");
    } else {
        Serial.println("¡Fallo en la lectura del sensor DHT11!");
    }
    
    // Control del LED (parpadea cada segundo)
    digitalWrite(LED_PIN, HIGH);
    delay(500);
    digitalWrite(LED_PIN, LOW);
    delay(500);
}
